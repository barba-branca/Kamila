import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega o arquivo .env da pasta raiz
load_dotenv()

# Pega a chave do Gemini AI do seu arquivo .env
api_key = os.getenv('GOOGLE_AI_API_KEY')

if not api_key:
    print("ERRO: A chave 'GOOGLE_AI_API_KEY' não foi encontrada no seu arquivo .env!")
else:
    try:
        genai.configure(api_key=api_key)

        print("Conectado ao Google AI. Modelos disponíveis para sua chave:\n")
        
        # Lista todos os modelos disponíveis para você
        for m in genai.list_models():
            # Verifica se o modelo suporta a função que precisamos ("generateContent")
            if 'generateContent' in m.supported_generation_methods:
                print(f"-> {m.name}")
        
        print("\nINSTRUÇÃO: Copie um dos nomes acima (ex: 'models/gemini-1.0-pro') e cole no arquivo 'gemini_engine.py'.")

    except Exception as e:
        print(f"Ocorreu um erro ao tentar conectar com a API do Google: {e}")