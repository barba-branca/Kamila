#!/usr/bin/env python3
"""
Teste de inicialização da Kamila
"""

import sys
import os

# Adicionar o diretório .kamila ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.kamila'))

try:
    print("Testando inicialização da Kamila...")

    from core.tts_engine import TTSEngine
    from core.memory_manager import MemoryManager

    print("✓ Importações básicas OK")

    # Testar TTS
    print("Testando TTS...")
    tts = TTSEngine()
    tts.speak("Inicialização do teste")
    print("✓ TTS OK")

    # Testar Memory Manager
    print("Testando Memory Manager...")
    memory = MemoryManager()
    print(f"✓ Memory Manager OK - Nome atual: {memory.get_user_name()}")

    # Testar importação da classe principal
    print("Testando importação da KamilaAssistant...")
    from main import KamilaAssistant
    print("✓ KamilaAssistant importada OK")

    # Testar inicialização (sem start)
    print("Testando inicialização da KamilaAssistant...")
    kamila = KamilaAssistant()
    print("✓ KamilaAssistant inicializada OK")

    print("\n🎉 Todos os testes passaram! Kamila está pronta para funcionar.")

except Exception as e:
    print(f"❌ Erro durante teste: {e}")
    import traceback
    traceback.print_exc()
