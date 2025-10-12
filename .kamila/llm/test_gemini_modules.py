#!/usr/bin/env python3
"""
Teste dos Módulos Gemini e AI Studio
Testa a integração com Google Gemini AI e AI Studio.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_gemini_engine():
    """Testa o motor Gemini."""
    logger.info(" Testando Gemini Engine...")

    try:
        from core.gemini_engine import GeminiEngine

        # Inicializar engine
        gemini = GeminiEngine()

        # Testar informações do modelo
        model_info = gemini.get_model_info()
        logger.info(f" Informações do modelo: {model_info}")

        # Testar respostas simuladas
        test_messages = [
            "Olá! Como você está?",
            "Que horas são?",
            "Conta uma piada",
            "Obrigado pela ajuda!"
        ]

        for message in test_messages:
            logger.info(f"  Teste: {message}")
            response = gemini.chat(message)
            logger.info(f" Resposta: {response[:100]}...")
            logger.info("-" * 50)

        logger.info(" Teste do Gemini Engine concluído!")

    except Exception as e:
        logger.error(f" Erro no teste do Gemini Engine: {e}")
        return False

    return True

def test_ai_studio_integration():
    """Testa a integração com AI Studio."""
    logger.info(" Testando AI Studio Integration...")

    try:
        from core.ai_studio_integration import AIStudioIntegration

        # Inicializar integração
        ai_studio = AIStudioIntegration()

        # Testar modelos disponíveis
        models = ai_studio.get_available_models()
        logger.info(f" Modelos disponíveis: {models}")

        # Testar geração de texto
        test_prompts = [
            "Olá! Como você está?",
            "Que horas são?",
            "Conta uma piada sobre programação"
        ]

        for prompt in test_prompts:
            logger.info(f"  Teste: {prompt}")
            response = ai_studio.generate_text(prompt)
            logger.info(f" Resposta: {response[:100]}...")
            logger.info("-" * 50)

        # Testar análise de sentimento
        sentiment_test = "Estou muito feliz hoje!"
        sentiment = ai_studio.analyze_sentiment(sentiment_test)
        logger.info(f" Análise de sentimento: {sentiment}")

        logger.info(" Teste da AI Studio Integration concluído!")

    except Exception as e:
        logger.error(f" Erro no teste da AI Studio Integration: {e}")
        return False

    return True

def test_combined_integration():
    """Testa integração combinada dos módulos."""
    logger.info(" Testando integração combinada...")

    try:
        from core.gemini_engine import GeminiEngine
        from core.ai_studio_integration import AIStudioIntegration

        # Inicializar ambos os motores
        gemini = GeminiEngine()
        ai_studio = AIStudioIntegration()

        # Testar se ambos funcionam
        gemini_response = gemini.chat("Olá! Como você está?")
        ai_response = ai_studio.generate_text("Olá! Como você está?")

        logger.info(f" Gemini: {gemini_response[:50]}...")
        logger.info(f" AI Studio: {ai_response[:50]}...")

        logger.info(" Teste de integração combinada concluído!")

    except Exception as e:
        logger.error(f" Erro no teste de integração combinada: {e}")
        return False

    return True

def main():
    """Função principal de teste."""
    logger.info(" Iniciando testes dos módulos Gemini...")

    # Carregar variáveis de ambiente
    load_dotenv('.kamila/.env')

    # Verificar se API key está configurada
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if api_key:
        logger.info(" API Key do Google AI configurada")
    else:
        logger.warning("  API Key do Google AI não configurada - usando modo simulado")

    # Executar testes
    tests = [
        ("Gemini Engine", test_gemini_engine),
        ("AI Studio Integration", test_ai_studio_integration),
        ("Combined Integration", test_combined_integration)
    ]

    results = []

    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Executando: {test_name}")
        logger.info(f"{'='*60}")

        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ Falha ao executar {test_name}: {e}")
            results.append((test_name, False))

    # Resumo dos resultados
    logger.info(f"\n{'='*60}")
    logger.info(" RESUMO DOS TESTES")
    logger.info(f"{'='*60}")

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = " PASSOU" if result else "❌ FALHOU"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1

    logger.info(f"\n Resultado Final: {passed}/{total} testes passaram")

    if passed == total:
        logger.info(" Todos os testes passaram! Módulos Gemini funcionando perfeitamente.")
        return 0
    else:
        logger.warning("  Alguns testes falharam. Verifique a configuração e logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
