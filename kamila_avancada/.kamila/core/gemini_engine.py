import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def responder_com_gemini(prompt):
    try:
        resposta = model.generate_content(prompt)
        return resposta.text
    except Exception as e:
        return f"Desculpe, houve um erro com a IA: {e}"
