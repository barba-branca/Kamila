#!/usr/bin/env python3
"""
Teste simples do TTS Engine
"""

import sys
import os

# Adicionar o diretório .kamila ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.kamila'))

try:
    from core.tts_engine import TTSEngine

    print("Testando TTS Engine...")

    # Inicializar TTS
    tts = TTSEngine()

    # Testar fala
    print("Falando: 'Olá, teste de voz!'")
    tts.speak("Olá, teste de voz!")

    print("TTS testado com sucesso!")

except Exception as e:
    print(f"Erro no teste TTS: {e}")
    import traceback
    traceback.print_exc()
