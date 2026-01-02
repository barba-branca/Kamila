#!/usr/bin/env python3
"""
STT Engine - Speech-to-Text para Kamila
Motor de reconhecimento de voz usando apenas Google Speech Recognition.
"""

import os
import sys
import time
import logging
import speech_recognition as sr
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

logger = logging.getLogger(__name__)

class STTEngine:
    """Motor de reconhecimento de voz usando Google Speech Recognition."""

    def __init__(self):
        """Inicializa o motor STT."""
        logger.info(" Inicializando STT Engine (Google Speech)...")

        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.wake_word_detected = False

        # Configurações
        self.energy_threshold = 300
        self.pause_threshold = 0.8
        self.dynamic_energy_threshold = True

        # Configurar microfone
        self._setup_microphone()

        logger.info(" STT Engine inicializado com sucesso!")

    def _setup_microphone(self):
        """Configura o microfone."""
        try:
            # Listar microfones disponíveis
            mic_list = sr.Microphone.list_microphone_names()

            if not mic_list:
                logger.warning("  Nenhum microfone encontrado!")
                return

            # Usar o microfone padrão (índice 0)
            self.microphone = sr.Microphone(device_index=0)

            # Ajustar configurações do microfone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            logger.info(f"  Microfone configurado: {mic_list[0]}")

        except Exception as e:
            logger.error(f" Erro ao configurar microfone: {e}")
            self.microphone = None

    def detect_wake_word(self, wake_word="kamila", timeout=10):
        """
        Detecta a palavra de ativação usando Google Speech Recognition.

        Args:
            wake_word (str): Palavra de ativação
            timeout (int): Tempo limite em segundos

        Returns:
            bool: True se wake word foi detectada
        """
        if not self.microphone:
            logger.warning("  Microfone não disponível")
            return False

        try:
            logger.debug(" Ouvindo wake word...")

            with self.microphone as source:
                # Ajustar para ruído ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                # Ouvir áudio
                audio = self.recognizer.listen(source, timeout=timeout)

            # Tentar reconhecer usando Google Speech Recognition
            try:
                # Pegar chave da API do Google
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key and api_key != "your_google_speech_api_key_here":
                    command = self.recognizer.recognize_google(audio, key=api_key, language='pt-BR')
                else:
                    command = self.recognizer.recognize_google(audio, language='pt-BR')

                logger.info(f" Comando reconhecido: {command}")

                # Verificar se contém a wake word
                if wake_word.lower() in command.lower():
                    logger.info(f"  Wake word '{wake_word}' detectada!")
                    return True
                else:
                    logger.debug(f" Wake word '{wake_word}' não detectada em: {command}")
                    return False

            except sr.UnknownValueError:
                logger.debug(" Comando não entendido")
                return False
            except sr.RequestError as e:
                logger.error(f" Erro no serviço de reconhecimento: {e}")
                return False

        except Exception as e:
            logger.error(f" Erro na detecção de wake word: {e}")
            return False

    def listen_for_command(self, timeout=5):
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
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                # Ouvir áudio
                audio = self.recognizer.listen(source, timeout=timeout)

            # Tentar reconhecer usando Google Speech Recognition
            try:
                # Pegar chave da API do Google
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key and api_key != "your_google_speech_api_key_here":
                    command = self.recognizer.recognize_google(audio, key=api_key, language='pt-BR')
                else:
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
        logger.info(" STT Engine limpo!")
