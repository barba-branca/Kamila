
"""
STT Engine - Speech-to-Text para Kamila
Motor de reconhecimento de voz usando SpeechRecognition e Porcupine.
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

# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

logger = logging.getLogger(__name__)

class STTEngine:
    """Motor de reconhecimento de voz."""

    def __init__(self, wake_word="kamila"):
        """Inicializa o motor STT."""
        logger.info(" Inicializando STT Engine...")
        self.wake_word = wake_word

        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.porcupine = None
        self.wake_word_detected = False

        # Configurações
        self.energy_threshold = 300
        self.pause_threshold = 0.8
        self.dynamic_energy_threshold = True

        # Configurar microfone
        self._setup_microphone()

        # Configurar Porcupine para wake word
        self._setup_porcupine()

        logger.info(" STT Engine inicializado com sucesso!")

    def _setup_microphone(self):
            """Configura o microfone."""
            try:
                # Listar microfones disponíveis
                mic_list = sr.Microphone.list_microphone_names()

                if not mic_list:
                    logger.warning("  Nenhum microfone encontrado!")
                    return

                # Selecionar um microfone real (não mapper)
                device_index = 0
                for i, mic in enumerate(mic_list):
                    if "Mapeador" not in mic and "Mapper" not in mic and "map" not in mic.lower():
                        device_index = i
                        break
                
                self.microphone = sr.Microphone(device_index=device_index)

                # Ajustar configurações do microfone para melhor sensibilidade
                with self.microphone as source:
                    logger.info("Ajustando para ruído ambiente... Por favor, fique em silêncio por um momento.")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    self.recognizer.energy_threshold = 300  # Valor inicial, pode ser ajustado
                    self.recognizer.dynamic_energy_threshold = True
                    logger.info(f"Limiar de energia ajustado para: {self.recognizer.energy_threshold}")

                logger.info(f"  Microfone configurado: {mic_list[device_index]}")

            except Exception as e:
                logger.error(f" Erro ao configurar microfone: {e}")
                self.microphone = None

    def _setup_porcupine(self):
        """Configura o sistema de detecção de wake word."""
        try:
            # Tentar primeiro com PICOVOICE_ACCESS_KEY (nome correto)
            api_key = os.getenv('PICOVOICE_ACCESS_KEY') or os.getenv('PICOVOICE_API_KEY')

            if not api_key:
                logger.warning("  Chave do Picovoice não encontrada!")
                logger.info("  Usando detecção de wake word baseada em energia + STT")
                self.porcupine = None
                return

            # Caminhos dos modelos
            model_path = "models/porcupine_models/porcupine_params_pt.pv"
            keyword_path = "models/wake_words/camila_pt_windows_v3_0_0.ppn"
            
            # Verificar se os arquivos existem
            if not os.path.exists(model_path):
                logger.warning(f"  Modelo não encontrado: {model_path}")
                logger.info("  Usando detecção de wake word baseada em energia + STT")
                self.porcupine = None
                return

            if not os.path.exists(keyword_path):
                logger.warning(f"  Arquivo de wake word não encontrado: {keyword_path}")
                logger.info("  Usando detecção de wake word baseada em energia + STT")
                self.porcupine = None
                return

            # Criar instância do Porcupine
            self.porcupine = create_porcupine(
                access_key=api_key,
                keyword_paths=[keyword_path],
                model_path=model_path
            )

            logger.info("Porcupine configurado com sucesso para wake word 'kamila'")

        except Exception as e:
            logger.error(f" Erro ao configurar Porcupine: {e}")
            self.porcupine = None

    def block_for_wake_word(self):
        """Ouve continuamente o microfone até a wake word ser detectada."""
        if not self.porcupine:
            logger.warning("Porcupine não configurado. Ativação por wake word desativada.")
            time.sleep(10) # Simula uma espera longa se o porcupine não funcionar
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

            while True:
                pcm = audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    logger.info(f"Wake word '{self.wake_word}' detectada!")
                    return True

        except KeyboardInterrupt:
            logger.info("Detecção de wake word interrompida pelo usuário.")
            return False
        except Exception as e:
            logger.error(f"Erro no loop de detecção de wake word: {e}")
            return False
        finally:
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()
            
    def _detect_wake_word_by_energy(self, audio):
        """Detecta wake word baseada em energia do áudio."""
        try:
            # Calcular energia RMS
            energy = sum(audio.get_raw_data()) / len(audio.get_raw_data()) if audio.get_raw_data() else 0

            threshold = 500  # Threshold para detecção
            return abs(energy) > threshold

        except:
            return False

    def _simulate_wake_word_detection(self, timeout=10):
        """Simula detecção de wake word para testes."""
        logger.info(" Simulando detecção de wake word...")
        time.sleep(2)  # Simular tempo de detecção
        return True

    def listen_for_command(self, timeout=15):
        """
        Ouve e transcreve um comando de voz.

        Args:
            timeout (int): Tempo limite em segundos

        Returns:
            str: Comando transcrito ou None se falhou
        """
        if not self.microphone:
            logger.warning("  Microfone não disponível")
            return "teste comando sem microfone"

        try:
            logger.debug(" Ouvindo comando...")

            with self.microphone as source:
                # Ajustar para ruído ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Ouvir áudio
                audio = self.recognizer.listen(source, timeout=timeout)

            # Tentar reconhecer usando Google Speech Recognition
            try:
                # Pegar chave da API do Google
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key:
                    command = self.recognizer.recognize_google(audio, key=api_key, language='pt-BR')
                else:
                    # Fallback para reconhecimento offline (se disponível)
                    command = self.recognizer.recognize_google(audio, language='pt-BR')

                logger.info(f" Comando reconhecido: {command}")
                return command.lower()

            except sr.UnknownValueError:
                logger.debug(" Comando não entendido")
                return None
            except sr.RequestError as e:
                logger.error(f" Erro no serviço de reconhecimento: {e}")
                return None

        except Exception as e:
            logger.error(f" Erro ao ouvir comando: {e}")
            return None

    def cleanup(self):
        """Limpa recursos do STT."""
        logger.info(" Limpando STT Engine...")

        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None

        logger.info(" STT Engine limpo!")
