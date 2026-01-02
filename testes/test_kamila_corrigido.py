#!/usr/bin/env python3
"""
Teste Corrigido do Projeto Kamila Recuperado
Verifica se todos os arquivos estão presentes e organizados.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_file_exists(file_path):
    """Verifica se um arquivo existe."""
    if os.path.exists(file_path):
        return True, f"✅ {file_path} - ENCONTRADO"
    else:
        return False, f"❌ {file_path} - NÃO ENCONTRADO"

def check_directory_structure():
    """Verifica a estrutura de pastas."""
    logger.info("📁 Verificando estrutura de pastas...")

    directories = [
        ".kamila",
        ".kamila/core",
        ".kamila/llm",
        "config",
        "data",
        "docs",
        "models",
        "audio",
        "hardware",
        "logs",
        "scripts",
        "deployment"
    ]

    results = []
    for directory in directories:
        exists = os.path.exists(directory)
        status = "✅" if exists else "❌"
        results.append((directory, exists))
        logger.info(f"{status} {directory}")

    return results

def check_kamila_files():
    """Verifica arquivos da Kamila."""
    logger.info("🤖 Verificando arquivos da Kamila...")

    kamila_files = [
        ".kamila/main.py",
        ".kamila/main_with_llm.py",
        ".kamila/__init__.py",
        ".kamila/.env.example"
    ]

    results = []
    for file_path in kamila_files:
        exists, message = check_file_exists(file_path)
        results.append((file_path, exists))
        logger.info(message)

    return results

def check_core_modules():
    """Verifica módulos core."""
    logger.info("🧠 Verificando módulos core...")

    core_files = [
        ".kamila/core/stt_engine.py",
        ".kamila/core/tts_engine.py",
        ".kamila/core/interpreter.py",
        ".kamila/core/memory_manager.py",
        ".kamila/core/actions.py"
    ]

    results = []
    for file_path in core_files:
        exists, message = check_file_exists(file_path)
        results.append((file_path, exists))
        logger.info(message)

    return results

def check_llm_modules():
    """Verifica módulos LLM."""
    logger.info("🧪 Verificando módulos LLM...")

    llm_files = [
        ".kamila/llm/gemini_engine.py",
        ".kamila/llm/ai_studio_integration.py",
        ".kamila/llm/test_llm_modules.py",
        ".kamila/llm/requirements_gemini.txt",
        ".kamila/llm/README.md",
        ".kamila/llm/__init__.py"
    ]

    results = []
    for file_path in llm_files:
        exists, message = check_file_exists(file_path)
        results.append((file_path, exists))
        logger.info(message)

    return results

def check_config_files():
    """Verifica arquivos de configuração."""
    logger.info("⚙️  Verificando arquivos de configuração...")

    config_files = [
        "config/requirements.txt",
        "data/memory.json",
        "docs/README.md",
        "TODO_LLM_ORGANIZADO.md"
    ]

    results = []
    for file_path in config_files:
        exists, message = check_file_exists(file_path)
        results.append((file_path, exists))
        logger.info(message)

    return results

def check_data_integrity():
    """Verifica integridade dos dados."""
    logger.info("💾 Verificando integridade dos dados...")

    try:
        # Verificar memory.json
        with open("data/memory.json", 'r', encoding='utf-8') as f:
            memory_data = json.load(f)

        logger.info("✅ data/memory.json - JSON válido")
        logger.info(f"   Usuário: {memory_data.get('user_name', 'N/A')}")
        logger.info(f"   Interações: {memory_data.get('interactions', 0)}")
        logger.info(f"   Humor: {memory_data.get('mood', 'N/A')}")

        return True

    except Exception as e:
        logger.error(f"❌ Erro na verificação de dados: {e}")
        return False

def main():
    """Função principal."""
    logger.info("🚀 TESTE CORRIGIDO DO PROJETO KAMILA RECUPERADO")
    logger.info("=" * 60)
    logger.info(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"📂 Diretório: {os.getcwd()}")
    logger.info("=" * 60)

    # Executar verificações
    checks = [
        ("Estrutura de Pastas", check_directory_structure),
        ("Arquivos Kamila", check_kamila_files),
        ("Módulos Core", check_core_modules),
        ("Módulos LLM", check_llm_modules),
        ("Configuração", check_config_files),
        ("Integridade dos Dados", check_data_integrity)
    ]

    total_passed = 0
    total_checks = 0

    for check_name, check_func in checks:
        logger.info(f"\n🔍 {check_name.upper()}")
        logger.info("-" * 40)

        try:
            result = check_func()
            if isinstance(result, list):
                passed = sum(1 for _, exists in result if exists)
                total = len(result)
                total_passed += passed
                total_checks += total
                logger.info(f"📊 Resultado: {passed}/{total} OK")
            elif isinstance(result, bool):
                if result:
                    total_passed += 1
                total_checks += 1
                logger.info("📊 Resultado: ✅ OK" if result else "📊 Resultado: ❌ FALHOU")

        except Exception as e:
            logger.error(f"❌ Erro na verificação: {e}")
            total_checks += 1

    # Resumo final
    logger.info(f"\n{'='*60}")
    logger.info("📊 RESUMO FINAL")
    logger.info(f"{'='*60}")
    logger.info(f"✅ Testes passados: {total_passed}")
    logger.info(f"📋 Total de testes: {total_checks}")
    percentage = (total_passed / total_checks * 100) if total_checks > 0 else 0
    logger.info(f"📈 Porcentagem: {percentage".1f"}%")

    if total_passed == total_checks:
        logger.info("🎉 PROJETO KAMILA 100% RECUPERADO!")
        logger.info("✅ Todos os arquivos e estrutura organizados com sucesso!")
        return 0
    else:
        logger.warning("⚠️  Alguns arquivos podem estar faltando.")
        logger.info("🔧 Verifique os logs acima para detalhes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
