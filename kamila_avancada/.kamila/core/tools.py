# Mapeia ACTION_MAP para um schema de ferramentas p/ Gemini
from core import actions

def build_tools_spec():
    # Especificação simples: cada ação recebe "params" (objeto livre)
    # Você pode detalhar parâmetros depois (tipo, required, etc.)
    return [
        {
          "name": "get_time",
          "description": "Diz a hora atual.",
          "parameters": {
              "type": "object",
              "properties": {},
              "required": []
          }
        },
        {
          "name": "get_weather",
          "description": "Mostra previsão do tempo para uma cidade.",
          "parameters": {
              "type": "object",
              "properties": {
                  "location": {"type":"string","description":"Cidade, ex: Goiânia"}
              }
          }
        },
        {
          "name": "unknown",
          "description": "Usado quando não há intenção reconhecida.",
          "parameters": {"type":"object","properties":{}}
        }
    ]

def call_tool(name: str, args: dict):
    # Encaminha para suas funções reais em actions.py
    fn = actions.ACTION_MAP.get(name) or actions.unknown_intent
    return fn(args or {})
