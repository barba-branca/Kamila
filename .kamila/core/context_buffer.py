

from collections import deque
from typing import List, Dict, Any

class ContextBuffer:
    """
    Gerencia a memória de curto prazo (buffer de contexto).
    Armazena as últimas N interações da conversa atual.
    """
    def __init__(self, size: int = 10):
        self.buffer = deque(maxlen=size)

    def add_interaction(self, user_input: str, assistant_response: str):
        interaction = {"user": user_input, "assistant": assistant_response}
        self.buffer.append(interaction)

    def get_recent_context(self) -> str:
        if not self.buffer:
            return "Nenhuma conversa recente."
        
        formatted_context = ""
        for interaction in self.buffer:
            formatted_context += f"Usuário: {interaction['user']}\n"
            formatted_context += f"Kamila: {interaction['assistant']}\n"
        return formatted_context.strip()

    def clear(self):
        self.buffer.clear()