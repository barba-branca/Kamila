
"""
Command Interpreter - Interpretação de Comandos para Kamila
Sistema de interpretação de comandos de voz usando IA.
"""

import os
import re
import logging
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

logger = logging.getLogger(__name__)

class CommandInterpreter:
    """Interpreta comandos de voz e identifica intenções."""

    def __init__(self):
        """Inicializa o interpretador de comandos."""
        logger.info(" Inicializando Command Interpreter...")

        # Dicionário de intenções e padrões
        self.intents = self._load_intents()

        # Configurações
        self.confidence_threshold = 0.7
        self.max_alternatives = 3

        # Contexto atual
        self.current_context = "general"

        logger.info(" Command Interpreter inicializado com sucesso!")

    def _load_intents(self) -> Dict[str, Dict[str, Any]]:
        """Carrega definições de intenções."""
        intents = {
            "greeting": {
                "patterns": [
                    r"(oi|olá|bom dia|boa tarde|boa noite|e aí|eai|opa)( kamila| kammy)?",
                    r"kamila, (oi|olá|bom dia|boa tarde|boa noite)",
                    r"(iniciar|ligar|ativar) (a |kamila|assistente)"
                ],
                "responses": [
                    "Olá! Como posso ajudar?",
                    "Oi! Estou aqui para ajudar!",
                    "Olá! O que você precisa?",
                    "Oi! Pronto para ajudar!"
                ],
                "context": "general"
            },
            "goodbye": {
                "patterns": [
                    r"(tchau|adeus|até logo|até mais|até depois)",
                    r"(desligar|encerrar|sair|parar) (a |kamila|assistente)",
                    r"kamila, (tchau|adeus|até logo)"
                ],
                "responses": [
                    "Tchau! Foi bom conversar com você!",
                    "Até logo! Me chame quando precisar!",
                    "Tchau! Estarei aqui se precisar de ajuda!"
                ],
                "context": "general"
            },
            "time": {
                "patterns": [
                    r"que horas",
                    r"hora atual",
                    r"me diz a hora",
                    r"qual.*hora",
                    r"que.*horas"
                ],
                "responses": [
                    "Agora são {time}.",
                    "São {time} no momento."
                ],
                "context": "general"
            },
            "date": {
                "patterns": [
                    r"(que dia é hoje|qual é a data|data de hoje)",
                    r"kamila, (que dia é hoje|qual é a data)"
                ],
                "responses": [
                    "Hoje é {date}.",
                    "A data de hoje é {date}."
                ],
                "context": "general"
            },
            "weather": {
                "patterns": [
                    r"(como está o tempo|qual é a previsão|previsão do tempo)",
                    r"(clima|temperatura) (hoje|agora)",
                    r"kamila, (como está o tempo|previsão do tempo)"
                ],
                "responses": [
                    "Vou verificar a previsão do tempo para você.",
                    "Deixe-me checar como está o clima."
                ],
                "context": "general"
            },
            "help": {
                "patterns": [
                    r"(ajuda|help|o que você faz|como funciona)",
                    r"(quais são seus comandos|o que você sabe fazer)",
                    r"kamila, (ajuda|help|o que você faz)"
                ],
                "responses": [
                    "Posso ajudar com várias coisas! Pergunte sobre hora, data, clima, ou apenas converse comigo!",
                    "Estou aqui para ajudar! Posso responder perguntas sobre hora, data, clima e muito mais!"
                ],
                "context": "general"
            },
            "status": {
                "patterns": [
                    r"(como você está|está tudo bem|como vai)",
                    r"(status|estado|condição)",
                    r"kamila, (como você está|está tudo bem)"
                ],
                "responses": [
                    "Estou ótima! Pronta para ajudar!",
                    "Tudo bem por aqui! E você?",
                    "Estou funcionando perfeitamente!"
                ],
                "context": "general"
            },
            "music": {
                "patterns": [
                    r"(tocar música|colocar música|reproduzir)",
                    r"(música|canção|som)",
                    r"kamila, (tocar|colocar) (música|uma música)"
                ],
                "responses": [
                    "Vou tocar uma música para você!",
                    "Que tal ouvirmos uma música?"
                ],
                "context": "entertainment"
            },
            "lights": {
                "patterns": [
                    r"(acender|apagar|ligar|desligar) (a luz|luz|luzes)",
                    r"(luz|luzes) (on|off|ligada|desligada)",
                    r"kamila, (acende|apaga|liga|desliga) (a luz|luz)"
                ],
                "responses": [
                    "Controle de luzes ativado.",
                    "Vou ajustar as luzes para você."
                ],
                "context": "smart_home"
            },
            "volume": {
                "patterns": [
                    r"(aumentar|diminuir|alterar) (o volume|volume)",
                    r"(volume|falar) (mais alto|mais baixo)",
                    r"kamila, (aumenta|diminui) (o volume|volume)"
                ],
                "responses": [
                    "Ajustando o volume.",
                    "Volume alterado com sucesso."
                ],
                "context": "audio"
            },
            "camera_monitor": {
                "patterns": [
                    r"(capturar|tirar|fotografar) (uma foto|foto|imagem)",
                    r"(usar|abrir|ativar) (a câmera|câmera|webcam)",
                    r"kamila, (captura|tira) (uma foto|foto)"
                ],
                "responses": [
                    "Capturando imagem da câmera.",
                    "Vou tirar uma foto para você."
                ],
                "context": "camera"
            },
            "start_monitoring": {
                "patterns": [
                    r"(iniciar|começar|ativar) (monitoramento|vigilância|monitor)",
                    r"(ficar|vigiar|fiscalizar) (de olho|atenta|vigilante)",
                    r"kamila, (inicia|começa) (monitoramento|vigilância)"
                ],
                "responses": [
                    "Iniciando monitoramento de emergência.",
                    "Vou ficar vigiando por convulsões ou quedas."
                ],
                "context": "health"
            },
            "stop_monitoring": {
                "patterns": [
                    r"(parar|encerrar|desativar) (monitoramento|vigilância|monitor)",
                    r"(não|pare de) (vigiar|fiscalizar|monitorar)",
                    r"kamila, (para|encerra) (monitoramento|vigilância)"
                ],
                "responses": [
                    "Monitoramento de emergência parado.",
                    "Parando vigilância."
                ],
                "context": "health"
            },
            "monitoring_status": {
                "patterns": [
                    r"(status|estado) (do monitoramento|da vigilância)",
                    r"(está|como está) (monitorando|vigilando)",
                    r"kamila, (status|estado) (do monitoramento|da vigilância)"
                ],
                "responses": [
                    "Verificando status do monitoramento.",
                    "Deixe-me checar como está a vigilância."
                ],
                "context": "health"
            },
            "clear_history": {
                "patterns": [
                    r"(limpar|apagar|deletar) (histórico|memória|conversas)",
                    r"(esquecer|não lembrar) (do que falei|das conversas)",
                    r"kamila, (limpa|apaga) (histórico|memória)"
                ],
                "responses": [
                    "Limpando histórico de conversação.",
                    "Histórico apagado com sucesso."
                ],
                "context": "privacy"
            },
            "health_protocol": {
                "patterns": [
                    r"(ativar|iniciar|ligar) (protocolo de saúde|protocolo emergência|modo saúde)",
                    r"(preciso|me ajuda|socorro) (de saúde|emergência|médica)",
                    r"kamila, (ativa|inicia) (protocolo de saúde|protocolo emergência)"
                ],
                "responses": [
                    "Ativando protocolo de saúde completo.",
                    "Protocolo de emergência ativado. Estou cuidando de tudo."
                ],
                "context": "health"
            },
            "dim_lights": {
                "patterns": [
                    r"(diminuir|reduzir|baixar) (brilho|luz|luzes)",
                    r"(luz|luzes) (mais baixa|fraca|suave)",
                    r"kamila, (diminui|reduz) (o brilho|brilho)"
                ],
                "responses": [
                    "Diminuindo brilho para seu conforto.",
                    "Brilho reduzido para um ambiente mais tranquilo."
                ],
                "context": "health"
            },
            "lower_volume": {
                "patterns": [
                    r"(diminuir|reduzir|baixar) (volume|som|áudio)",
                    r"(volume|som) (mais baixo|baixo|suave)",
                    r"kamila, (diminui|reduz) (o volume|volume)"
                ],
                "responses": [
                    "Diminuindo volume do sistema.",
                    "Volume reduzido para ambiente mais tranquilo."
                ],
                "context": "health"
            },
            "emergency_contact": {
                "patterns": [
                    r"(chamar|contatar|ligar) (contatos|emergência|socorro)",
                    r"(notificar|avisar) (alguém|contatos|família)",
                    r"kamila, (chama|contata) (emergência|socorro)"
                ],
                "responses": [
                    "Notificando contatos de emergência.",
                    "Ajuda está a caminho."
                ],
                "context": "health"
            },
            "record_crisis": {
                "patterns": [
                    r"(registrar|anotar|gravar) (crise|ataque|episódio)",
                    r"(salvar|guardar) (detalhes|informações) (da crise|do episódio)",
                    r"kamila, (registra|anota) (crise|ataque)"
                ],
                "responses": [
                    "Registrando detalhes da crise.",
                    "Vou anotar isso para seu médico."
                ],
                "context": "health"
            },
            "daily_checkin": {
                "patterns": [
                    r"(check-in|checkin|verificação) (diário|diária|do dia)",
                    r"(como está|como foi) (seu dia|hoje)",
                    r"kamila, (faz|me faz) (check-in|verificação)"
                ],
                "responses": [
                    "Fazendo check-in diário de saúde.",
                    "Como você está se sentindo hoje?"
                ],
                "context": "health"
            },
            "medication_reminder": {
                "patterns": [
                    r"(lembrete|lembrar) (de medicação|remédio|remédios)",
                    r"(hora de tomar|tomar) (remédio|medicação)",
                    r"kamila, (lembra|lembrete) (medicação|remédio)"
                ],
                "responses": [
                    "Lembrete de medicação.",
                    "É hora de tomar seus remédios."
                ],
                "context": "health"
            }
        }

        return intents

    def interpret_command(self, command: str) -> Optional[str]:
        """
        Interpreta um comando de voz e retorna a intenção.

        Args:
            command (str): Comando a ser interpretado

        Returns:
            str: Intenção identificada ou None se não reconhecida
        """
        if not command or not command.strip():
            logger.warning("  Comando vazio para interpretar")
            return None

        try:
            logger.debug(f" Interpretando comando: {command}")

            # Normalizar comando
            normalized_command = self._normalize_command(command)

            # Buscar intenção
            intent, confidence = self._find_best_intent(normalized_command)

            if intent and confidence >= self.confidence_threshold:
                logger.info(f" Intenção identificada: {intent} (confiança: {confidence:.2f})")
                return intent
            else:
                logger.debug(f" Intenção não reconhecida (melhor: {intent}, confiança: {confidence:.2f})")
                return None

        except Exception as e:
            logger.error(f" Erro ao interpretar comando: {e}")
            return None

    def _normalize_command(self, command: str) -> str:
        """Normaliza o comando para facilitar matching."""
        # Converter para minúsculas
        normalized = command.lower().strip()

        # Remover pontuação desnecessária
        normalized = re.sub(r'[^\w\s]', ' ', normalized)

        # Remover palavras de preenchimento comuns
        filler_words = ['por favor', 'por gentileza', 'você pode', 'me diz', 'me fala']
        for word in filler_words:
            normalized = normalized.replace(word, '')

        # Remover espaços extras
        normalized = ' '.join(normalized.split())

        return normalized

    def _find_best_intent(self, command: str) -> Tuple[Optional[str], float]:
        """Encontra a melhor intenção para o comando."""
        best_intent = None
        best_confidence = 0.0

        for intent_name, intent_data in self.intents.items():
            confidence = self._calculate_confidence(command, intent_data["patterns"])

            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent_name

        return best_intent, best_confidence

    def _calculate_confidence(self, command: str, patterns: List[str]) -> float:
        """Calcula confiança de matching para um conjunto de padrões."""
        max_confidence = 0.0

        for pattern in patterns:
            try:
                # Busca por correspondência exata ou parcial
                if re.search(pattern, command, re.IGNORECASE):
                    # Calcular confiança baseada na cobertura do padrão
                    pattern_words = set(re.findall(r'\w+', pattern))
                    command_words = set(re.findall(r'\w+', command))

                    if pattern_words:
                        coverage = len(pattern_words.intersection(command_words)) / len(pattern_words)
                        max_confidence = max(max_confidence, coverage)

            except Exception as e:
                logger.debug(f"Erro no padrão {pattern}: {e}")
                continue

        return max_confidence

    def get_response_for_intent(self, intent: str, context: Dict[str, Any] = None) -> str:
        """
        Gera uma resposta para uma intenção específica.

        Args:
            intent (str): Intenção identificada
            context (Dict): Contexto adicional para personalização

        Returns:
            str: Resposta gerada
        """
        if intent not in self.intents:
            return "Desculpe, não sei como responder a isso."

        try:
            intent_data = self.intents[intent]
            responses = intent_data["responses"]

            # Selecionar resposta aleatória
            import random
            response_template = random.choice(responses)

            # Personalizar resposta baseada no contexto
            response = self._personalize_response(response_template, context if context is not None else {})

            # Atualizar contexto
            self.current_context = intent_data.get("context", "general")

            return response

        except Exception as e:
            logger.error(f" Erro ao gerar resposta: {e}")
            return "Ocorreu um erro ao processar sua solicitação."

    def _personalize_response(self, template: str, context: Dict[str, Any]) -> str:
        """Personaliza uma resposta com dados do contexto."""
        try:
            # Substituir placeholders comuns
            placeholders = {
                "{time}": datetime.now().strftime("%H:%M"),
                "{date}": datetime.now().strftime("%d/%m/%Y"),
                "{day}": datetime.now().strftime("%A"),
                "{user_name}": context.get("user_name", "você"),
                "{assistant_name}": "Kamila"
            }

            response = template
            for placeholder, value in placeholders.items():
                response = response.replace(placeholder, str(value))

            return response

        except Exception as e:
            logger.error(f" Erro ao personalizar resposta: {e}")
            return template

    def add_custom_intent(self, name: str, patterns: List[str], responses: List[str], context: str = "general"):
        """Adiciona uma nova intenção personalizada."""
        try:
            self.intents[name] = {
                "patterns": patterns,
                "responses": responses,
                "context": context
            }

            logger.info(f" Nova intenção adicionada: {name}")
            return True

        except Exception as e:
            logger.error(f" Erro ao adicionar intenção: {e}")
            return False

    def get_available_intents(self) -> List[str]:
        """Retorna lista de intenções disponíveis."""
        return list(self.intents.keys())

    def get_intent_details(self, intent: str) -> Optional[Dict[str, Any]]:
        """Retorna detalhes de uma intenção específica."""
        return self.intents.get(intent)

    def set_confidence_threshold(self, threshold: float):
        """Define o threshold de confiança."""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
        logger.info(f" Threshold de confiança definido: {threshold}")

    def get_context_suggestions(self, partial_command: str) -> List[str]:
        """Retorna sugestões de comandos baseadas no contexto atual."""
        suggestions = []

        try:
            # Buscar comandos que começam com o texto parcial
            partial_lower = partial_command.lower()

            for intent_name, intent_data in self.intents.items():
                for pattern in intent_data["patterns"]:
                    # Extrair exemplos do padrão
                    examples = self._extract_examples_from_pattern(pattern)
                    for example in examples:
                        if example.startswith(partial_lower) and len(example) > len(partial_lower):
                            suggestions.append(example)

            # Limitar sugestões
            return suggestions[:self.max_alternatives]

        except Exception as e:
            logger.error(f" Erro ao gerar sugestões: {e}")
            return []

    def _extract_examples_from_pattern(self, pattern: str) -> List[str]:
        """Extrai exemplos de comandos de um padrão regex."""
        examples = []

        try:
            # Tentar extrair alternativas do padrão
            alternatives = re.findall(r'\(([^)]+)\)', pattern)

            for alt in alternatives:
                # Dividir por |
                options = [opt.strip() for opt in alt.split('|')]
                examples.extend(options)

        except Exception as e:
            logger.debug(f"Erro ao extrair exemplos: {e}")

        return examples
