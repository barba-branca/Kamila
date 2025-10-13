"""
Kamila - Assistente Virtual com IA e Voz
Loop principal da assistente com wake word detection e processamento de comandos.
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv

# Adicionar o diretório atual ao sys.path para imports relativos funcionarem
sys.path.insert(0, os.path.dirname(__file__))

# Importações dos módulos core
from core.stt_engine import STTEngine
from core.tts_engine import TTSEngine
from core.interpreter import CommandInterpreter
from core.memory_manager import MemoryManager
from core.actions import ActionManager

# Importações dos módulos LLM (Gemini AI)
from llm.gemini_engine import GeminiEngine
from llm.ai_studio_integration import AIStudioIntegration

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
        logger.info("Inicializando Kamila...")

        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            logger.warning("Arquivo .env não encontrado na raiz do projeto.")
        
        # Configurações devem vir primeiro
        self.wake_word = "kamila"  # Palavra de ativação
        self.inactivity_timeout = 300  # 5 minutos

        # Agora inicializamos os componentes, passando a wake_word
        self.stt_engine = STTEngine(wake_word=self.wake_word)
        self.tts_engine = TTSEngine()
        self.interpreter = CommandInterpreter()
        self.memory_manager = MemoryManager()
        self.action_manager = ActionManager(self.tts_engine)
        self.gemini_engine = GeminiEngine()
        self.ai_studio = AIStudioIntegration()

        # Estado da assistente
        self.is_awake = False
        self.last_interaction = time.time()

        logger.info("Kamila inicializada com sucesso!")

    def start(self):
        """Inicia o loop principal da assistente."""
        logger.info("Iniciando o loop principal da Kamila.")
        self.tts_engine.speak("Iniciando sistemas. Aguardando ativação.")

        try:
            while True:
                if not self.is_awake:
                    logger.info("Aguardando a palavra de ativação 'Kamila'...")
                    # Este método agora bloqueia a execução até que a palavra seja ouvida
                    detected = self.stt_engine.block_for_wake_word()
                    if detected:
                        self.wake_up()

                if self.is_awake:
                    logger.info("Kamila ativa. Ouvindo o comando...")
                    command = self.stt_engine.listen_for_command(timeout=10)

                    if command:
                        self.last_interaction = time.time()
                        self.process_command(command)
                        # Após processar, volta a dormir e a escutar a wake word
                        self.go_to_sleep()
                    else:
                        logger.info("Nenhum comando recebido. Voltando ao modo de espera.")
                        self.go_to_sleep()
                
                time.sleep(0.1)

        except KeyboardInterrupt:
            logger.info("Interrupção detectada. Encerrando Kamila...")
            self.shutdown()
        except Exception as e:
            logger.error(f"Erro crítico no loop principal: {e}", exc_info=True)
            self.shutdown()


    def wake_up(self):
        """Acorda a assistente."""
        if not self.is_awake:
            logger.info("Kamila acordando...")
            self.is_awake = True
            self.last_interaction = time.time()
            self.greet_user()

    def go_to_sleep(self):
        """Coloca a assistente em modo de espera."""
        if self.is_awake:
            logger.info("Kamila voltando para o modo de espera.")
            self.is_awake = False

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
            greeting += f", {user_name}! Que bom te ver de novo!"
        else:
            greeting += "! Qual é o seu nome?"

        self.tts_engine.speak(greeting)

    def process_command(self, command):
        """Processa um comando de voz."""
        logger.info(f"Processando comando: {command}")

        try:
            # Verificar se é resposta à pergunta de nome
            user_name = self.memory_manager.get_user_name()
            if not user_name and self._is_name_response(command):
                name = self._extract_name_from_response(command)
                if name:
                    self.memory_manager.set_user_name(name)
                    self.tts_engine.speak(f"Prazer em conhecer você, {name}! Agora vou me lembrar do seu nome.")
                    self.memory_manager.add_interaction(command, "name_response", f"Nome definido: {name}")
                    return

            # Interpretar comando
            intent = self.interpreter.interpret_command(command)

            if intent:
                # Executar ação
                response = self.action_manager.execute_action(intent, command)

                # Se não há resposta específica, usar IA generativa
                if not response or response.startswith("Desculpe"):
                    logger.info("Usando modelos de linguagem para resposta avançada...")
                    context = self._build_context(command)
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
                logger.info("Comando não reconhecido, tentando modelos de linguagem...")
                # Avisa que está pensando (opcional, ajuda a diminuir a ansiedade da espera)
                print("Kamila está pensando...") 
                
                context = self._build_context(command)
                ai_response = self.gemini_engine.chat(command, context)

                if ai_response:
                    # --- DEBUG: MOSTRAR O QUE A IA DISSE ---
                    logger.info(f"--- RESPOSTA DA IA ({len(ai_response)} caracteres) ---")
                    # Imprime no console para você ler, caso o áudio falhe
                    print(f"\n>>> KAMILA DIZ: {ai_response}\n") 
                    logger.info("Tentando falar a resposta...")
                    
                    try:
                        self.tts_engine.speak(ai_response)
                        logger.info("Fala concluída com sucesso.")
                    except Exception as e:
                        logger.error(f"ERRO NO TTS ao tentar falar a resposta da IA: {e}")
                        print("(Erro de áudio, mas a resposta textual está acima)")

                    # Salvar na memória
                    self.memory_manager.add_interaction(command, "conversational_ai", ai_response)
                else:
                    logger.warning("IA retornou resposta vazia.")
                    self.tts_engine.speak("Desculpe, tive um problema para pensar na resposta.")
        except Exception as e:
            logger.error(f"Erro ao processar comando: {e}")
            self.tts_engine.speak("Ocorreu um erro ao processar seu comando.")

    def _build_context(self, command=None):
        """Constrói contexto para modelos de linguagem."""
        context = {
            'user_name': self.memory_manager.get_user_name(),
            'conversation_history': self.memory_manager.get_recent_interactions(5),
            'current_time': datetime.now().strftime("%H:%M"),
            'assistant_name': 'Kamila',
            'user_preferences': self.memory_manager.get_user_preferences(),
            'total_interactions': self.memory_manager.get_statistics().get('total_interactions', 0)
        }

        # Detectar humor do usuário se comando fornecido
        if command:
            context['user_mood'] = self._detect_user_mood(command)

        return context

    def _detect_user_mood(self, command: str) -> str:
        """Detecta o humor aproximado do usuário baseado no comando."""
        command_lower = command.lower()

        # Palavras positivas
        positive_words = ['ótimo', 'bom', 'feliz', 'alegre', 'incrível', 'maravilhoso', 'perfeito', 'excelente', 'satisfeito', 'contente', 'amo', 'adoro', 'gosto', 'obrigado', 'valeu', 'beleza', 'show', 'top', 'genial']
        # Palavras negativas
        negative_words = ['ruim', 'péssimo', 'horrível', 'terrível', 'triste', 'chateado', 'irritado', 'raiva', 'odeio', 'detesto', 'problema', 'erro', 'falha', 'quebrou', 'quebrado']
        # Palavras de curiosidade
        curious_words = ['como', 'por que', 'quando', 'onde', 'quem', 'qual', 'o que', 'explica', 'me diz', 'conta', 'fala', 'interessante', 'curioso']

        positive_count = sum(1 for word in positive_words if word in command_lower)
        negative_count = sum(1 for word in negative_words if word in command_lower)
        curious_count = sum(1 for word in curious_words if word in command_lower)

        if positive_count > negative_count and positive_count > 0:
            return 'feliz'
        elif negative_count > positive_count and negative_count > 0:
            return 'triste'
        elif curious_count > 1:  # Mais de uma palavra de curiosidade
            return 'curioso'
        elif negative_count > 0 and ('!' in command or '?' in command):
            return 'irritado'
        else:
            return 'neutro'

    def _is_name_response(self, command: str) -> bool:
        """Verifica se o comando parece ser uma resposta à pergunta de nome."""
        command_lower = command.lower().strip()

        # Respostas comuns à pergunta "Qual é o seu nome?"
        name_indicators = [
            'meu nome é', 'eu sou', 'sou o', 'me chamo', 'eu me chamo',
            'pode me chamar de', 'diga', 'fala', 'é'
        ]

        # Verificar se começa com indicadores de nome
        for indicator in name_indicators:
            if command_lower.startswith(indicator):
                return True

        # Verificar se é apenas um nome (palavra simples)
        words = command_lower.split()
        if len(words) <= 3 and not any(char in command_lower for char in ['?', '!', '.', ',']):
            # Não parece um comando normal
            return True

        return False

    def _extract_name_from_response(self, command: str) -> str:
        """Extrai o nome de uma resposta à pergunta de nome."""
        command_lower = command.lower().strip()

        # Padrões comuns de resposta
        patterns = [
            ('meu nome é', ''),
            ('eu sou', ''),
            ('sou o', ''),
            ('sou a', ''),
            ('me chamo', ''),
            ('eu me chamo', ''),
            ('pode me chamar de', ''),
            ('diga', ''),
            ('fala', ''),
        ]

        for pattern, replacement in patterns:
            if pattern in command_lower:
                name = command_lower.replace(pattern, replacement).strip()
                # Capitalizar primeira letra
                if name:
                    return name.capitalize()
                else:
                    return command.strip().capitalize()

        # Se não encontrou padrão, assumir que o comando inteiro é o nome
        words = command.split()
        if len(words) <= 3:
            return command.strip().capitalize()

        # Fallback: usar primeira palavra como nome
        return command.split()[0].capitalize()

    def shutdown(self):
        """Encerra a assistente."""
        logger.info("Encerrando Kamila...")
        self.tts_engine.speak("Até logo! Foi um prazer ajudar você.")
        self.stt_engine.cleanup()
        self.tts_engine.cleanup()
        self.gemini_engine.cleanup()
        self.ai_studio.cleanup()

def main():
    """Função principal."""
    try:
        # Verificar se .env existe
        if not os.path.exists('.env'):
            logger.warning("Arquivo .env não encontrado. Criando arquivo de exemplo...")
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

    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_content)

    print("Arquivo .env.example criado!")
    print("Edite o arquivo .env com suas chaves de API reais.")

if __name__ == "__main__":
    main()
