import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai. GenerativeModel("gemini-pro")

def responder_gemini(prompt: str) -> str:
    try:
        resposta = model.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e: 
        logging.error(f"[Gemini] Erro ao gerar a resposta:{e}")
        return "Desculpe, houve um erro em pensar sobre isso." 