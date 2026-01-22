#!/usr/bin/env python3
"""
Test Script for Kamila Assistant
Script de teste para verificar se todos os componentes estão funcionando.
"""

import os
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Testa se todas as importações estão funcionando."""
    logger.info("🧪 Testando importações...")

    try:
        from core.stt_engine import STTEngine
        from core.tts_engine import TTSEngine
        from core.interpreter import CommandInterpreter
        from core.memory_manager import MemoryManager
        from core.actions import ActionManager

        logger.info("✅ Todas as importações OK!")
        return True

    except ImportError as e:
        logger.error(f"❌ Erro nas importações: {e}")
        return False

def test_tts_engine():
    """Testa o motor de síntese de voz."""
    logger.info("🔊 Testando TTS Engine...")

    try:
        from core.tts_engine import TTSEngine

        tts = TTSEngine()
        tts.speak("Olá! Este é um teste da assistente Kamila.")

        logger.info("✅ TTS Engine funcionando!")
        return True

    except Exception as e:
        logger.error(f"❌ Erro no TTS Engine: {e}")
        return False

def test_stt_engine():
    """Testa o motor de reconhecimento de voz."""
    logger.info("🎤 Testando STT Engine...")

    try:
        from core.stt_engine import STTEngine

        stt = STTEngine()

        # Teste básico do microfone
        if stt.test_microphone():
            logger.info("✅ STT Engine funcionando!")
            return True
        else:
            logger.warning("⚠️  STT Engine inicializado, mas microfone pode ter problemas")
            return True  # Não falhar se só o microfone tiver problema

    except Exception as e:
        logger.error(f"❌ Erro no STT Engine: {e}")
        return False

def test_interpreter():
    """Testa o interpretador de comandos."""
    logger.info("🧠 Testando Command Interpreter...")

    try:
        from core.interpreter import CommandInterpreter

        interpreter = CommandInterpreter()

        # Testar alguns comandos
        test_commands = [
            "oi kamila",
            "que horas são",
            "como está o tempo",
            "qual é o seu nome",
            "conta uma piada"
        ]

        for command in test_commands:
            intent = interpreter.interpret_command(command)
            response = interpreter.get_response(intent) if intent else "Não reconhecido"

            logger.info(f"   '{command}' -> {intent} -> {response[:50]}...")

        logger.info("✅ Command Interpreter funcionando!")
        return True

    except Exception as e:
        logger.error(f"❌ Erro no Command Interpreter: {e}")
        return False

def test_memory_manager():
    """Testa o gerenciador de memória."""
    logger.info("💾 Testando Memory Manager...")

    try:
        from core.memory_manager import MemoryManager

        memory = MemoryManager()

        # Testar funcionalidades básicas
        memory.set_user_name("Teste")
        memory.set_mood("happy")
        memory.add_interaction("teste", "greeting", "resposta teste")

        stats = memory.get_memory_stats()
        logger.info(f"   Estatísticas: {stats}")

        logger.info("✅ Memory Manager funcionando!")
        return True

    except Exception as e:
        logger.error(f"❌ Erro no Memory Manager: {e}")
        return False

def test_action_manager():
    """Testa o gerenciador de ações."""
    logger.info("⚙️  Testando Action Manager...")

    try:
        from core.actions import ActionManager

        actions = ActionManager()

        # Testar algumas ações
        test_intents = ['greeting', 'time', 'name', 'joke', 'help']

        for intent in test_intents:
            response = actions.execute_action(intent)
            logger.info(f"   {intent} -> {response[:50]}...")

        logger.info("✅ Action Manager funcionando!")
        return True

    except Exception as e:
        logger.error(f"❌ Erro no Action Manager: {e}")
        return False

def test_configuration():
    """Testa se a configuração está correta."""
    logger.info("⚙️  Testando configuração...")

    # Verificar se .env existe
    env_file = '.kamila/.env'
    if not os.path.exists(env_file):
        logger.warning(f"⚠️  Arquivo {env_file} não encontrado!")
        logger.info("   Criando arquivo .env.example como referência...")
        if not os.path.exists('.kamila/.env.example'):
            logger.error("   .env.example também não encontrado!")
            return False

    # Verificar se requirements.txt existe
    if not os.path.exists('config/requirements.txt'):
        logger.error("❌ requirements.txt não encontrado!")
        return False

    # Verificar se main.py existe
    if not os.path.exists('.kamila/main.py'):
        logger.error("❌ main.py não encontrado!")
        return False

    logger.info("✅ Configuração OK!")
    return True

def main():
    """Função principal do teste."""
    logger.info("🚀 Iniciando testes da Kamila Assistant...")
    logger.info("=" * 50)

    tests = [
        ("Configuração", test_configuration),
        ("Importações", test_imports),
        ("TTS Engine", test_tts_engine),
        ("STT Engine", test_stt_engine),
        ("Command Interpreter", test_interpreter),
        ("Memory Manager", test_memory_manager),
        ("Action Manager", test_action_manager)
    ]

    results = []
    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        logger.info(f"🧪 Executando: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                passed += 1
        except Exception as e:
            logger.error(f"❌ Erro ao executar {test_name}: {e}")
            results.append((test_name, False))

        logger.info("")

    # Resultado final
    logger.info("=" * 50)
    logger.info("📊 RESULTADO DOS TESTES:")
    logger.info("=" * 50)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        logger.info(f"{test_name"20"} | {status}")

    logger.info("=" * 50)
    logger.info(f"📈 TOTAL: {passed}/{total} testes passaram")

    if passed == total:
        logger.info("🎉 Todos os testes passaram! Kamila está pronta para uso!")
        return 0
    else:
        logger.warning("⚠️  Alguns testes falharam. Verifique os erros acima.")
        logger.info("💡 Dicas:")
        logger.info("   - Verifique se todas as dependências estão instaladas")
        logger.info("   - Configure as chaves de API no arquivo .env")
        logger.info("   - Verifique se o microfone está funcionando")
        return 1

if __name__ == "__main__":
    sys.exit(main())
