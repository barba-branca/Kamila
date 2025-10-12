#!/usr/bin/env python3
"""
Teste simples para verificar se Kamila está falando
"""

import sys
import os

# Adicionar o diretório .kamila ao path
sys.path.append('.kamila')

from core.tts_engine import TTSEngine

def test_kamila_voice():
    """Testa se Kamila está falando corretamente."""
    print("🗣️  Testando voz de Kamila...")

    try:
        # Inicializar TTS
        tts = TTSEngine()

        # Testar diferentes tipos de resposta
        test_messages = [
            "Olá! Estou acordada e pronta para ajudar!",
            "Bom dia! Como posso ajudar?",
            "Agora são 14:30",
            "Hoje é segunda-feira, 20 de janeiro de 2025",
            "Desculpe, não entendi esse comando. Pode repetir?",
            "Até logo! Me chame quando precisar."
        ]

        print("🎤 Kamila vai falar as seguintes mensagens:")
        for i, message in enumerate(test_messages, 1):
            print(f"{i}. {message}")

        print("\n🎵 Ouvindo Kamila falar...")
        for message in test_messages:
            tts.speak(message)

        print("✅ Teste concluído! Kamila está falando normalmente.")
        tts.cleanup()

    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

    return True

if __name__ == "__main__":
    test_kamila_voice()
