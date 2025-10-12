"""
AI Studio Integration - Integração com Google AI Studio para Kamila
Gerencia modelos de IA generativa e processamento avançado de linguagem.
"""

import os
import json
import logging
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class AIStudioIntegration:
    """Integração com Google AI Studio para modelos generativos."""

    def __init__(self):
        """Inicializa a integração com AI Studio."""
        logger.info(" Inicializando AI Studio Integration...")

        # Carregar variáveis de ambiente
        load_dotenv()

        self.api_key = os.getenv('GOOGLE_AI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.models_available = []

        if not self.api_key:
            logger.warning("  GOOGLE_AI_API_KEY não configurada. Usando modo simulado.")
            return

        # Verificar modelos disponíveis
        self._discover_available_models()

        logger.info(" AI Studio Integration inicializada!")

    def _discover_available_models(self):
        """Descobre modelos disponíveis na API."""
        try:
            if not self.api_key:
                return

            url = f"{self.base_url}/models?key={self.api_key}"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'models' in data:
                self.models_available = [model['name'] for model in data['models']]
                logger.info(f" Modelos disponíveis: {len(self.models_available)}")

        except Exception as e:
            logger.error(f" Erro ao descobrir modelos: {e}")
            self.models_available = []

    def generate_text(self, prompt: str, model: str = "gemini-pro",
                     temperature: float = 0.7, max_tokens: int = 2048) -> Optional[str]:
        """
        Gera texto usando modelos do AI Studio.

        Args:
            prompt (str): Prompt para geração
            model (str): Nome do modelo
            temperature (float): Temperatura de criatividade (0.0-1.0)
            max_tokens (int): Máximo de tokens na resposta

        Returns:
            str: Texto gerado ou None se erro
        """
        if not self.api_key:
            return self._generate_simulated_text(prompt)

        try:
            url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"

            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "topK": 40,
                    "topP": 0.95
                }
            }

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'candidates' in data and len(data['candidates']) > 0:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    text = candidate['content']['parts'][0]['text']
                    return text.strip()

            return None

        except Exception as e:
            logger.error(f" Erro ao gerar texto: {e}")
            return self._generate_simulated_text(prompt)

    def _generate_simulated_text(self, prompt: str) -> str:
        """
        Gera texto simulado quando API não está disponível.

        Args:
            prompt (str): Prompt do usuário

        Returns:
            str: Resposta simulada
        """
        logger.info(" Usando modo simulado para geração de texto")

        prompt_lower = prompt.lower()

        # Respostas simuladas baseadas em contexto
        if 'oi' in prompt_lower or 'olá' in prompt_lower:
            return "Olá! Sou Kamila, sua assistente virtual. Como posso ajudar você hoje?"

        elif 'como você está' in prompt_lower:
            return "Estou ótima, obrigada por perguntar! Estou aqui e pronta para ajudar com o que precisar."

        elif 'obrigad' in prompt_lower:
            return "De nada! É sempre um prazer ajudar. Se precisar de mais alguma coisa, é só chamar!"

        elif 'hora' in prompt_lower or 'horário' in prompt_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            return f"Agora são {current_time}. O tempo está passando rápido hoje!"

        elif 'piada' in prompt_lower:
            import random
            jokes = [
                "Por que o computador foi ao médico? Porque estava com um vírus! ",
                "O que o zero disse para o oito? 'Belo cinto!' ",
                "Por que a matemática é triste? Porque tem muitos problemas! "
            ]
            return random.choice(jokes)

        elif 'clima' in prompt_lower or 'tempo' in prompt_lower:
            return "Infelizmente não tenho acesso à previsão do tempo no momento, mas posso ajudar com outras coisas!"

        elif 'música' in prompt_lower:
            return "Não posso tocar músicas agora, mas posso contar uma piada ou dizer a hora para animar você! "

        elif 'ajuda' in prompt_lower or 'socorro' in prompt_lower:
            return """Posso ajudar você com várias coisas:
            • Dizer a hora atual
            • Contar piadas
            • Responder perguntas
            • Conversar sobre diversos assuntos
            • Lembrar de informações importantes

            O que você gostaria de fazer?"""

        else:
            return f"Interessante! Você mencionou: '{prompt[:50]}...'. Estou em modo simulado, então não posso responder completamente, mas posso ajudar com comandos básicos como perguntar a hora, contar piadas, ou simplesmente bater um papo!"

    def chat_completion(self, messages: List[Dict[str, str]],
                       model: str = "gemini-pro", temperature: float = 0.7) -> Optional[str]:
        """
        Gera completion de chat usando histórico de mensagens.

        Args:
            messages (List[Dict]): Lista de mensagens no formato [{"role": "user/assistant", "content": "texto"}]
            model (str): Nome do modelo
            temperature (float): Temperatura de criatividade

        Returns:
            str: Resposta gerada ou None se erro
        """
        if not self.api_key:
            return self._simulate_chat_completion(messages)

        try:
            url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"

            payload = {
                "contents": messages,
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": 2048,
                    "topK": 40,
                    "topP": 0.95
                }
            }

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'candidates' in data and len(data['candidates']) > 0:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    text = candidate['content']['parts'][0]['text']
                    return text.strip()

            return None

        except Exception as e:
            logger.error(f" Erro no chat completion: {e}")
            return self._simulate_chat_completion(messages)

    def _simulate_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        Simula chat completion quando API não está disponível.

        Args:
            messages (List[Dict]): Lista de mensagens

        Returns:
            str: Resposta simulada
        """
        if not messages:
            return "Olá! Como posso ajudar?"

        last_message = messages[-1].get('content', '').lower()

        # Simular respostas baseadas no contexto
        if 'oi' in last_message or 'olá' in last_message:
            return "Oi! Tudo bem? Estou aqui para ajudar com o que precisar!"

        elif 'como você está' in last_message:
            return "Estou ótima! E você, como está se sentindo hoje?"

        elif 'obrigad' in last_message:
            return "De nada! Foi um prazer ajudar. Posso fazer mais alguma coisa por você?"

        else:
            return "Entendi sua mensagem! Em modo simulado, posso responder perguntas básicas, contar piadas, ou simplesmente conversar. O que mais você gostaria de saber?"

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analisa o sentimento do texto.

        Args:
            text (str): Texto para análise

        Returns:
            Dict: Resultado da análise de sentimento
        """
        if not self.api_key:
            return self._simulate_sentiment_analysis(text)

        try:
            # Usar o modelo para análise de sentimento
            prompt = f"""Analise o sentimento do seguinte texto em português brasileiro.
            Responda apenas com um JSON no formato:
            {{"sentimento": "positivo/negativo/neutro", "confianca": 0.0-1.0, "emocoes": ["lista", "de", "emoções"]}}

            Texto: {text}"""

            response = self.generate_text(prompt, temperature=0.1)

            if response:
                try:
                    # Tentar extrair JSON da resposta
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return self._simulate_sentiment_analysis(text)

        except Exception as e:
            logger.error(f" Erro na análise de sentimento: {e}")
            return self._simulate_sentiment_analysis(text)

    def _simulate_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """
        Simula análise de sentimento quando API não está disponível.

        Args:
            text (str): Texto para análise

        Returns:
            Dict: Análise simulada
        """
        text_lower = text.lower()

        # Análise simples baseada em palavras-chave
        positive_words = ['bom', 'ótimo', 'excelente', 'feliz', 'alegre', 'gostei', 'obrigado', 'parabéns']
        negative_words = ['ruim', 'horrível', 'triste', 'chateado', 'odeio', 'terrível', 'problema', 'mal']

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            sentiment = "positivo"
            confidence = min(0.8, 0.5 + (positive_count * 0.1))
            emotions = ["feliz", "contente"]
        elif negative_count > positive_count:
            sentiment = "negativo"
            confidence = min(0.8, 0.5 + (negative_count * 0.1))
            emotions = ["triste", "chateado", "mal"]
        else:
            sentiment = "neutro"
            confidence = 0.6
            emotions = ["neutro"]

        return {
            "sentimento": sentiment,
            "confianca": confidence,
            "emocoes": emotions
        }

    def get_available_models(self) -> List[str]:
        """
        Retorna lista de modelos disponíveis.

        Returns:
            List[str]: Lista de nomes dos modelos
        """
        return self.models_available.copy()

    def test_integration(self):
        """Testa a integração com AI Studio."""
        logger.info(" Testando AI Studio Integration...")

        test_cases = [
            "Olá! Como você está?",
            "Que horas são?",
            "Conta uma piada",
            "Obrigado pela ajuda!"
        ]

        for test in test_cases:
            logger.info(f"  Teste: {test}")
            response = self.generate_text(test)
            logger.info(f" Resposta: {response[:100]}...")
            logger.info("-" * 50)

        # Testar análise de sentimento
        sentiment_test = "Estou muito feliz hoje!"
        sentiment = self.analyze_sentiment(sentiment_test)
        logger.info(f" Análise de sentimento: {sentiment}")

        logger.info(" Teste da AI Studio Integration concluído!")

