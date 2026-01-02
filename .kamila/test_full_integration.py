#!/usr/bin/env python3
"""
Teste de Integração Completa - Kamila
Testa o loop completo: STT → Interpretação → Ações → TTS → LLM
"""

import sys
import os
import time
import logging

# Adicionar o diretório .kamila ao path
sys.path.insert(0, os.path.dirname(__file__))

from core.stt_engine import STTEngine
from core.tts_engine import TTSEngine
from core.interpreter import CommandInterpreter
from core.memory_manager import MemoryManager
from core.actions import ActionManager
from llm.gemini_engine import GeminiEngine

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_stt_only():
    """Testa apenas STT."""
    print("🗣️  Testando STT Engine...")
    stt = STTEngine()
    print("Diga algo (3 segundos)...")
    command = stt.listen_for_command(timeout=3)
    print(f"Comando reconhecido: {command}")
    stt.cleanup()
    return command is not None

def test_tts_only():
    """Testa apenas TTS."""
    print("🔊 Testando TTS Engine...")
    tts = TTSEngine()
    tts.speak("Olá! Teste de voz funcionando!")
    tts.cleanup()
    return True

def test_interpreter_only():
    """Testa apenas interpretação."""
    print("🧠 Testando Interpreter...")
    interpreter = CommandInterpreter()
    test_commands = [
        "que horas são",
        "como você está",
        "ligar luz",
        "tocar música",
        "comando inexistente"
    ]
    for cmd in test_commands:
        intent = interpreter.interpret_command(cmd)
        print(f"Comando: '{cmd}' → Intenção: {intent}")
    return True

def test_actions_only():
    """Testa apenas ações."""
    print("⚡ Testando Actions...")
    tts = TTSEngine()
    actions = ActionManager(tts)
    test_commands = [
        ("que horas são", "time"),
        ("como você está", "status"),
        ("comando teste", None)
    ]
    for cmd, expected_intent in test_commands:
        response = actions.execute_action(expected_intent, cmd)
        print(f"Ação: '{cmd}' → Resposta: {response}")
    tts.cleanup()
    return True

def test_gemini_only():
    """Testa apenas Gemini."""
    print("🤖 Testando Gemini Engine...")
    gemini = GeminiEngine()
    response = gemini.chat("Olá, como você está?")
    print(f"Gemini resposta: {response}")
    gemini.cleanup()
    return response is not None

def test_full_pipeline():
    """Testa o pipeline completo."""
    print("🔄 Testando Pipeline Completo...")

    # Inicializar componentes
    stt = STTEngine()
    tts = TTSEngine()
    interpreter = CommandInterpreter()
    memory = MemoryManager()
    actions = ActionManager(tts)
    gemini = GeminiEngine()

    # Simular comando (já que não podemos falar em teste)
    test_command = "que horas são"

    print(f"Simulando comando: '{test_command}'")

    # Pipeline completo
    try:
        # 1. Interpretação
        intent = interpreter.interpret_command(test_command)
        print(f"1. Intenção identificada: {intent}")

        # 2. Ação
        if intent:
            response = actions.execute_action(intent, test_command)
            print(f"2. Resposta da ação: {response}")
        else:
            response = None
            print("2. Nenhuma intenção identificada")

        # 3. Se não há resposta, usar Gemini
        if not response:
            context = {
                'user_name': memory.get_user_name(),
                'current_time': time.strftime("%H:%M"),
                'assistant_name': 'Kamila'
            }
            ai_response = gemini.chat(test_command, context)
            print(f"3. Resposta do Gemini: {ai_response}")
            response = ai_response

        # 4. TTS (simulado)
        if response:
            print(f"4. TTS falaria: '{response}'")
            # tts.speak(response)  # Comentado para não falar durante teste

        # 5. Memória
        memory.add_interaction(test_command, intent or "unknown", response or "no response")
        print("5. Interação salva na memória")

        success = True

    except Exception as e:
        print(f"Erro no pipeline: {e}")
        success = False

    # Limpar
    stt.cleanup()
    tts.cleanup()
    gemini.cleanup()

    return success

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando Testes de Integração Completa - Kamila\n")

    tests = [
        ("STT Only", test_stt_only),
        ("TTS Only", test_tts_only),
        ("Interpreter Only", test_interpreter_only),
        ("Actions Only", test_actions_only),
        ("Gemini Only", test_gemini_only),
        ("Full Pipeline", test_full_pipeline)
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{'='*50}")
        try:
            result = test_func()
            results.append((name, result))
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"{name}: {status}")
        except Exception as e:
            print(f"{name}: ❌ ERRO - {e}")
            results.append((name, False))

    print(f"\n{'='*50}")
    print("📊 RESULTADOS FINAIS:")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Total: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 Todos os testes passaram! Integração completa funcionando.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")

    print("\n💡 Para testar a assistente completa:")
    print("   python .kamila/main.py")
    print("   Diga 'kamila' + seu comando (ex: 'kamila, que horas são')")

if __name__ == "__main__":
    main()
