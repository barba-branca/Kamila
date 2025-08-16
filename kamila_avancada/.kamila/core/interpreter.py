from . import actions
from .gemini_engine import responder_com_gemini
from .gemini_ai import responder_gemini

def interpretar_comando(comando):
    comando = comando.lower()
    
    if "google" in comando:
        actions.abrir_site("https://www.google.com")
        return "Abrindo o Google para você."

    # fallback inteligente com Gemini
    resposta_ia = responder_com_gemini(comando)
    return resposta_ia
