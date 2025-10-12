#!/usr/bin/env python3
"""
TTS Engine - Text-to-Speech para Kamila
Motor de síntese de voz usando pyttsx3.
"""

import os
import sys
import logging
import pyttsx3
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

logger = logging.getLogger(__name__)

class TTSEngine:
    """Motor de síntese de voz."""

    def __init__(self):
        """Inicializa o motor TTS."""
        logger.info("  Inicializando TTS Engine...")

        try:
            # Inicializar pyttsx3
            self.engine = pyttsx3.init()

            # Configurar propriedades da voz
            self._configure_voice()

            # Configurar volume e velocidade
            self._configure_audio_settings()

            logger.info(" TTS Engine inicializado com sucesso!")

        except Exception as e:
            logger.error(f" Erro ao inicializar TTS: {e}")
            self.engine = None

    def _configure_voice(self):
        """Configura a voz do sistema."""
        try:
            # Listar vozes disponíveis
            voices = self.engine.getProperty('voices')

            # Tentar encontrar uma voz em português
            selected_voice = None
            for voice in voices:
                if 'pt' in voice.languages or 'portuguese' in voice.name.lower():
                    selected_voice = voice
                    break

            # Se não encontrou voz PT, usar a primeira disponível
            if not selected_voice and voices:
                selected_voice = voices[0]

            if selected_voice:
                self.engine.setProperty('voice', selected_voice.id)
                logger.info(f"Voz configurada: {selected_voice.name}")

        except Exception as e:
            logger.warning(f"  Erro ao configurar voz: {e}")

    def _configure_audio_settings(self):
        """Configura volume e velocidade da voz."""
        try:
            # Configurar volume (0.0 a 1.0)
            volume = float(os.getenv('VOICE_VOLUME', '0.8'))
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))

            # Configurar velocidade (palavras por minuto)
            rate = int(os.getenv('VOICE_RATE', '180'))
            self.engine.setProperty('rate', rate)

            logger.info(f" Volume: {volume}, Velocidade: {rate} WPM")

        except Exception as e:
            logger.warning(f"  Erro ao configurar áudio: {e}")

    def speak(self, text, wait=True):
        """
        Fala o texto fornecido.

        Args:
            text (str): Texto a ser falado
            wait (bool): Se deve aguardar o fim da fala
        """
        if not self.engine:
            logger.warning("  TTS Engine não inicializado")
            print(f"Kamila: {text}")
            return

        if not text or not text.strip():
            logger.warning("  Texto vazio para falar")
            return

        try:
            logger.debug(f"  Falando: {text}")

            # Falar o texto
            self.engine.say(text)
            self.engine.runAndWait() if wait else self.engine.startLoop(False)

            # Pequena pausa para melhor entonação
            import time
            time.sleep(0.1)

        except Exception as e:
            logger.error(f" Erro ao falar: {e}")
            # Fallback: imprimir o texto
            print(f"Kamila: {text}")

    def speak_async(self, text):
        """
        Fala o texto de forma assíncrona (não bloqueante).

        Args:
            text (str): Texto a ser falado
        """
        if not self.engine:
            logger.warning("  TTS Engine não inicializado")
            print(f"Kamila: {text}")
            return

        try:
            logger.debug(f"  Falando (async): {text}")
            self.engine.say(text)
            self.engine.startLoop(False)

        except Exception as e:
            logger.error(f" Erro ao falar async: {e}")
            print(f"Kamila: {text}")

    def stop_speaking(self):
        """Para a fala atual."""
        if self.engine:
            try:
                self.engine.stop()
                logger.debug("  Fala interrompida")
            except Exception as e:
                logger.error(f" Erro ao parar fala: {e}")

    def get_available_voices(self):
        """Retorna lista de vozes disponíveis."""
        if not self.engine:
            return []

        try:
            voices = self.engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'language': getattr(voice, 'languages', ['unknown'])[0]
                }
                for voice in voices
            ]
        except Exception as e:
            logger.error(f" Erro ao listar vozes: {e}")
            return []

    def set_voice(self, voice_id):
        """
        Define uma voz específica.

        Args:
            voice_id (str): ID da voz a ser usada
        """
        if not self.engine:
            logger.warning("  TTS Engine não inicializado")
            return False

        try:
            self.engine.setProperty('voice', voice_id)
            logger.info(f" Voz alterada para: {voice_id}")
            return True
        except Exception as e:
            logger.error(f" Erro ao alterar voz: {e}")
            return False

    def set_volume(self, volume):
        """
        Define o volume da voz.

        Args:
            volume (float): Volume entre 0.0 e 1.0
        """
        if not self.engine:
            logger.warning("  TTS Engine não inicializado")
            return False

        try:
            volume = max(0.0, min(1.0, float(volume)))
            self.engine.setProperty('volume', volume)
            logger.info(f" Volume alterado para: {volume}")
            return True
        except Exception as e:
            logger.error(f" Erro ao alterar volume: {e}")
            return False

    def set_rate(self, rate):
        """
        Define a velocidade da voz.

        Args:
            rate (int): Velocidade em palavras por minuto
        """
        if not self.engine:
            logger.warning("  TTS Engine não inicializado")
            return False

        try:
            rate = int(rate)
            self.engine.setProperty('rate', rate)
            logger.info(f" Velocidade alterada para: {rate} WPM")
            return True
        except Exception as e:
            logger.error(f" Erro ao alterar velocidade: {e}")
            return False

    def cleanup(self):
        """Limpa recursos do TTS."""
        logger.info(" Limpando TTS Engine...")

        if self.engine:
            try:
                self.engine.stop()
                self.engine = None
                logger.info(" TTS Engine limpo!")
            except Exception as e:
                logger.error(f" Erro ao limpar TTS: {e}")
