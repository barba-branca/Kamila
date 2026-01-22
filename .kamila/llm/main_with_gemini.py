#!/usr/bin/env python3
"""
Kamila - Assistente Virtual com IA e Voz
Loop principal da assistente com wake word detection e processamento de comandos.
Inclui integração com Google Gemini AI e AI Studio.
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv

# Importações dos módulos core
from core.stt_engine import STTEngine
from core.tts_engine import TTSEngine
from core.interpreter import CommandInterpreter
from core.memory_manager import MemoryManager
from core.actions import ActionManager
from core.gemini_engine import GeminiEngine
from core.ai_studio_integration import AIStudioIntegration

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
    """Classe principal da assistente virtual Kamila."""

    def __init__(self):
        """Inicializa a assistente Kamila."""
        logger.info("🚀 Inicializando Kamila...")

        # Carregar variáveis de ambiente
        load_dotenv('.kamila/.env')

        # Inicializar componentes
        self.stt_engine = STTEngine()
        self.tts_engine = TTSEngine()
        self.interpreter = CommandInterpreter()
        self.memory_manager = MemoryManager()
        self.action_manager = ActionManager()
        self.gemini_engine = GeminiEngine()
        self.ai_studio = AIStudioIntegration()

        # Estado da assistente
        self.is_listening = False
        self.is_awake = False
        self.last_interaction = time.time()

        # Configurações
        self.wake_word = "kamila"  # Palavra de ativação
        self.inactivity_timeout = 30  # Segundos de inatividade

        logger.info(" Kamila inicializada com sucesso!")

    def start(self):
        """Inicia o loop principal da assistente."""
        logger.info(" Iniciando monitoramento de wake word...")

        try:
            while True:
                # Kamila sempre fica ativa, sem timeout de inatividade
                # Removido o check de inatividade para manter Kamila sempre acordada

                # Aguardar wake word
                if not self.is_awake:
                    logger.debug(" Aguardando wake word...")
                    wake_word_detected = self.stt_engine.detect_wake_word(self.wake_word)

                    if wake_word_detected:
                        self.wake_up()
                        self.greet_user()

                # Modo ativo - processar comandos
                else:
                    logger.debug(" Ouvindo comandos...")
                    command = self.stt_engine.listen_for_command()

                    if command:
                        self.last_interaction = time.time()
                        self.process_command(command)
                    # Removido o else que chamava go_to_sleep para manter ativa

                time.sleep(0.1)  # Pequena pausa para não sobrecarregar

        except KeyboardInterrupt:
            logger.info(" Interrupção detectada. Encerrando Kamila...")
            self.shutdown()
        except Exception as e:
            logger.error(f" Erro crítico: {e}")
            self.shutdown()

    def wake_up(self):
        """Acorda a assistente."""
        logger.info(" Kamila acordando...")
        self.is_awake = True
        self.is_listening = True

        # Saudação visual/auditiva
        self.tts_engine.speak("Olá! Estou acordada e pronta para ajudar!")

        # Atualizar memória
        self.memory_manager.update_interaction()

    def go_to_sleep(self):
        """Coloca a assistente em modo de espera."""
        logger.info(" Kamila em modo de espera...")
        self.is_awake = False
        self.is_listening = False

        # Removida a despedida para manter Kamila sempre ativa
        # self.tts_engine.speak("Até logo! Me chame quando precisar.")

    def greet_user(self):
        """Saudação personalizada baseada na memória."""
        user_name = self.memory_manager.get_user_name()
        current_time = datetime.now().hour

        if 6 <= current_time < 12:
            greeting = f"Bom dia"
        elif 12 <= current_time < 18:
            greeting = "Boa tarde"
        else:
            greeting = "Boa noite"

        if user_name:
            greeting += f", {user_name}!"
        else:
            greeting += "!"

        self.tts_engine.speak(greeting)

    def process_command(self, command):
        """Processa um comando de voz."""
        logger.info(f" Processando comando: {command}")

        try:
            # Interpretar comando
            intent = self.interpreter.interpret_command(command)

            if intent:
                # Executar ação
                response = self.action_manager.execute_action(intent, command)

                # Se não há resposta específica, usar IA generativa
                if not response or response.startswith("Desculpe"):
                    logger.info(" Usando IA generativa para resposta avançada...")
                    context = self._build_context()
                    ai_response = self.gemini_engine.chat(command, context)

                    if ai_response:
                        response = ai_response
                    else:
                        response = "Desculpe, não consegui processar sua solicitação com IA."

                # Responder
                if response:
                    self.tts_engine.speak(response)
                    response_text = response
                else:
                    self.tts_engine.speak("Comando executado com sucesso!")
                    response_text = "Comando executado com sucesso!"

                # Atualizar memória
                self.memory_manager.add_interaction(command, intent, response_text)

            else:
                # Comando não reconhecido - tentar IA generativa
                logger.info(" Comando não reconhecido, tentando IA generativa...")
                context = self._build_context()
                ai_response = self.gemini_engine.chat(command, context)

                if ai_response:
                    self.tts_engine.speak(ai_response)
                    # Criar intenção genérica para comandos não reconhecidos
                    self.memory_manager.add_interaction(command, "conversational_ai", ai_response)
                else:
                    self.tts_engine.speak("Desculpe, não entendi esse comando. Pode repetir?")

        except Exception as e:
            logger.error(f"Erro ao processar comando: {e}")
            self.tts_engine.speak("Ocorreu um erro ao processar seu comando.")

    def _build_context(self):
        """Constrói contexto para IA generativa."""
        return {
            'user_name': self.memory_manager.get_user_name(),
            'mood': self.memory_manager.get_mood(),
            'conversation_history': self.memory_manager.get_recent_interactions(5),
            'current_time': datetime.now().strftime("%H:%M"),
            'assistant_name': 'Kamila'
        }

    def shutdown(self):
        """Encerra a assistente."""
        logger.info(" Encerrando Kamila...")
        self.tts_engine.speak("Até logo! Foi um prazer ajudar você.")
        self.stt_engine.cleanup()
        self.tts_engine.cleanup()
        self.gemini_engine.cleanup()
        self.ai_studio.cleanup()

def main():
    """Função principal."""
    try:
        # Verificar se .env existe
        if not os.path.exists('.kamila/.env'):
            logger.warning("  Arquivo .env não encontrado. Criando arquivo de exemplo...")
            create_env_example()

        # Inicializar e executar assistente
        assistant = KamilaAssistant()
        assistant.start()

    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)

def create_env_example():
    """Cria arquivo .env.example com as variáveis necessárias."""
    env_content = """# Kamila Assistant - Environment Variables

# API Keys
PICOVOICE_API_KEY=sua_chave_picovoice_aqui
GOOGLE_API_KEY=sua_chave_google_speech_aqui
GOOGLE_AI_API_KEY=sua_chave_google_ai_aqui

# Configurações de Voz
VOICE_RATE=180
VOICE_VOLUME=0.8

# Configurações de Hardware (opcional)
ARDUINO_PORT=/dev/ttyUSB0
ARDUINO_BAUDRATE=9600

# Configurações da Assistente
ASSISTANT_NAME=Kamila
WAKE_WORD=kamila
INACTIVITY_TIMEOUT=30

# Configurações de Debug
DEBUG_MODE=false
LOG_LEVEL=INFO
"""

    with open('.kamila/.env.example', 'w', encoding='utf-8') as f:
        f.write(env_content)

    print(" Arquivo .env.example criado!")
    print("  Edite o arquivo .kamila/.env com suas chaves de API reais.")

if __name__ == "__main__":
    main()
