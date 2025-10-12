#!/usr/bin/env python3
"""
Teste direto da fala da Kamila sem wake word
"""

import sys
import os

# Adicionar o diretório .kamila ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.kamila'))

try:
    print("Testando fala direta da Kamila...")

    from main import KamilaAssistant

    # Inicializar Kamila
    kamila = KamilaAssistant()
    print("✓ Kamila inicializada")

    # Simular uma saudação direta
    print("Testando saudação...")
    kamila.tts_engine.speak("Olá! Eu sou a Kamila e estou funcionando!")

    # Testar o método greet_user diretamente
    print("Testando método greet_user...")
    kamila.greet_user()

    # Testar processamento de comando de nome
    print("Testando processamento de nome...")
    kamila.process_command("Meu nome é João")

    print("Teste de fala concluído!")

except Exception as e:
    print(f"Erro no teste: {e}")
    import traceback
    traceback.print_exc()
