

from typing import List
from .embedding_store import EmbeddingStore

class Retriever:
    """
    Responsável por recuperar memórias relevantes da base de embeddings.
    """
    def __init__(self, embedding_store: EmbeddingStore):
        self.store = embedding_store

    def retrieve_relevant_memories(self, current_input: str, n_memories: int = 3) -> List[str]:
        """
        Busca memórias semanticamente relevantes para a entrada atual do usuário.
        """
        print(f"[Retriever] Buscando memórias relevantes para: '{current_input[:50]}...'")
        memories = self.store.search_memories(query_text=current_input, n_results=n_memories)
        if memories:
            print(f"[Retriever] Memórias encontradas: {memories}")
        return memories