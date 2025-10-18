"""
Kamila - Assistente Virtual com IA e Voz
Versão com Arquitetura de Memória Inteligente (Curto e Longo Prazo).
"""
import os
import sys
import time
import logging
import threading
import queue
from datetime import datetime
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, '.kamila'))

from core.stt_engine import STTEngine
from core.tts_engine import TTSEngine
from core.memory_manager import MemoryManager
from kamila_ia_models.llm_interface import LLMInterface
from flask import Flask, request


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logs/kamila.log'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

app = Flask(__name__)
assistant = None


class KamilaAssistant:
    def __init__(self):
        """Inicializa a Kamila e todos os seus componentes, incluindo a nova memória."""
        logger.info("Inicializando Kamila com memória inteligente...")
        load_dotenv(os.path.join(project_root, '.env'))

        self.speak_queue = queue.Queue()
        self.wake_word = "kamila"
        
        try:
            # Componentes de Voz e Ação
            self.stt_engine = STTEngine(wake_word=self.wake_word)
            self.tts_engine = TTSEngine()

            # --- INTEGRAÇÃO DA NOVA MEMÓRIA ---
            self.llm_interface = LLMInterface()
            self.memory = MemoryManager(self.llm_interface) 

        except ValueError as e:
            logger.error(f"ERRO DE CONFIGURAÇÃO: {e}. Verifique o arquivo .env.")
            sys.exit(1)

        self.is_awake = False
        logger.info("Kamila inicializada com sucesso!")

    def check_speak_queue(self):
        """Processa a fila de mensagens para falar, uma por uma."""
        if not self.speak_queue.empty():
            try:
                message = self.speak_queue.get_nowait()
                if message:
                    self.tts_engine.speak(message)
            except queue.Empty:
                pass 

    def start(self):
        """Inicia o loop principal de escuta e fala da Kamila."""
        logger.info("Iniciando o loop principal da Kamila.")
        self.speak_queue.put("Sistemas online. Aguardando ativação.")

        try:
            while True:
                self.check_speak_queue()
                if not self.is_awake:
                    if self.stt_engine.block_for_wake_word():
                        self.wake_up()
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Interrupção detectada.")
        finally:
            self.shutdown()
            
    def wake_up(self):
        """Acorda a assistente, cumprimenta, ouve um comando, processa e volta a dormir."""
        self.is_awake = True
        self.greet_user()

        command = self.stt_engine.listen_for_command(timeout=10) # Tempo generoso para o usuário falar
        if command:
            self.process_command(command)
        else:
            logger.info("Nenhum comando recebido após ativação.")
            self.speak_queue.put("Acho que não ouvi nada. Se precisar de mim, é só chamar!")
        
        self.go_to_sleep()

    def go_to_sleep(self):
        """Volta para o modo de escuta passiva."""
        self.is_awake = False
        logger.info("Kamila voltando ao modo de espera pela wake word.")

    def greet_user(self):
        """Cumprimenta o usuário usando o nome guardado na memória."""
        user_name = self.memory.user_name
        greeting = f"Olá, {user_name}! Estou ouvindo." if user_name != "usuário" else "Olá! Estou ouvindo."
        self.speak_queue.put(greeting)
        
    def greet_on_unlock(self):
        """Saudação especial (via API) para quando o PC é desbloqueado."""
        print("\n!!! GATILHO DE SAUDAÇÃO RECEBIDO !!!\n")
        user_name = self.memory.user_name
        greeting = f"Bem-vindo de volta, {user_name}!" if user_name != "usuário" else "Bem-vindo de volta!"
        self.speak_queue.put(greeting)

    def process_command(self, command):
        """Processa um comando de voz usando o novo MemoryManager."""
        logger.info(f"Processando comando com memória inteligente: '{command}'")
        
        assistant_response = self.memory.process_interaction(command)
        
        self.speak_queue.put(assistant_response)

    def shutdown(self):
        """Encerra a assistente de forma segura."""
        logger.info("Encerrando Kamila...")
        self.speak_queue.put("Até logo.")
        # Espera um pouco para a última mensagem ser processada e falada
        time.sleep(3)
        self.check_speak_queue()



@app.route('/trigger_greeting', methods=['POST'])
def trigger_greeting():
    """Endpoint da API para disparar a saudação de desbloqueio."""
    global assistant
    if assistant:
        logger.info("API: Gatilho de saudação recebido via Flask.")
        threading.Thread(target=assistant.greet_on_unlock, daemon=True).start()
        return {"status": "success", "message": "Gatilho de saudação enfileirado."}
    return {"status": "error", "message": "Assistente não está pronta."}, 500

def run_api():
    """Inicia o servidor Flask em modo de produção."""
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=5000)

def main():
    """Função principal que inicializa a assistente e o servidor da API."""
    global assistant
    try:
        assistant = KamilaAssistant()
        
        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        logger.info("Servidor da API da Kamila iniciado em segundo plano na porta 5000.")

        assistant.start()

    except Exception as e:
        logger.error(f"Erro fatal na inicialização: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()