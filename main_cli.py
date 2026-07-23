#!/usr/bin/env python3
"""
Kamila CLI - Interface de Texto para Assistente Pessoal
Desenvolvido com foco em simplicidade, utilidade e memória persistente.
"""

import os
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configuração de Logging
logging.basicConfig(level=logging.ERROR) # Silencia logs de debug para manter CLI limpa
logger = logging.getLogger("KamilaCLI")

# Configuração de Voz
VOICE_ENABLED = True  # Pode ser alterado pelo usuário ou via argumento

def setup_paths():
    """Configura os caminhos para importação dos módulos da Kamila."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    sys.path.insert(0, os.path.join(project_root, '.kamila'))
    return project_root

def print_kamila(text):
    """Imprime a resposta da Kamila de forma formatada."""
    print(f"\n👩‍💻 Kamila: {text}\n")

def speak_kamila(tts_engine, text):
    """Fala a resposta se a voz estiver ativada."""
    if VOICE_ENABLED and tts_engine:
        try:
            tts_engine.speak(text)
        except Exception as e:
            print(f"[Erro de Voz]: {e}")

def main():
    setup_paths()
    load_dotenv()
    
    print("\n" + "="*50)
    print("   KAMILA - ASSISTENTE PESSOAL (CLI v1.0)")
    print("   Modo: Texto | Voz: " + ("Ativado" if VOICE_ENABLED else "Desativado"))
    print("   Digite 'ajuda' para ver comandos ou 'sair' para encerrar.")
    print("="*50 + "\n")

    # Importação tardia para não poluir o startup com logs antes do banner
    try:
        from kamila_ia_models.llm_interface import LLMInterface
        from core.memory_manager import MemoryManager
        from core.tts_engine import TTSEngine
        try:
            from core.action_manager import ActionManager
        except ImportError:
            ActionManager = None
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("Verifique se o ambiente virtual está ativo e as dependências instaladas.")
        return

    # Inicialização dos Sistemas
    print("⏳ Inicializando sistemas...")
    
    try:
        llm_interface = LLMInterface()
        memory_manager = MemoryManager(llm_interface)
        
        tts_engine = None
        if VOICE_ENABLED:
            tts_engine = TTSEngine()
            
        print("✅ Kamila pronta! Pode falar comigo.")
        
    except Exception as e:
        print(f"❌ Falha na inicialização: {e}")
        return

    # Loop Principal
    while True:
        try:
            user_input = input("👤 Você: ").strip()
            
            if not user_input:
                continue
                
            command = user_input.lower()
            
            # --- Comandos de Sistema ---
            if command in ['sair', 'tchau', 'encerrar', 'quit', 'exit']:
                response = "Até mais! Focada e disciplinada. Tchau!"
                print_kamila(response)
                speak_kamila(tts_engine, response)
                break
                
            elif command == 'limpar':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("--- Tela Limpa ---")
                continue

            # --- Fluxos Específicos (Diário, Hábitos, Lembretes) ---
            
            # 1. DIÁRIO
            if "registra meu dia" in command or "registrar meu dia" in command:
                handle_diary(memory_manager, tts_engine)
                continue
                
            # 2. HÁBITOS (Criação)
            if command.startswith("novo hábito:") or command.startswith("novo habito:"):
                habit_name = command.split(":", 1)[1].strip()
                if habit_name:
                    memory_manager.store.add_memory(
                        f"O usuário criou um novo hábito: {habit_name}",
                        {"type": "habit_definition", "name": habit_name, "created_at": datetime.now().isoformat()}
                    )
                    response = f"Hábito '{habit_name}' registrado. A consistência é a chave. Vou te cobrar."
                    print_kamila(response)
                    speak_kamila(tts_engine, response)
                else:
                    print_kamila("Qual o nome do hábito? Diga 'Novo hábito: ler livros'.")
                continue
                
            # 3. HÁBITOS (Check)
            if command.startswith("fiz ") or command.startswith("concluí "):
                habit_done = command.replace("fiz ", "").replace("concluí ", "").strip()
                memory_manager.store.add_memory(
                    f"O usuário completou o hábito: {habit_done}",
                    {"type": "habit_log", "name": habit_done, "status": "completed"}
                )
                response = f"Boa! Mais um dia vencido com '{habit_done}'. Continue assim."
                print_kamila(response)
                speak_kamila(tts_engine, response)
                continue
                
            # 4. LEMBRETES (Simples)
            if command.startswith("lembrar de ") or command.startswith("me lembra de "):
                reminder = command.replace("lembrar de ", "").replace("me lembra de ", "").strip()
                memory_manager.store.add_memory(
                    f"Lembrete para o usuário: {reminder}",
                    {"type": "reminder", "content": reminder, "active": True}
                )
                response = f"Anotei: '{reminder}'. Não esqueça."
                print_kamila(response)
                speak_kamila(tts_engine, response)
                continue

            # --- Processamento Geral (Memória + LLM) ---
            # Se não for comando específico, a Kamila "pensa" e responde
            response = memory_manager.process_interaction(user_input)
            
            print_kamila(response)
            speak_kamila(tts_engine, response)

        except KeyboardInterrupt:
            print("\n\nEncerrando forçadamente...")
            break
        except Exception as e:
            print(f"\n❌ Erro no loop principal: {e}")
            logger.error("Erro no loop", exc_info=True)

def handle_diary(memory_manager, tts_engine):
    """Fluxo interativo para registro de diário."""
    print_kamila("Hora do diário. Vamos refletir.")
    speak_kamila(tts_engine, "Hora do diário. Vamos refletir.")
    
    questions = [
        "O que você fez de mais importante hoje?",
        "O que você aprendeu ou poderia ter feito melhor?",
        "Como você se sentiu na maior parte do dia?"
    ]
    
    answers = []
    
    for q in questions:
        print_kamila(q)
        speak_kamila(tts_engine, q)
        ans = input("👤 Resposta: ").strip()
        if ans:
            answers.append(f"Pergunta: {q} | Resposta: {ans}")
    
    if answers:
        if len(answers) < 3:
             print_kamila("Você foi breve. Tente detalhar mais amanhã.")
        
        full_entry = "\n".join(answers)
        memory_manager.store.add_memory(
            f"Diário do dia {datetime.now().strftime('%d/%m/%Y')}:\n{full_entry}",
            {"type": "diary_entry"}
        )
        
        final_msg = "Diário salvo. Amanhã é um novo dia para evoluir."
        print_kamila(final_msg)
        speak_kamila(tts_engine, final_msg)
    else:
        print_kamila("Nada registrado. Se precisar, estou aqui.")

if __name__ == "__main__":
    main()
