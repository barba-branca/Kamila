import logging
from tenacity import retry, wait_exponential, stop_after_attempt
import google.generativeai as genai

from core.config import GOOGLE_API_KEY, GEMINI_PRIMARY, GEMINI_FALLBACK, SYSTEM_RULES
from core.tools import build_tools_spec, call_tool

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY ausente no .env")

genai.configure(api_key=GOOGLE_API_KEY)

def _model(name: str):
    # Usa o modelo com tool_use habilitado
    return genai.GenerativeModel(
        model_name=name,
        system_instruction=SYSTEM_RULES,
        tools=[{"function_declarations": build_tools_spec()}]
    )

@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
def _invoke(model_name: str, text: str, context_vars: dict = None):
    model = _model(model_name)
    msgs = []
    if context_vars:
        # Você pode injetar pedaços da memória como "history" no começo
        pass
    return model.generate_content([{"role":"user","parts":[{"text":text}]}], safety_settings=None)

def llm_route_and_execute(user_text: str, context_vars: dict = None) -> str:
    """
    Tenta o Flash primeiro; se vier sem ferramenta apropriada ou baixa confiança,
    tenta o Pro. Executa a ferramenta escolhida e devolve a resposta final em texto.
    """
    for idx, model_name in enumerate([GEMINI_PRIMARY, GEMINI_FALLBACK]):
        logging.info(f"LLM: tentando modelo {model_name} (tentativa {idx+1})")
        resp = _invoke(model_name, user_text, context_vars)
        # ---- Interpretar chamada de ferramenta ----
        # google-generativeai retorna 'function_call' nas partes quando o modelo decide usar ferramenta
        try:
            parts = resp.candidates[0].content.parts
        except Exception:
            parts = []

        tool_calls = [p for p in parts if getattr(p, "function_call", None)]
        if tool_calls:
            # Executa a(s) ferramentas em ordem e retorna a saída da última
            result_text = None
            for call in tool_calls:
                fn_name = call.function_call.name
                args = dict(call.function_call.args or {})
                logging.info(f"LLM -> ferramenta: {fn_name}({args})")
                result_text = call_tool(fn_name, args)
            # Opcional: mandar o resultado de volta ao LLM para formatar a fala final
            # Aqui, vamos simplificar e devolver o texto direto da ferramenta
            return result_text or "Certo."

        # Se o modelo não chamou ferramenta, mas respondeu algo útil, retornamos
        try:
            plain = resp.text
        except Exception:
            plain = None

        if plain and len(plain.strip()) > 0:
            # Heurística: se a resposta contém “não entendi”/“não sei”, sobe p/ Pro
            low_conf = any(x in plain.lower() for x in ["não entendi", "não sei", "não tenho certeza"])
            if low_conf and model_name != GEMINI_FALLBACK:
                continue  # tenta Pro
            return plain

    # Se nada deu certo:
    return "Desculpe, não consegui decidir uma ação. Pode repetir de outra forma?"
