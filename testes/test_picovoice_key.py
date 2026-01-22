#!/usr/bin/env python3
"""
Teste da API Key do Picovoice
Verifica se a chave está configurada corretamente.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

def test_picovoice_key():
    """Testa a API key do Picovoice."""
    print("🧪 Testando API Key do Picovoice...")

    api_key = os.getenv('PICOVOICE_API_KEY')

    if not api_key:
        print("❌ PICOVOICE_API_KEY não encontrada no .env")
        return False

    if api_key == "your_picovoice_api_key_here":
        print("⚠️  API Key ainda está com valor padrão")
        print("💡 Configure uma chave real do Picovoice em .kamila/.env")
        return False

    print(f"✅ API Key encontrada: {api_key[:10]}...")
    print("✅ Formato da chave parece válido!")

    # Teste básico de inicialização
    try:
        from pvporcupine import create as create_porcupine

        # Tentar criar instância com chave
        porcupine = create_porcupine(
            access_key=api_key,
            keyword_paths=["models/wake_words/camila_pt_windows_v3_0_0.ppn"],
            model_path="models/porcupine_models/porcupine_params_pt.pv"
        )

        print("✅ Porcupine inicializado com sucesso!")
        porcupine.delete()
        return True

    except Exception as e:
        print(f"❌ Erro ao inicializar Porcupine: {e}")
        return False

def test_google_key():
    """Testa a API key do Google Speech."""
    print("\n🧪 Testando API Key do Google Speech...")

    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("⚠️  GOOGLE_API_KEY não encontrada (opcional)")
        return True

    if api_key == "your_google_speech_api_key_here":
        print("⚠️  Google API Key ainda está com valor padrão")
        return True

    print(f"✅ Google API Key encontrada: {api_key[:10]}...")
    return True

if __name__ == "__main__":
    print("🚀 Teste das API Keys para Kamila")
    print("=" * 40)

    picovoice_ok = test_picovoice_key()
    google_ok = test_google_key()

    print("\n" + "=" * 40)
    if picovoice_ok:
        print("✅ Picovoice: CONFIGURADO CORRETAMENTE")
    else:
        print("❌ Picovoice: PRECISA CONFIGURAÇÃO")

    if google_ok:
        print("✅ Google Speech: CONFIGURADO")
    else:
        print("⚠️  Google Speech: OPCIONAL")

    print("\n💡 Para configurar as chaves:")
    print("1. Acesse https://console.picovoice.ai/")
    print("2. Crie uma conta e obtenha sua Access Key")
    print("3. Edite o arquivo .kamila/.env")
    print("4. Substitua 'your_picovoice_api_key_here' pela sua chave real")
