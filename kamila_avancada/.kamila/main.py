import os
import struct
import pvporcupine
import pyaudio
from core import stt_engine, tts_engine, interpreter, actions, memory_manager
import logging
import time
from dotenv import load_dotenv
load_dotenv()

# --- CONFIGURAÇÃO DO PORCUPINE ---
# !!! VERIFIQUE SE SUA ACCESSKEY REAL ESTÁ AQUI !!!
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")


# --- CAMINHO PARA SEU ARQUIVO .PPN ---
# Crie uma pasta 'wake_words' na raiz do seu projeto e coloque o arquivo .ppn dentro dela.
# Em seguida, coloque o nome exato do arquivo aqui.
WAKE_WORD_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'wake_words', 'camila_pt_windows_v3_0_0.ppn')
WAKE_WORD_FILE_PATH = os.path.abspath(WAKE_WORD_FILE_PATH)
MODEL_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'porcupine_models', 'porcupine_params_pt.pv'))


print("[DEBUG] Caminho absoluto:", os.path.abspath(WAKE_WORD_FILE_PATH))
print("[DEBUG] Existe o arquivo?", os.path.exists(WAKE_WORD_FILE_PATH))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def wait_for_wake_word(porcupine, audio_stream):
    """Escuta passivamente o áudio até que a palavra de ativação seja detectada."""
    # Extrai o nome da palavra-chave do caminho do arquivo para o log
    wake_word_name = os.path.basename(WAKE_WORD_FILE_PATH).split('_')[0].capitalize()
    logging.info(f"Aguardando a palavra de ativação ('{wake_word_name}')...")
    
    while True:
        try:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                logging.info(f"Palavra de ativação '{wake_word_name}' detectada!")
                tts_engine.speak("Sim?")
                return
        except IOError as e:
            logging.warning(f"Erro de buffer de áudio, continuando a escuta: {e}")
            continue

def main():
    porcupine = None
    pa = None
    audio_stream = None
    try:
        if PICOVOICE_ACCESS_KEY == 'SUA_ACCESS_KEY_AQUI':
            logging.error("A AccessKey da PicoVoice não foi definida. Por favor, edite o main.py.")
            return
        
        if not os.path.exists(WAKE_WORD_FILE_PATH):
            logging.error(f"Arquivo da palavra de ativação não encontrado em: '{WAKE_WORD_FILE_PATH}'")
            logging.error("Por favor, treine sua palavra-chave no console da PicoVoice e coloque o arquivo .ppn no local correto.")
            return

        logging.info(f"Inicializando Porcupine com o modelo customizado: {WAKE_WORD_FILE_PATH}")
        porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keyword_paths=[WAKE_WORD_FILE_PATH],
            model_path=MODEL_FILE_PATH
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        user_name = memory_manager.get_from_memory('user_name', 'amigo')
        logging.info(f"Camila pronta para o usuário {user_name}.")
        
        while True:
            wait_for_wake_word(porcupine, audio_stream)
            
            comando = stt_engine.listen()

            if comando:
                # ... (resto da lógica de interação) ...
                interaction_count = memory_manager.get_from_memory('interactions', 0) + 1
                memory_manager.update_memory('interactions', interaction_count)
                memory_manager.update_memory('last_interaction_time', time.strftime("%Y-%m-%d %H:%M:%S"))
                logging.info(f"Comando recebido: '{comando}' (Interação nº {interaction_count})")
                
                resposta = interpreter.interpretar_comando(comando)
                if resposta and resposta.get('intent') != 'unknown':
                    resposta = actions.execute_action(intent_data)
                    if resposta:
                        tts_engine.speak(resposta)
                else:
                    tts_engine.speak("Desculpe, não sei como ajudar com isso ainda.")
            else:
                tts_engine.speak("Não entendi o comando, por favor, tente novamente.")

    except pvporcupine.PorcupineError as e:
        logging.error(f"Erro no Porcupine (Palavra de Ativação): {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro crítico no main: {e}", exc_info=True)
    finally:
        logging.info("Encerrando Kamila...")
        if porcupine is not None: porcupine.delete()
        if audio_stream is not None: audio_stream.close()
        if pa is not None: pa.terminate()

if __name__ == "__main__":
    main()