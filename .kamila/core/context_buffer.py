

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
        
        context_parts = []
        for interaction in self.buffer:
            context_parts.append(f"Usuário: {interaction['user']}\n")
            context_parts.append(f"Kamila: {interaction['assistant']}\n")
        return "".join(context_parts).strip()

    def clear(self):
        self.buffer.clear()