#!/usr-bin/env python3
"""
TTS Engine - Text-to-Speech para Kamila
Motor de síntese de voz usando pyttsx3.
VERSÃO OTIMIZADA - Reutiliza a instância do motor para performance.
"""

import os
import logging
import threading
import pyttsx3
import threading
from dotenv import load_dotenv
import re

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

logger = logging.getLogger(__name__)

class TTSEngine:
    """Motor de síntese de voz otimizado que reutiliza a instância do motor."""

    def __init__(self):
        """Inicializa as configurações do motor TTS e o próprio motor."""
        logger.info("Inicializando TTS Engine...")
        self._lock = threading.Lock()

        # Initialize engine once
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3 engine: {e}")
            raise

        self.voice_id = self._get_portuguese_voice_id()
        self.rate = int(os.getenv('VOICE_RATE', 180))
        self.volume = float(os.getenv('VOICE_VOLUME', 0.9))
        
        # Configure initial properties
        self._configure_engine()

        if self.voice_id:
            logger.info(f"Voz em Português encontrada e configurada.")
        else:
            logger.warning("Nenhuma voz em Português encontrada. Usará a voz padrão do sistema.")
            
        logger.info(f"Volume: {self.volume}, Velocidade: {self.rate} WPM")
        logger.info("TTS Engine configurado com sucesso!")

    def _configure_engine(self):
        """Aplica as configurações atuais ao motor."""
        try:
            if self.voice_id:
                self.engine.setProperty('voice', self.voice_id)
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
        except Exception as e:
            logger.error(f"Erro ao configurar motor TTS: {e}")

    def _get_portuguese_voice_id(self):
        """Busca o ID da voz em português usando o motor existente."""
        try:
            # No need to call init() again or stop()
            voices = self.engine.getProperty('voices')
            for voice in voices:
                # Condição robusta para encontrar a voz correta no Windows
                if 'brazil' in voice.name.lower() or 'pt-br' in getattr(voice, 'id', '').lower():
                    return voice.id
        except Exception as e:
            logger.error(f"Erro ao buscar vozes do sistema: {e}")
        return None

    def _sanitize_text(self, text: str) -> str:
        """Remove caracteres que pyttsx3 não consegue falar, como emojis."""
        if not text:
            return ""
        try:
            # Padrão de regex aprimorado para remover a maioria dos símbolos não-padrão
            emoji_pattern = re.compile(
                "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\u2600-\u26FF"         # miscellaneous symbols
                u"\u2700-\u27BF"         # dingbats
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
        except Exception:
            return text.encode('ascii', 'ignore').decode('ascii')

    def speak(self, text: str):
        """Fala o texto usando o motor compartilhado de forma segura."""
        if not text or not text.strip():
            logger.warning("Texto vazio para falar. Ignorando.")
            return

        sanitized_text = self._sanitize_text(text)

        with self._lock:
            try:
                # Re-apply configuration just in case properties were changed externally
                # or reset (though typically they persist)
                self._configure_engine()

                logger.info(f"Preparando para falar: '{sanitized_text[:70]}...'")

                self.engine.say(sanitized_text)
                self.engine.runAndWait()

                logger.info("Fala concluída com sucesso.")

            except RuntimeError as re_err:
                logger.error(f"Erro de Runtime no TTS (loop já rodando?): {re_err}")
            except Exception as e:
                logger.error(f"Erro CRÍTICO durante a execução da fala: {e}")
                print(f"Kamila (erro de voz): {sanitized_text}")

    def cleanup(self):
        """Libera recursos se necessário."""
        # pyttsx3 engine doesn't have an explicit close/destroy method exposed easily,
        # but we can stop the loop if running.
        with self._lock:
            try:
                self.engine.stop()
            except:
                pass
        logger.info("TTS Engine cleanup executado.")
        
    def speak_async(self, text: str):
        """
        Versão que não bloqueia o programa.
        Nota: pyttsx3 runAndWait é bloqueante. Para ser verdadeiramente async,
        isso deveria rodar em uma thread separada.
        Nesta implementação otimizada, mantemos o comportamento de bloqueio da thread chamada,
        mas usamos o lock para evitar colisão.
        """
        if not text or not text.strip():
            return

        sanitized_text = self._sanitize_text(text)

        def _speak_thread():
            try:
                engine = pyttsx3.init()
                if self.voice_id:
                    engine.setProperty('voice', self.voice_id)
                engine.setProperty('rate', self.rate)
                engine.setProperty('volume', self.volume)

                engine.say(sanitized_text)

                engine.runAndWait()

            except Exception as e:
                logger.error(f"Erro no speak_async: {e}")

        thread = threading.Thread(target=_speak_thread)
        thread.start()
        with self._lock:
            try:
                self._configure_engine()
                self.engine.say(sanitized_text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"Erro no speak_async: {e}")