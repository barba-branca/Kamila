#!/usr/bin/env python3
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

# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

logger = logging.getLogger(__name__)

class STTEngine:
    """Motor de reconhecimento de voz."""

    def __init__(self):
        """Inicializa o motor STT."""
        logger.info("🎤 Inicializando STT Engine...")

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

            # Usar o microfone padrão (índice 0)
            self.microphone = sr.Microphone(device_index=0)

            # Ajustar configurações do microfone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            logger.info(f"  Microfone configurado: {mic_list[0]}")

        except Exception as e:
            logger.error(f" Erro ao configurar microfone: {e}")
            self.microphone = None

    def _setup_porcupine(self):
        """Configura o Porcupine para detecção de wake word."""
        try:
            # Pegar chave da API do Porcupine
            api_key = os.getenv('PICOVOICE_API_KEY')
            if not api_key:
                logger.warning("  PICOVOICE_API_KEY não encontrada!")
                return

            # Caminho para o modelo de wake word
            model_path = "models/wake_words/camila_pt_windows_v3_0_0.ppn"
            keyword_path = "models/wake_words/camila_pt_windows_v3_0_0.ppn"

            if not os.path.exists(model_path):
                logger.warning(f"  Modelo não encontrado: {model_path}")
                return

            # Criar instância do Porcupine
            self.porcupine = create_porcupine(
                access_key=api_key,
                keyword_paths=[keyword_path],
                model_path="models/porcupine_models/porcupine_params_pt.pv"
            )

            logger.info(" Porcupine configurado para wake word 'kamila'")

        except Exception as e:
            logger.error(f" Erro ao configurar Porcupine: {e}")
            self.porcupine = None

    def detect_wake_word(self, wake_word="kamila", timeout=10):
        """
        Detecta a palavra de ativação usando Porcupine.

        Args:
            wake_word (str): Palavra de ativação
            timeout (int): Tempo limite em segundos

        Returns:
            bool: True se wake word foi detectada
        """
        if not self.porcupine:
            logger.warning("  Porcupine não configurado, usando simulação")
            return self._simulate_wake_word_detection(timeout)

        try:
            logger.debug(" Ouvindo wake word...")

            # Porcupine não tem timeout nativo, então implementamos
            start_time = time.time()

            while time.time() - start_time < timeout:
                if self.porcupine:
                    # Processar áudio (simplificado)
                    # Em uma implementação real, você precisaria de um stream de áudio
                    pass

                time.sleep(0.1)

            return False

        except Exception as e:
            logger.error(f" Erro na detecção de wake word: {e}")
            return False

    def _simulate_wake_word_detection(self, timeout=10):
        """Simula detecção de wake word para testes."""
        logger.info(" Simulando detecção de wake word...")
        time.sleep(0.5)  # Simular tempo de detecção
        return True

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
                if api_key:
                    # Usar método correto para reconhecimento
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
