"""
STT Engine - Speech-to-Text para Kamila
Motor de reconhecimento de voz usando SpeechRecognition, Porcupine e PyAudio.
Versão final e robusta com fallback inteligente e calibração dinâmica.
"""

import os
import sys
import time
import logging
import speech_recognition as sr
from pvporcupine import create as create_porcupine
from dotenv import load_dotenv
import pyaudio
import struct

# Carregar variáveis de ambiente da raiz do projeto
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logger = logging.getLogger(__name__)

class STTEngine:
    """Motor de reconhecimento de voz."""

    def __init__(self, wake_word="kamila"):
        """Inicializa o motor STT."""
        logger.info("Inicializando STT Engine...")
        self.wake_word = wake_word
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.porcupine = None
        
        self._setup_microphone()
        self._setup_porcupine()
        
        logger.info("STT Engine inicializado com sucesso!")

    def _setup_microphone(self):
        """Configura o microfone e calibra o Recognizer."""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                logger.warning("Nenhum microfone encontrado!")
                return
            
            # --- MELHORIA: Seleção de microfone mais inteligente ---
            device_index = None
            for i, name in enumerate(mic_list):
                # Evita "mapeadores" virtuais que podem causar problemas
                if "mapeador" not in name.lower() and "mapper" not in name.lower():
                    device_index = i
                    break
            if device_index is None: device_index = 0 # Fallback para o padrão

            self.microphone = sr.Microphone(device_index=device_index, sample_rate=16000)

            # --- MELHORIA: Calibração Dinâmica e Robusta ---
            with self.microphone as source:
                logger.info("Ajustando para ruído ambiente... Fique em silêncio.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                self.recognizer.dynamic_energy_threshold = True # Habilita adaptação contínua
                self.recognizer.pause_threshold = 0.8
                logger.info(f"Limiar de energia inicial ajustado para: {self.recognizer.energy_threshold:.2f}")

            logger.info(f"Microfone configurado: {mic_list[device_index]}")

        except Exception as e:
            logger.error(f"Erro crítico ao configurar microfone: {e}")
            self.microphone = None

    def _setup_porcupine(self):
        """Configura o sistema de detecção de wake word."""
        try:
            access_key = os.getenv('PICOVOICE_ACCESS_KEY')
            if not access_key:
                logger.warning("PICOVOICE_ACCESS_KEY não encontrada! Wake word desativada.")
                self.porcupine = None
                return
            
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models', 'porcupine_models', 'porcupine_params_pt.pv')
            keyword_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models', 'wake_words', 'camila_pt_windows_v3_0_0.ppn')
            
            if not os.path.exists(model_path) or not os.path.exists(keyword_path):
                logger.error("Arquivos de modelo do Porcupine (.pv ou .ppn) não encontrados!")
                self.porcupine = None
                return

            self.porcupine = create_porcupine(
                access_key=access_key,
                keyword_paths=[keyword_path],
                model_path=model_path
            )
            logger.info("Porcupine configurado com sucesso para wake word 'kamila'")

        except Exception as e:
            logger.error(f"Erro ao configurar Porcupine: {e}")
            self.porcupine = None

    def block_for_wake_word(self):
        """Ouve continuamente até a wake word ser detectada. Esta é a função principal de escuta passiva."""
        if not self.porcupine:
            logger.error("Porcupine não está configurado. Não é possível detectar wake word. A aplicação ficará em espera.")
            time.sleep(3600) # Pausa longa para evitar loop infinito
            return False

        pa = None
        audio_stream = None
        try:
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length)

            logger.info(f"Microfone aberto. Ouvindo a palavra de ativação '{self.wake_word}'...")

            while True:
                pcm = audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    logger.info("Palavra de ativação detectada!")
                    return True

        except KeyboardInterrupt:
            return False
        finally:
            if audio_stream:
                audio_stream.close()
            if pa:
                pa.terminate()
            logger.info("Microfone para wake word fechado.")
    
    def listen_for_command(self, timeout=10):
        """Ouve e transcreve um comando de voz após a ativação."""
        if not self.microphone:
            logger.error("Microfone não disponível, impossível ouvir o comando.")
            return None

        try:
            logger.info(f"Ouvindo comando (timeout de {timeout}s)...")
            with self.microphone as source:
                # O ajuste dinâmico já está ativo, mas uma pequena recalibração ajuda
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5) 
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            logger.info("Áudio capturado. Transcrevendo...")
            api_key = os.getenv('GOOGLE_API_KEY')
            
            # --- MELHORIA: Fallback Inteligente ---
            command = None
            try:
                # 1. Tenta com a chave de API (melhor qualidade)
                if api_key and api_key != "sua_chave_google_speech_aqui":
                    logger.debug("Tentando transcrever com GOOGLE_API_KEY...")
                    command = self.recognizer.recognize_google(audio, key=api_key, language='pt-BR')
                else:
                    raise sr.RequestError("Chave de API do Google não configurada.")
            except sr.RequestError as e:
                # 2. Se a chave falhar (Unauthorized, offline, etc.), tenta o método padrão
                logger.warning(f"Erro com a API Key ({e}). Usando fallback para o serviço padrão.")
                try:
                    command = self.recognizer.recognize_google(audio, language='pt-BR')
                except Exception as inner_e:
                    logger.error(f"Serviço de reconhecimento padrão também falhou: {inner_e}")
                    return None
            except sr.UnknownValueError:
                logger.warning("Não foi possível entender o áudio.")
                return None
            
            if command:
                logger.info(f"Comando reconhecido: '{command}'")
                return command.lower()
            return None

        except sr.WaitTimeoutError:
            logger.warning("Timeout: Nenhum comando foi falado a tempo.")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao ouvir comando: {e}", exc_info=True)
            return None
            
    def cleanup(self):
        """Limpa recursos."""
        logger.info("Limpando STT Engine...")
        if self.porcupine:
            self.porcupine.delete()
        logger.info("STT Engine limpo!")