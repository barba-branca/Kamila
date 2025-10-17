"""
Kamila - Assistente Virtual com IA e Voz
Loop principal da assistente com wake word detection e processamento de comandos.
"""
import re
import os
import sys
import time
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv

# Adicionando o diretório atual ao sys.path para imports relativos funcionarem
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
        self.action_manager = ActionManager(self.tts_engine, self.memory_manager)
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
            # --- NOVA LÓGICA DE RECONHECIMENTO DE NOME ---
            user_name = self.memory_manager.get_user_name()
            # Se a Kamila ainda não sabe o nome do usuário, ela verifica se a resposta é um nome.
            if not user_name and self._is_name_response(command):
                name = self._extract_name_from_response(command)
                if name:
                    self.memory_manager.set_user_name(name)
                    response = f"Prazer em te conhecer, {name}! Agora vou me lembrar do seu nome."
                    self.tts_engine.speak(response)
                    self.memory_manager.add_interaction(command, "set_name", response)
                    return # Encerra o processamento aqui, pois a tarefa já foi concluída.
            # --- FIM DA NOVA LÓGICA ---
            
            intent = self.interpreter.interpret_command(command)

            if intent:
                response = self.action_manager.execute_action(intent, command)

                # Se a ação não deu resposta, usa a IA
                if not response:
                    logger.info("Ação não retornou resposta. Usando IA generativa...")
                    context = self._build_context(command)
                    response = self.gemini_engine.chat(command, context)

                # Responder
                if response:
                    self.tts_engine.speak(response)
                    self.memory_manager.add_interaction(command, intent, response)
                else:
                    self.tts_engine.speak("Não tenho uma resposta para isso no momento.")

            else:
                # Comando não reconhecido - tentar IA generativa via streaming
                logger.info("Comando não reconhecido, usando IA com streaming...")
                print("Kamila está pensando...")
                
                context = self._build_context(command)
                
                full_response = ""
                sentence_buffer = ""
                
                # O loop que consome o streaming
                for chunk in self.gemini_engine.generate_response_stream(command, context):
                    full_response += chunk
                    sentence_buffer += chunk
                    
                    # Procura por finais de frases (., !, ?) para falar
                    if any(p in sentence_buffer for p in ".!?"):
                        # Separa a frase completa
                        parts = re.split(r'([.!?])', sentence_buffer)
                        # A frase é a parte do texto mais o seu sinal de pontuação
                        sentence_to_speak = "".join(parts[:2]).strip()
                        # O que sobrou fica no buffer para a próxima iteração
                        sentence_buffer = "".join(parts[2:])

                        if sentence_to_speak:
                            # A primeira resposta é quase instantânea
                            print(f"Kamila diz: {sentence_to_speak}") 
                            self.tts_engine.speak(sentence_to_speak)
                
                # Fala qualquer texto que tenha sobrado no buffer no final
                if sentence_buffer.strip():
                    print(f"Kamila diz: {sentence_buffer.strip()}")
                    self.tts_engine.speak(sentence_buffer.strip())

                if full_response:
                    self.memory_manager.add_interaction(command, "conversational_ai", full_response.strip())
                else:
                    self.tts_engine.speak("Não consegui formular uma resposta.")

        except Exception as e:
            logger.error(f"Erro ao processar comando: {e}", exc_info=True)
            self.tts_engine.speak("Ocorreu um erro interno ao processar seu comando.")

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

    def _is_name_response(self, command: str) -> bool:
        """Verifica se o comando parece ser uma resposta à pergunta sobre o nome."""
        command_lower = command.lower().strip()
        # Palavras-chave que indicam uma resposta de nome
        name_starters = ["meu nome é", "eu sou", "me chamo", "é ", "sou "]
        for starter in name_starters:
            if command_lower.startswith(starter):
                return True
        # Considera uma resposta de 1 a 2 palavras sem verbos como um possível nome
        if len(command.split()) <= 2:
            return True
        return False

    def _extract_name_from_response(self, command: str) -> str:
        """Extrai o nome do usuário a partir de uma frase de resposta."""
        command = command.strip()
        name_starters = ["meu nome é", "eu sou o", "eu sou a", "me chamo", "é ", "sou "]
        for starter in name_starters:
            if command.lower().startswith(starter):
                # Remove a frase inicial e pega o nome, capitalizando-o
                name = command[len(starter):].strip()
                return name.capitalize()
        # Se for só uma ou duas palavras, assume que é o nome
        return command.capitalize()

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
