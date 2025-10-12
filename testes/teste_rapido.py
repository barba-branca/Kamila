#!/usr/bin/env python3
"""
Teste Rápido do Projeto Kamila
Verifica se todos os arquivos estão presentes.
"""

import os

def main():
    print("🚀 TESTE RÁPIDO DO PROJETO KAMILA")
    print("=" * 50)

    # Lista de arquivos essenciais
    arquivos_essenciais = [
        ".kamila/main.py",
        ".kamila/main_with_llm.py",
        ".kamila/core/stt_engine.py",
        ".kamila/core/tts_engine.py",
        ".kamila/core/interpreter.py",
        ".kamila/core/memory_manager.py",
        ".kamila/core/actions.py",
        ".kamila/llm/gemini_engine.py",
        ".kamila/llm/ai_studio_integration.py",
        "testes/test_llm_modules.py",  # Movido para pasta testes
        "config/requirements.txt",
        "data/memory.json",
        "docs/README.md"
    ]

    encontrados = 0
    total = len(arquivos_essenciais)

    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print("✅ " + arquivo)
            encontrados += 1
        else:
            print("❌ " + arquivo)

    print("=" * 50)
    print("RESULTADO: " + str(encontrados) + "/" + str(total) + " arquivos encontrados")

    if encontrados == total:
        print("🎉 PROJETO KAMILA 100% RECUPERADO!")
        print("✅ Todos os arquivos essenciais estão presentes!")
        return 0
    else:
        print("⚠️  Alguns arquivos podem estar faltando.")
        return 1

if __name__ == "__main__":
    exit(main())
