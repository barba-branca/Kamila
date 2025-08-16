import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY   = os.getenv("GOOGLE_API_KEY")
GEMINI_PRIMARY   = os.getenv("GEMINI_PRIMARY", "gemini-2.5-flash")
GEMINI_FALLBACK  = os.getenv("GEMINI_FALLBACK", "gemini-2.5-pro")
KAMILA_NAME      = os.getenv("KAMILA_NAME", "Kamila")
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "São Paulo")

SYSTEM_RULES = f"""
Você é a assistente {KAMILA_NAME}. Fale português do Brasil, voz amigável e objetiva.
Use FERRAMENTAS quando precisar executar ações no sistema do usuário.
Se a intenção do usuário não for clara, faça perguntas curtas de esclarecimento.
Nunca invente dados. Se não souber, diga que não sabe e proponha como descobrir.
"""
