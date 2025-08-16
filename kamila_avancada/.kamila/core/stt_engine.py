import speech_recognition as sr
import logging
import time

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.2  # tempo de pausa para considerar fim de fala

# Função para obter microfone padrão
def get_microphone():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        logging.info(f"Microfones disponíveis: {mic_list}")
        return sr.Microphone()
    except Exception as e:
        logging.error(f"Erro ao acessar os microfones: {e}")
        return None

# Função principal de escuta
def listen(timeout=7, phrase_time_limit=10):
    mic = get_microphone()
    if not mic:
        logging.error("STT Engine: Nenhum microfone disponível.")
        return None

    try:
        with mic as source:
            logging.info("STT Engine: Calibrando ruído ambiente por 2 segundos...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            logging.info(f"STT Engine: Limiar de energia definido: {recognizer.energy_threshold:.2f}")
            logging.info("STT Engine: Diga algo...")

            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("STT Engine: Processando áudio...")

            # Transcrição
            text = recognizer.recognize_google(audio, language='pt-BR')
            logging.info(f"STT Engine: Texto reconhecido -> '{text}'")
            return text.strip().lower()

    except sr.WaitTimeoutError:
        logging.warning("STT Engine: Tempo de espera excedido. Nenhuma fala detectada.")
    except sr.UnknownValueError:
        logging.warning("STT Engine: Áudio incompreensível.")
    except sr.RequestError as e:
        logging.error(f"STT Engine: Erro na API do Google: {e}")
    except Exception as e:
        logging.error(f"STT Engine: Erro inesperado: {e}")

    return None

# Teste local
if __name__ == '__main__':
    print("🔊 Testando reconhecimento de voz...")
    comando = listen()
    if comando:
        print(f"✅ Você disse: {comando}")
    else:
        print("⚠️ Nenhuma entrada válida reconhecida.")
