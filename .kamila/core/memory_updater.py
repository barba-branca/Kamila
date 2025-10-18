

import re
from .embedding_store import EmbeddingStore

class MemoryUpdater:
    """
    Analisa a conversa para detectar fatos importantes e os envia para a memória de longo prazo.
    """
    def __init__(self, embedding_store: EmbeddingStore):
        self.store = embedding_store
        
        # Padrões para detectar fatos. Mais complexos e flexíveis.
        self.fact_patterns = {
            "name": re.compile(r"meu nome é (\w+)|pode me chamar de (\w+)|eu sou o? (\w+)", re.IGNORECASE),
            "preference_like": re.compile(r"eu (gosto|adoro|amo) (de|muito de)? (.+)", re.IGNORECASE),
            "preference_dislike": re.compile(r"eu (não gosto|odeio|detesto) (de)? (.+)", re.IGNORECASE),
        }

    def process_and_save_facts(self, user_input: str):
        """
        Verifica a entrada do usuário em busca de fatos e os salva.
        """
        for fact_type, pattern in self.fact_patterns.items():
            match = pattern.search(user_input)
            if match:
                # Pega o conteúdo do grupo de captura que não for vazio
                fact_content = next((g for g in match.groups() if g is not None and "gosto" not in g and "adoro" not in g), None)
                if not fact_content: continue

                fact_content = fact_content.strip()

                if "name" in fact_type:
                    full_fact = f"O nome do usuário é {fact_content}."
                    metadata = {"type": "user_profile", "key": "name"}
                else:
                    full_fact = f"O usuário {fact_type.replace('_', ' ')}: {fact_content}."
                    metadata = {"type": "preference", "content": fact_content}
                
                self.store.add_memory(full_fact, metadata)