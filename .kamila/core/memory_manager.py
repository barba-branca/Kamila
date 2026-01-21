# .kamila/core/memory_manager.py

import sys
import os
import re

# --- INÍCIO DA CORREÇÃO DE IMPORT ---
# Pega o caminho do diretório 'core'
core_dir = os.path.dirname(os.path.abspath(__file__))
# Pega o caminho do diretório '.kamila' (um nível acima)
kamila_dir = os.path.dirname(core_dir)
# Pega o caminho da raiz do projeto (um nível acima de '.kamila')
project_root = os.path.dirname(kamila_dir)
# Adiciona a pasta raiz ao path
sys.path.insert(0, project_root)
# --- FIM DA CORREÇÃO DE IMPORT ---

from kamila_ia_models.llm_interface import LLMInterface
from .context_buffer import ContextBuffer
from .embedding_store import EmbeddingStore
from .retriever import Retriever
from .memory_updater import MemoryUpdater

class MemoryManager:
    """
    Orquestrador central de todos os sistemas de memória.
    """
    def __init__(self, llm_interface: LLMInterface, user_name: str = "usuário"):
        self.llm = llm_interface
        self.user_name = user_name
        self.buffer = ContextBuffer(size=8)
        self.store = EmbeddingStore(llm_interface)
        self.retriever = Retriever(self.store)
        self.updater = MemoryUpdater(self.store)

    def process_interaction(self, user_input: str):
        relevant_memories = self.retriever.retrieve_relevant_memories(user_input)
        recent_context = self.buffer.get_recent_context()
        
        prompt = self._build_prompt(user_input, recent_context, relevant_memories)
        
        print("\n[PROMPT ENVIADO PARA A IA]:\n---")
        print(prompt)
        print("---\n")
        
        assistant_response = self.llm.generate_response(prompt)
        
        self.buffer.add_interaction(user_input, assistant_response)
        self.updater.process_and_save_facts(user_input)
        
        match = self.updater.fact_patterns["name"].search(user_input)
        if match:
            name = next((g for g in match.groups() if g is not None), None)
            if name:
                self.user_name = name.strip().capitalize()
                print(f"[Memory Manager] Nome de usuário atualizado para: {self.user_name}")

        return assistant_response

    def add_health_event(self, event_type: str, details: dict):
        """
        Adiciona um evento de saúde à memória e processa como um fato importante.
        """
        import json
        from datetime import datetime

        timestamp = datetime.now().isoformat()
        event_description = f"Evento de Saúde ({event_type}): {json.dumps(details, ensure_ascii=False)}"

        print(f"[Memory Manager] Registrando evento de saúde: {event_description}")

        # Salva como um fato na memória de longo prazo
        self.store.add_memory(event_description)

        # Adiciona ao buffer de contexto imediato para que a IA saiba o que acabou de acontecer
        self.buffer.add_interaction(f"[SISTEMA] Registro de evento: {event_type}", f"Entendido. Registrei: {details}")

    def _build_prompt(self, user_input, recent_context, relevant_memories):
        prompt = f"""Você é Kamila, uma assistente de IA amigável e empática conversando com '{self.user_name}'.

---
Lembranças Relevantes do Passado (use-as se fizerem sentido para a conversa):
"""
        if relevant_memories:
            for mem in relevant_memories:
                prompt += f"- {mem}\n"
        else:
            prompt += "- Nenhuma.\n"
        
        prompt += f"""
---
Contexto da Conversa Atual:
{recent_context}

---
A mensagem mais recente do usuário é:
{self.user_name}: "{user_input}"

Sua resposta (como Kamila):
"""
        return prompt