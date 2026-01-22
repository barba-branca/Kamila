# teste_memoria.py

import os
import sys
from dotenv import load_dotenv

# --- INÍCIO DA CORREÇÃO DE IMPORT ---
# Pega o caminho absoluto da pasta onde este script está (a raiz do projeto)
project_root = os.path.dirname(os.path.abspath(__file__))

# Adiciona a pasta raiz E a pasta '.kamila' ao path do Python
# Isso garante que qualquer import funcione de qualquer lugar
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, '.kamila'))
# --- FIM DA CORREÇÃO DE IMPORT ---

from kamila_ia_models.llm_interface import LLMInterface
from core.memory_manager import MemoryManager

def main():
    """Simula uma conversa com a Kamila para demonstrar a memória."""
    load_dotenv()
    
    print("--- INICIANDO TESTE DO NOVO SISTEMA DE MEMÓRIA DA KAMILA ---")
    
    try:
        llm_interface = LLMInterface()
        memory_manager = MemoryManager(llm_interface)
        print("\n[SISTEMA]: Memória inteligente inicializada.")
    except ValueError as e:
        print(f"\n[ERRO]: {e}")
        print("[SISTEMA]: Verifique se seu arquivo .env está na pasta raiz e contém a GOOGLE_AI_API_KEY.")
        return

    conversation = [
        "Oi, tudo bem?",
        "Meu nome é Kauê.",
        "Eu adoro falar sobre tecnologia e inteligência artificial.",
        "Você lembra qual assunto eu mais gosto de conversar?",
        "E qual é o meu nome mesmo?",
    ]
    
    for turn in conversation:
        print("\n" + "="*50)
        print(f"Você: {turn}")
        
        response = memory_manager.process_interaction(turn)
        
        print(f"Kamila: {response}")
        
    print("\n" + "="*50)
    print("--- TESTE FINALIZADO ---")

if __name__ == "__main__":
    main()