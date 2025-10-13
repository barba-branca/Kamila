#!/usr-bin/env python3
"""
TTS Engine - Text-to-Speech para Kamila
Motor de síntese de voz usando pyttsx3.
VERSÃO FINAL ROBUSTA - Cria uma nova instância do motor para cada fala, evitando conflitos de áudio.
"""

import os
import logging
import pyttsx3
from dotenv import load_dotenv
import re

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

logger = logging.getLogger(__name__)

class TTSEngine:
    """Motor de síntese de voz robusto que reinicializa a cada chamada."""

    def __init__(self):
        """Inicializa as configurações do motor TTS, mas não o motor em si."""
        logger.info("Inicializando configurações do TTS Engine...")
        self.voice_id = self._get_portuguese_voice_id()
        self.rate = int(os.getenv('VOICE_RATE', 180))
        self.volume = float(os.getenv('VOICE_VOLUME', 0.9))
        
        if self.voice_id:
            logger.info(f"Voz em Português encontrada e configurada.")
        else:
            logger.warning("Nenhuma voz em Português encontrada. Usará a voz padrão do sistema.")
            
        logger.info(f"Volume: {self.volume}, Velocidade: {self.rate} WPM")
        logger.info("TTS Engine configurado com sucesso!")

    def _get_portuguese_voice_id(self):
        """Busca o ID da voz em português uma única vez."""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.stop() # Libera o motor temporário
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
        """Cria um motor de voz, fala o texto e o destrói."""
        if not text or not text.strip():
            logger.warning("Texto vazio para falar. Ignorando.")
            return

        sanitized_text = self._sanitize_text(text)

        try:
            # --- A MÁGICA ACONTECE AQUI ---
            # 1. Cria um motor de voz novo, limpo.
            engine = pyttsx3.init()

            # 2. Configura-o com as propriedades que guardamos
            if self.voice_id:
                engine.setProperty('voice', self.voice_id)
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            
            logger.info(f"Preparando para falar: '{sanitized_text[:70]}...'")
            
            # 3. Manda falar
            engine.say(sanitized_text)
            
            # 4. Executa e espera
            engine.runAndWait()
            
            # 5. O motor é destruído automaticamente quando a função termina, liberando os recursos de áudio.
            logger.info("Fala concluída com sucesso.")

        except Exception as e:
            logger.error(f"Erro CRÍTICO durante a execução da fala: {e}")
            print(f"Kamila (erro de voz): {sanitized_text}")

    def cleanup(self):
        """Não há mais nada para limpar aqui, mas mantemos a função por compatibilidade."""
        logger.info("TTS Engine não requer limpeza nesta versão.")