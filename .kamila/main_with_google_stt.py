#!/usr/bin/env python3
"""
Kamila - Assistente Virtual com Wake Word e Voz
Versão com Google Speech Recognition (sem Picovoice).
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv

# Import engines
from core.tts_engine import TTSEngine
from core.stt_engine_google import STTEngine

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/kamila.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KamilaAssistant:
    """Classe principal da assistente virtual Kamila com wake word."""

    def __init__(self):
        """Inicializa a assistente Kamila."""
        logger.info("🚀 Inicializando Kamila com Google STT...")

        # Carregar variáveis de ambiente
        load_dotenv('.kamila/.env')

        # Estado da assistente
        self.is_listening = False
        self.is_awake = False
        self.last_interaction = time.time()

        # Configurações
        self.wake_word = "kamila"  # Palavra de ativação
        self.inactivity_timeout = int(os.getenv('INACTIVITY_TIMEOUT', '30'))
        self.command_timeout = int(os.getenv('COMMAND_TIMEOUT', '5'))

        # Inicializar engines
        self.tts_engine = TTSEngine()
        self.stt_engine = STTEngine()

        # Thread para escutar wake word
        self.wake_word_thread = None
        self.stop_listening = False

        logger.info(" Kamila inicializada com sucesso!")

    def start(self):
        """Inicia o loop principal da assistente."""
        logger.info(" Iniciando Kamila com Google STT...")

        try:
            print(" Kamila Assistente Virtual")
            print("  Diga 'kamila' para me ativar")
            print(" Digite 'ajuda' para ver comandos disponíveis")
            print(" Digite 'sair' para encerrar")
            print("-" * 50)

            # Iniciar thread de wake word
            self.start_wake_word_detection()

            while True:
                # Verificar inatividade
                if self.is_awake and (time.time() - self.last_interaction) > self.inactivity_timeout:
                    self.go_to_sleep()

                # Aguardar comando (modo texto como fallback)
                if not self.is_awake:
                    command = input("  Digite um comando: ").strip().lower()

                    if self.wake_word in command:
                        self.wake_up()
                        self.greet_user()
                    elif command in ['sair', 'quit', 'exit']:
                        break
                    elif command:
                        print(" Digite 'kamila' primeiro para me ativar!")

                # Modo ativo - processar comandos
                else:
                    command = input(" Kamila ativa - Digite seu comando: ").strip().lower()

                    if command:
                        self.last_interaction = time.time()
                        self.process_command(command)
                    else:
                        # Timeout - voltar para modo de espera
                        logger.debug(" Timeout - voltando para modo de espera")
                        self.go_to_sleep()

        except KeyboardInterrupt:
            logger.info(" Interrupção detectada. Encerrando Kamila...")
            self.shutdown()
        except Exception as e:
            logger.error(f" Erro crítico: {e}")
            self.shutdown()

    def start_wake_word_detection(self):
        """Inicia a detecção de wake word em uma thread separada."""
        if self.wake_word_thread and self.wake_word_thread.is_alive():
            logger.warning("  Wake word já está rodando")
            return

        self.stop_listening = False
        self.wake_word_thread = threading.Thread(target=self._wake_word_loop)
        self.wake_word_thread.daemon = True
        self.wake_word_thread.start()
        logger.info(" Detecção de wake word iniciada")

    def stop_wake_word_detection(self):
        """Para a detecção de wake word."""
        self.stop_listening = True
        if self.wake_word_thread:
            self.wake_word_thread.join(timeout=2)
        logger.info(" Detecção de wake word parada")

    def _wake_word_loop(self):
        """Loop principal de detecção de wake word."""
        logger.info(" Iniciando loop de wake word...")

        while not self.stop_listening:
            try:
                # Detectar wake word usando Google STT
                if self.stt_engine.detect_wake_word(self.wake_word, timeout=5):
                    logger.info("🗣️  Wake word detectada!")
                    self.wake_up()
                    self.greet_user()

                time.sleep(0.1)  # Pequena pausa para não sobrecarregar

            except Exception as e:
                logger.error(f" Erro no loop de wake word: {e}")
                time.sleep(1)  # Aguardar antes de tentar novamente

    def wake_up(self):
        """Acorda a assistente."""
        logger.info(" Kamila acordando...")
        self.is_awake = True
        self.is_listening = True

        # Saudação com voz
        self.tts_engine.speak("Olá! Estou acordada e pronta para ajudar!")

        # Atualizar timestamp
        self.last_interaction = time.time()

    def go_to_sleep(self):
        """Coloca a assistente em modo de espera."""
        logger.info(" Kamila indo dormir...")
        self.is_awake = False
        self.is_listening = False

        # Despedida com voz
        self.tts_engine.speak("Até logo! Me chame quando precisar.")

    def greet_user(self):
        """Saudação personalizada."""
        current_time = datetime.now().hour

        if 6 <= current_time < 12:
            greeting = "Bom dia"
        elif 12 <= current_time < 18:
            greeting = "Boa tarde"
        else:
            greeting = "Boa noite"

        self.tts_engine.speak(f"{greeting}! Como posso ajudar?")

    def process_command(self, command):
        """Processa um comando."""
        logger.info(f" Processando comando: {command}")

        try:
            # Processar comandos simples
            response = self._handle_simple_commands(command)

            if response:
                # Falar a resposta
                self.tts_engine.speak(response)
            else:
                error_msg = "Desculpe, não entendi esse comando. Pode repetir?"
                self.tts_engine.speak(error_msg)

        except Exception as e:
            logger.error(f"Erro ao processar comando: {e}")
            error_msg = "Ocorreu um erro ao processar seu comando."
            self.tts_engine.speak(error_msg)

    def _handle_simple_commands(self, command):
        """Manipula comandos simples sem IA."""
        command = command.lower().strip()

        # Saudação
        if any(word in command for word in ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite']):
            return "Olá! Como posso ajudar?"

        # Hora
        elif 'hora' in command or 'que horas' in command:
            now = datetime.now()
            return f"Agora são {now.strftime('%H:%M')}"

        # Data
        elif 'data' in command or 'que dia' in command:
            now = datetime.now()
            return f"Hoje é {now.strftime('%A, %d de %B de %Y')}"

        # Ajuda
        elif 'ajuda' in command or 'help' in command:
            return """Comandos disponíveis:
• 'hora' - ver a hora atual
• 'data' - ver a data atual
• 'tchau' - se despedir
• 'status' - ver status da assistente
• 'sair' - encerrar o programa"""

        # Status
        elif 'status' in command or 'como você está' in command:
            return "Estou funcionando perfeitamente! Pronta para ajudar!"

        # Despedida
        elif any(word in command for word in ['tchau', 'adeus', 'até logo']):
            self.go_to_sleep()
            return "Tchau! Foi bom conversar com você!"

        # Não reconhecido
        else:
            return None

    def shutdown(self):
        """Encerra a assistente."""
        logger.info(" Encerrando Kamila...")
        self.stop_wake_word_detection()
        self.tts_engine.speak("Até logo! Foi um prazer ajudar você.")
        self.tts_engine.cleanup()
        self.stt_engine.cleanup()

def main():
    """Função principal."""
    try:
        # Verificar se .env existe
        if not os.path.exists('.kamila/.env'):
            logger.warning("  Arquivo .env não encontrado. Usando configurações padrão.")

        # Inicializar e executar assistente
        assistant = KamilaAssistant()
        assistant.start()

    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
