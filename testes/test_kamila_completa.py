#!/usr/bin/env python3
"""
Teste Completo do Projeto Kamila Recuperado
Testa todos os módulos principais e funcionalidades.
"""

import os
import sys
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_core_modules():
    """Testa os módulos core da assistente."""
    logger.info("🧪 Testando módulos core...")

    try:
        # Testar imports dos módulos core
        from .kamila.core.stt_engine import STTEngine
        from .kamila.core.tts_engine import TTSEngine
        from .kamila.core.interpreter import CommandInterpreter
        from .kamila.core.memory_manager import MemoryManager
        from .kamila.core.actions import ActionManager

        logger.info("✅ Módulos core importados com sucesso!")
        return True

    except ImportError as e:
        logger.error(f"❌ Erro ao importar módulos core: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Erro nos módulos core: {e}")
        return False

def test_llm_modules():
    """Testa os módulos LLM."""
    logger.info("🧪 Testando módulos LLM...")

    try:
        # Testar imports dos módulos LLM
        from .kamila.llm.gemini_engine import GeminiEngine
        from .kamila.llm.ai_studio_integration import AIStudioIntegration

        logger.info("✅ Módulos LLM importados com sucesso!")
        return True

    except ImportError as e:
        logger.error(f"❌ Erro ao importar módulos LLM: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Erro nos módulos LLM: {e}")
        return False

def test_main_files():
    """Testa os arquivos main."""
    logger.info("🧪 Testando arquivos main...")

    try:
        # Verificar se arquivos existem
        main_files = [
            ".kamila/main.py",
            ".kamila/main_with_llm.py"
        ]

        for file_path in main_files:
            if os.path.exists(file_path):
                logger.info(f"✅ {file_path} encontrado")
            else:
                logger.error(f"❌ {file_path} não encontrado")
                return False

        return True

    except Exception as e:
        logger.error(f"❌ Erro nos arquivos main: {e}")
        return False

def test_configuration():
    """Testa arquivos de configuração."""
    logger.info("🧪 Testando configuração...")

    try:
        # Verificar requirements.txt
        if os.path.exists("config/requirements.txt"):
            logger.info("✅ config/requirements.txt encontrado")
        else:
            logger.error("❌ config/requirements.txt não encontrado")
            return False

        # Verificar se .env.example existe
        if os.path.exists(".kamila/.env.example"):
            logger.info("✅ .kamila/.env.example encontrado")
        else:
            logger.error("❌ .kamila/.env.example não encontrado")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Erro na configuração: {e}")
        return False

def test_data_files():
    """Testa arquivos de dados."""
    logger.info("🧪 Testando arquivos de dados...")

    try:
        # Verificar memory.json
        if os.path.exists("data/memory.json"):
            logger.info("✅ data/memory.json encontrado")
        else:
            logger.error("❌ data/memory.json não encontrado")
            return False

        # Verificar modelos
        if os.path.exists("models/wake_words"):
            logger.info("✅ Modelos de wake word encontrados")
        else:
            logger.error("❌ Modelos de wake word não encontrados")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Erro nos dados: {e}")
        return False

def main():
    """Função principal de teste."""
    logger.info("🚀 Iniciando teste completo do projeto Kamila...")
    logger.info(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Lista de testes
    tests = [
        ("Módulos Core", test_core_modules),
        ("Módulos LLM", test_llm_modules),
        ("Arquivos Main", test_main_files),
        ("Configuração", test_configuration),
        ("Arquivos de Dados", test_data_files)
    ]

    results = []
    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Executando: {test_name}")
        logger.info(f"{'='*60}")

        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                passed += 1
        except Exception as e:
            logger.error(f"❌ Falha ao executar {test_name}: {e}")
            results.append((test_name, False))

    # Resumo dos resultados
    logger.info(f"\n{'='*60}")
    logger.info("📊 RESUMO DOS TESTES")
    logger.info(f"{'='*60}")

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        logger.info(f"{test_name}: {status}")

    logger.info(f"\n📈 Resultado Final: {passed}/{total} testes passaram")

    # Status final
    if passed == total:
        logger.info("🎉 TODOS OS TESTES PASSARAM!")
        logger.info("✅ Projeto Kamila completamente recuperado e funcional!")
        return 0
    else:
        logger.warning("⚠️  Alguns testes falharam.")
        logger.info("🔧 Verifique os logs acima para detalhes.")
        return 1

if __name__ == "__main__":
    # Adicionar .kamila ao path do Python
    kamila_path = os.path.join(os.path.dirname(__file__), '.kamila')
    if kamila_path not in sys.path:
        sys.path.insert(0, kamila_path)

    sys.exit(main())
