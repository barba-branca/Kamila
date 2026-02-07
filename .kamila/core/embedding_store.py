

import sys
import os
from datetime import datetime
from typing import List, Dict, Any
import chromadb

# Adiciona a pasta raiz ao path para encontrar a pasta 'kamila_ia_models'
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from kamila_ia_models.llm_interface import LLMInterface

class EmbeddingStore:
    """
    Gerencia o armazenamento e a busca de memórias de longo prazo usando embeddings vetoriais.
    """
    def __init__(self, llm_interface: LLMInterface, collection_name="kamila_memories"):
        self.llm = llm_interface
        # Modificado para PersistentClient para garantir que a memória persista entre sessões
        db_path = os.path.join(project_root, '.kamila', 'kamila_memory_db')
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"ChromaDB: Coleção '{collection_name}' carregada (Persistente em {db_path}) com {self.collection.count()} itens.")

    def add_memory(self, text: str, metadata: Dict[str, Any]):
        embedding = self.llm.create_embedding(text)
        if not embedding:
            return
            
        memory_id = f"mem_{datetime.now().timestamp()}_{len(text)}"
        metadata['timestamp'] = datetime.now().isoformat()
        
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id]
        )
        print(f"[Memória Longo Prazo] Fato novo salvo: '{text}'")

    def add_memories(self, texts: List[str], metadatas: List[Dict[str, Any]]):
        if not texts:
            return

        embeddings = self.llm.create_embeddings_batch(texts)
        if not embeddings:
            return

        current_time = datetime.now()
        ids = []
        final_metadatas = []

        for i, text in enumerate(texts):
            # Using loop index to ensure uniqueness if timestamp is same
            memory_id = f"mem_{current_time.timestamp()}_{len(text)}_{i}"
            meta = metadatas[i].copy()
            meta['timestamp'] = current_time.isoformat()
            final_metadatas.append(meta)
            ids.append(memory_id)

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=final_metadatas,
            ids=ids
        )
        for text in texts:
             print(f"[Memória Longo Prazo] Fato novo salvo: '{text}'")

    def search_memories(self, query_text: str, n_results: int = 3) -> List[str]:
        if self.collection.count() == 0:
            return []

        query_embedding = self.llm.create_embedding(query_text)
        if not query_embedding:
            return []
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results['documents'][0] if results.get('documents') else []