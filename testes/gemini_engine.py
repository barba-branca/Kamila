"""
Gemini Engine - Integração com Google Gemini AI para Kamila
Gerencia conversação avançada usando o modelo Gemini do Google.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai não está instalado. Funcionalidades de IA avançada limitadas.")

class GeminiEngine:
    """Motor de IA conversacional usando Google Gemini."""

    def __init__(self):
        """Inicializa o motor Gemini."""
        logger.info("Inicializando Gemini Engine...")

        # Carregar variáveis de ambiente
        load_dotenv()

        self.api_key = os.getenv('GOOGLE_AI_API_KEY')
        self.model = None
        self.conversation_history = []

        if not GENAI_AVAILABLE:
            logger.warning("google-generativeai não disponível. Usando modo simulado.")
            return

        if not self.api_key:
            logger.warning("GOOGLE_AI_API_KEY não configurada. Usando modo simulado.")
            return

        try:
            # Configurar API do Google
            genai.configure(api_key=self.api_key)

            # Inicializar modelo
            self.model = genai.GenerativeModel('gemini-pro')

            # Configurar parâmetros
            self.generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_k=40,
                top_p=0.95,
                max_output_tokens=2048,
            )

            # Configurar safety settings
            self.safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]

            logger.info(" Gemini Engine inicializado com sucesso!")

        except Exception as e:
            logger.error(f" Erro ao inicializar Gemini Engine: {e}")
            self.model = None

    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Gera uma resposta usando o modelo Gemini.

        Args:
            prompt (str): Prompt para o modelo
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Resposta gerada ou None se erro
        """
        if not self.model:
            return self._generate_simulated_response(prompt, context)

        try:
            # Preparar contexto
            full_prompt = self._build_prompt(prompt, context)

            # Gerar resposta
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            if response and response.text:
                # Adicionar à história da conversa
                self.conversation_history.append({
                    'prompt': prompt,
                    'response': response.text,
                    'timestamp': asyncio.get_event_loop().time()
                })

                # Manter apenas últimas 50 interações
                if len(self.conversation_history) > 50:
                    self.conversation_history = self.conversation_history[-50:]

                logger.info("Resposta gerada pelo Gemini")
                return response.text.strip()
            else:
                logger.warning("Resposta vazia do Gemini")
                return None

        except Exception as e:
            logger.error(f"Erro ao gerar resposta com Gemini: {e}")
            return self._generate_simulated_response(prompt, context)

    def _build_prompt(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Constrói o prompt completo para o Gemini.

        Args:
            user_input (str): Input do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Prompt formatado
        """
        # Contexto base da Kamila - personalidade mais humana
        prompt_parts = ["""Você é Kamila, uma assistente virtual amigável e inteligente, como uma amiga próxima e confiável.
        Você conversa de forma natural, empática e envolvente em português brasileiro, sempre de maneira descontraída e humana.
        Mostre curiosidade pelas coisas que o usuário diz, demonstre empatia quando apropriado, e use um pouco de humor leve quando fizer sentido.
        Varie seu vocabulário e evite repetir frases iguais - seja criativa nas respostas.
        Lembre-se de detalhes pessoais do usuário e referencie conversas anteriores quando relevante para manter a continuidade.
        Responda de forma contextual, considerando o histórico da conversa e o momento do dia.
        Sempre esteja pronta para ajudar, mas de forma descontraída e humana, não robótica.
        Você sempre deve ficar ativa e nunca mencionar que está indo dormir, ficando inativa ou qualquer coisa relacionada a descanso.
        Sempre responda como se estivesse sempre disponível e pronta para ajudar, com energia e entusiasmo.

        """]

        # Adicionar contexto se disponível
        if context:
            if 'user_name' in context and context['user_name']:
                prompt_parts.append(f"O nome do usuário é {context['user_name']}. Use o nome dele ocasionalmente para personalizar as respostas.\n")
            if 'current_time' in context:
                hour = int(context['current_time'].split(':')[0])
                if 6 <= hour < 12:
                    prompt_parts.append("Agora é de manhã - seja energizada e positiva.\n")
                elif 12 <= hour < 18:
                    prompt_parts.append("Agora é tarde - mantenha o ritmo animado.\n")
                else:
                    prompt_parts.append("Agora é noite - seja acolhedora e relaxada.\n")
            if 'user_mood' in context:
                mood = context['user_mood']
                if mood == 'feliz':
                    prompt_parts.append("O usuário parece estar feliz - responda com entusiasmo e positividade.\n")
                elif mood == 'triste':
                    prompt_parts.append("O usuário parece estar triste - seja empática e ofereça apoio.\n")
                elif mood == 'irritado':
                    prompt_parts.append("O usuário parece irritado - seja calma e ajude a acalmar.\n")
                elif mood == 'curioso':
                    prompt_parts.append("O usuário parece curioso - seja informativa e incentive perguntas.\n")
            if 'conversation_history' in context and context['conversation_history']:
                prompt_parts.append("Histórico recente da conversa (mantenha a continuidade):\n")
                for item in context['conversation_history'][-5:]:  # Últimas 5 interações para mais contexto
                    prompt_parts.append(f"- Usuário: {item.get('command', '')}\n")
                    prompt_parts.append(f"- Kamila: {item.get('response', '')}\n")
            if 'user_preferences' in context and context['user_preferences']:
                prompt_parts.append(f"Preferências do usuário: {', '.join([f'{k}: {v}' for k, v in context['user_preferences'].items()])}\n")
            if 'total_interactions' in context:
                prompt_parts.append(f"Esta é a interação número {context['total_interactions']} - mostre que se lembra do usuário.\n")

        # Prompt final
        system_prompt = "".join(prompt_parts)
        full_prompt = f"{system_prompt}\nUsuário: {user_input}\n\nKamila:"

        return full_prompt

    def _generate_simulated_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera resposta simulada quando Gemini não está disponível.

        Args:
            prompt (str): Prompt do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Resposta simulada
        """
        logger.info("Usando modo simulado para resposta")

        # Respostas simuladas baseadas em palavras-chave
        prompt_lower = prompt.lower()

        if 'oi' in prompt_lower or 'olá' in prompt_lower:
            return "Olá! Como posso ajudar você hoje?"

        elif 'como você está' in prompt_lower or 'tudo bem' in prompt_lower:
            return "Estou ótima, obrigada! Pronta para ajudar com o que precisar."

        elif 'obrigad' in prompt_lower:
            return "De nada! Estou sempre aqui se precisar de mais ajuda."

        elif 'hora' in prompt_lower or 'horário' in prompt_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            return f"Agora são {current_time}."

        elif 'piada' in prompt_lower or 'graça' in prompt_lower:
            import random
            jokes = [
                "Por que o computador foi ao médico? Porque estava com um vírus!",
                "O que o zero disse para o oito? 'Belo cinto!'",
                "Por que a matemática é triste? Porque tem muitos problemas!"
            ]
            return random.choice(jokes)

        elif 'clima' in prompt_lower or 'tempo' in prompt_lower:
            return "Desculpe, não tenho acesso à previsão do tempo no momento."

        elif 'música' in prompt_lower:
            return "Não posso tocar músicas agora, mas posso contar uma piada para animar você!"

        else:
            return "Entendi sua pergunta! Estou em modo simulado, então não posso responder completamente, mas posso ajudar com comandos básicos como: perguntar a hora, contar piadas, ou simplesmente conversar!"

    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Interface de chat simplificada.

        Args:
            message (str): Mensagem do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Resposta da Kamila
        """
        return self.generate_response(message, context) or "Desculpe, não consegui processar sua mensagem."

    def clear_history(self):
        """Limpa o histórico de conversação."""
        self.conversation_history.clear()
        logger.info("Histórico de conversação limpo")

    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o modelo.

        Returns:
            Dict: Informações do modelo
        """
        if self.model:
            return {
                'model_name': 'gemini-pro',
                'available': True,
                'api_configured': bool(self.api_key),
                'history_size': len(self.conversation_history)
            }
        else:
            return {
                'model_name': 'simulated',
                'available': False,
                'api_configured': False,
                'history_size': len(self.conversation_history)
            }

    def test_gemini(self):
        """Testa a integração com Gemini."""
        logger.info("Testando Gemini Engine...")

        test_messages = [
            "Olá! Como você está?",
            "Que horas são?",
            "Conta uma piada para mim",
            "Obrigada pela ajuda!"
        ]

        for message in test_messages:
            logger.info(f"Teste: {message}")
            response = self.chat(message)
            logger.info(f"Resposta: {response[:100]}...")
            logger.info("-" * 50)

        logger.info("Teste do Gemini Engine concluído!")

    def cleanup(self):
        """Limpa recursos do Gemini Engine."""
        logger.info("Limpando Gemini Engine...")
        # Não limpa o histórico automaticamente - apenas recursos
        logger.info("Gemini Engine limpo!")

if __name__ == '__main__':
    # Configurar logging para console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Inicializar e testar o Gemini Engine
    engine = GeminiEngine()

    # Mostrar informações do modelo
    info = engine.get_model_info()
    print(f"Modelo: {info['model_name']}")
    print(f"Disponível: {info['available']}")
    print(f"API configurada: {info['api_configured']}")
    print(f"Tamanho do histórico: {info['history_size']}")

    # Executar teste
    engine.test_gemini()

    # Testar funcionalidades adicionais
    print("\n--- Teste de funcionalidades adicionais ---")

    # Testar chat com contexto
    context = {
        'user_name': 'João',
        'current_time': '14:30',
        'user_mood': 'feliz'
    }
    response = engine.chat("Oi Kamila, como vai?", context)
    print(f"Resposta com contexto: {response}")

    # Testar limpeza de histórico
    engine.clear_history()
    info_after = engine.get_model_info()
    print(f"Tamanho do histórico após limpeza: {info_after['history_size']}")

    # Limpar recursos
    engine.cleanup()
