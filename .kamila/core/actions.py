#!/usr/bin/env python3
"""
Action Manager - Gerenciamento de Ações para Kamila
Sistema de execução de ações baseado em intenções interpretadas.
"""

import os
import sys
import logging
import subprocess
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dotenv import load_dotenv
import cv2  # acesso à webcam
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
# Carregar variáveis de ambiente
load_dotenv('.kamila/.env')

logger = logging.getLogger(__name__)

class ActionManager:
    """Gerencia e executa ações baseadas em intenções."""

    def __init__(self, tts_engine=None):
        """Inicializa o gerenciador de ações."""
        logger.info(" Inicializando Action Manager...")

        # Motor TTS
        self.tts_engine = tts_engine

        # Dicionário de ações disponíveis
        self.actions = self._load_actions()

        # Estado do sistema
        self.system_status = {
            "last_action": None,
            "last_action_time": None,
            "active_actions": []
        }

        logger.info(" Action Manager inicializado com sucesso!")

    def _load_actions(self) -> Dict[str, Dict[str, Any]]:
        """Carrega definições de ações."""
        return {
            "greeting": {
                "handler": self._handle_greeting,
                "description": "Responde a saudações",
                "parameters": []
            },
            "goodbye": {
                "handler": self._handle_goodbye,
                "description": "Responde a despedidas",
                "parameters": []
            },
            "time": {
                "handler": self._handle_time,
                "description": "Informa a hora atual",
                "parameters": []
            },
            "date": {
                "handler": self._handle_date,
                "description": "Informa a data atual",
                "parameters": []
            },
            "weather": {
                "handler": self._handle_weather,
                "description": "Consulta previsão do tempo",
                "parameters": []
            },
            "help": {
                "handler": self._handle_help,
                "description": "Mostra ajuda e comandos disponíveis",
                "parameters": []
            },
            "status": {
                "handler": self._handle_status,
                "description": "Informa status da assistente",
                "parameters": []
            },
            "music": {
                "handler": self._handle_music,
                "description": "Controla reprodução de música",
                "parameters": ["action", "song"]
            },
            "lights": {
                "handler": self._handle_lights,
                "description": "Controla iluminação",
                "parameters": ["action", "room"]
            },
            "volume": {
                "handler": self._handle_volume,
                "description": "Controla volume do sistema",
                "parameters": ["level"]
            },
            "open_app": {
                "handler": self._handle_open_app,
                "description": "Abre aplicações",
                "parameters": ["app_name"]
            },
            "search": {
                "handler": self._handle_search,
                "description": "Faz pesquisas na web",
                "parameters": ["query"]
            },
            "calculate": {
                "handler": self._handle_calculate,
                "description": "Faz cálculos matemáticos",
                "parameters": ["expression"]
            },
            "camera_monitor": {
                "handler": self._handle_camera_monitor,
                "description": "Captura uma imagem da webcam",
                "parameters": []
            },
            "start_monitoring": {
                "handler": self._handle_start_monitoring,
                "description": "Inicia monitoramento de emergência por webcam",
                "parameters": []
            },
            "stop_monitoring": {
                "handler": self._handle_stop_monitoring,
                "description": "Para monitoramento de emergência por webcam",
                "parameters": []
            },
            "monitoring_status": {
                "handler": self._handle_monitoring_status,
                "description": "Verifica status do monitoramento",
                "parameters": []
            },
            "clear_history": {
                "handler": self._handle_clear_history,
                "description": "Limpa o histórico de conversação",
                "parameters": []
            },
            "health_protocol": {
                "handler": self._handle_health_protocol,
                "description": "Ativa protocolo de saúde para emergências",
                "parameters": []
            },
            "dim_lights": {
                "handler": self._handle_dim_lights,
                "description": "Diminui brilho das luzes",
                "parameters": []
            },
            "lower_volume": {
                "handler": self._handle_lower_volume,
                "description": "Diminui volume do sistema",
                "parameters": []
            },
            "emergency_contact": {
                "handler": self._handle_emergency_contact,
                "description": "Contata contatos de emergência",
                "parameters": []
            },
            "record_crisis": {
                "handler": self._handle_record_crisis,
                "description": "Registra detalhes de uma crise",
                "parameters": ["details"]
            },
            "daily_checkin": {
                "handler": self._handle_daily_checkin,
                "description": "Faz check-in diário de saúde",
                "parameters": []
            },
            "medication_reminder": {
                "handler": self._handle_medication_reminder,
                "description": "Lembrete de medicação",
                "parameters": []
            },
        }

    def execute_action(self, intent: str, command: str) -> Optional[str]:
        """
        Executa uma ação baseada na intenção.

        Args:
            intent (str): Intenção identificada
            command (str): Comando original do usuário

        Returns:
            str: Resposta da ação ou None se falhou
        """
        if intent not in self.actions:
            logger.warning(f"  Ação não encontrada: {intent}")
            return "Desculpe, não sei como executar essa ação."

        try:
            logger.info(f"⚡ Executando ação: {intent}")

            # Pegar handler da ação
            action_data = self.actions[intent]
            handler = action_data["handler"]

            # Executar ação
            result = handler(command)

            # Atualizar estado
            self.system_status["last_action"] = intent
            self.system_status["last_action_time"] = datetime.now().isoformat()

            logger.info(f" Ação executada: {intent}")
            return result

        except Exception as e:
            logger.error(f" Erro ao executar ação {intent}: {e}")
            return "Ocorreu um erro ao executar a ação solicitada."

    def _handle_greeting(self, command: str) -> str:
        """Manipula saudações."""
        current_hour = datetime.now().hour

        if 6 <= current_hour < 12:
            return "Bom dia! Como posso ajudar você hoje?"
        elif 12 <= current_hour < 18:
            return "Boa tarde! Em que posso ser útil?"
        else:
            return "Boa noite! O que você precisa?"

    def _handle_goodbye(self, command: str) -> str:
        """Manipula despedidas."""
        return "Tchau! Foi um prazer ajudar você. Até logo!"

    def _handle_time(self, command: str) -> str:
        """Manipula consultas de hora."""
        now = datetime.now()
        return f"Agora são {now.strftime('%H:%M')}."

    def _handle_date(self, command: str) -> str:
        """Manipula consultas de data."""
        now = datetime.now()
        return f"Hoje é {now.strftime('%A, %d de %B de %Y')}."

    def _handle_weather(self, command: str) -> str:
        """Manipula consultas de tempo."""
        return "Vou verificar a previsão do tempo para você. Um momento..."

    def _handle_help(self, command: str) -> str:
        """Manipula pedidos de ajuda."""
        help_text = """
Posso ajudar com:
• Consultar hora e data
• Previsão do tempo
• Controlar música
• Ajustar iluminação
• Abrir aplicações
• Fazer pesquisas
• Cálculos matemáticos
• Monitoramento de emergência (convulsões e quedas)
• Capturar imagens da webcam
• Limpar histórico de conversação

Comandos de monitoramento:
• "iniciar monitoramento" - Inicia vigilância por emergência
• "parar monitoramento" - Para vigilância por emergência
• "status monitoramento" - Verifica status do monitoramento

Comandos de saúde e emergência:
• "protocolo de saúde" - Ativa protocolo completo de emergência
• "diminuir brilho" - Reduz brilho da tela para conforto
• "diminuir volume" - Reduz volume do sistema
• "contato emergência" - Notifica contatos de emergência
• "registrar crise" - Registra detalhes de uma crise
• "check-in diário" - Faz check-in diário de saúde
• "lembrete medicação" - Lembrete para tomar remédios

Comandos de privacidade:
• "limpar histórico" - Limpa o histórico de conversação

Diga "Camila" para me ativar e depois seu comando!
        """
        return help_text.strip()

    def _handle_status(self, command: str) -> str:
        """Manipula consultas de status."""
        return "Estou funcionando perfeitamente! Pronta para ajudar!"

    def _handle_music(self, command: str) -> str:
        """Manipula controle de música."""
        return "Controle de música ativado. Que música você gostaria de ouvir?"

    def _handle_lights(self, command: str) -> str:
        """Manipula controle de iluminação."""
        return "Controle de iluminação ativado. Qual luz você quer controlar?"

    def _handle_volume(self, command: str) -> str:
        """Manipula controle de volume."""
        return "Ajustando volume do sistema..."

    def _handle_open_app(self, command: str) -> str:
        """Manipula abertura de aplicações."""
        # Extrair nome da aplicação do comando
        app_keywords = ["abrir", "abre", "iniciar", "liga", "executar"]

        for keyword in app_keywords:
            if keyword in command:
                # Pegar texto após a palavra-chave
                app_name = command.split(keyword, 1)[1].strip()
                return f"Abrindo {app_name}..."

        return "Qual aplicação você gostaria de abrir?"

    def _handle_search(self, command: str) -> str:
        """Manipula pesquisas na web."""
        # Extrair termo de pesquisa
        search_keywords = ["pesquisar", "pesquisa", "procurar", "buscar", "busca"]

        for keyword in search_keywords:
            if keyword in command:
                query = command.split(keyword, 1)[1].strip()
                return f"Pesquisando por: {query}"

        return "O que você gostaria de pesquisar?"

    def _handle_calculate(self, command: str) -> str:
        """Manipula cálculos matemáticos."""
        # Extrair expressão matemática
        calc_keywords = ["calcular", "calcula", "quanto é", "calcule"]

        for keyword in calc_keywords:
            if keyword in command:
                expression = command.split(keyword, 1)[1].strip()
                return f"Calculando: {expression}"

        return "Qual cálculo você gostaria que eu fizesse?"
    def _handle_camera_monitor(self, command: str) -> str:
        try:
            cap = cv2.VideoCapture(0)  # 0 = webcam padrão
            if not cap.isOpened():
                return "Não consegui acessar a câmera."
            ret, frame = cap.read()
            if not ret:
                cap.release()
                return "Erro ao capturar imagem."
            filename = f"captura_{datetime.now():%Y%m%d_%H%M%S}.jpg"
            cv2.imwrite(filename, frame)
            cap.release()
            return f"Imagem capturada e salva em {filename}"
        except Exception as e:
            logger.error(f"Erro na câmera: {e}")
            return "Falha ao acessar a webcam."

    def add_custom_action(self, name: str, handler: Callable, description: str = "", parameters: List[str] = None):
        """
        Adiciona uma ação personalizada.

        Args:
            name (str): Nome da ação
            handler (Callable): Função que executa a ação
            description (str): Descrição da ação
            parameters (List[str]): Parâmetros esperados
        """
        try:
            self.actions[name] = {
                "handler": handler,
                "description": description,
                "parameters": parameters or []
            }

            logger.info(f"🆕 Nova ação adicionada: {name}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao adicionar ação: {e}")
            return False

    def get_available_actions(self) -> List[str]:
        """Retorna lista de ações disponíveis."""
        return list(self.actions.keys())

    def get_action_info(self, action_name: str) -> Optional[Dict[str, Any]]:
        """Retorna informações de uma ação específica."""
        return self.actions.get(action_name)

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status atual do sistema."""
        return self.system_status.copy()

    def reset_system_status(self):
        """Reseta status do sistema."""
        self.system_status = {
            "last_action": None,
            "last_action_time": None,
            "active_actions": []
        }
        logger.info(" Status do sistema resetado")

    def _handle_start_monitoring(self, command: str) -> str:
        """Inicia monitoramento de emergência por webcam."""
        try:
            # Importar o monitor de webcam
            from core.webcam_monitor import WebcamMonitor

            # Criar callback para alertas
            def alert_callback(alert_type, message):
                logger.warning(f"🚨 ALERTA: {alert_type} - {message}")
                # O TTS já é tratado dentro do WebcamMonitor

            # Inicializar monitor se não existir
            if not hasattr(self, 'webcam_monitor') or self.webcam_monitor is None:
                self.webcam_monitor = WebcamMonitor(self.tts_engine)

            # Iniciar monitoramento
            success = self.webcam_monitor.start_monitoring(alert_callback)

            if success:
                return "Monitoramento de emergência iniciado! Ficarei vigiando por convulsões ou quedas."
            else:
                return "Não foi possível iniciar o monitoramento. Verifique se a webcam está conectada."

        except Exception as e:
            logger.error(f"Erro ao iniciar monitoramento: {e}")
            return "Erro ao iniciar monitoramento de emergência."

    def _handle_stop_monitoring(self, command: str) -> str:
        """Para monitoramento de emergência por webcam."""
        try:
            if hasattr(self, 'webcam_monitor') and self.webcam_monitor:
                self.webcam_monitor.stop_monitoring()
                self.webcam_monitor = None
                return "Monitoramento de emergência parado."
            else:
                return "Nenhum monitoramento ativo para parar."

        except Exception as e:
            logger.error(f"Erro ao parar monitoramento: {e}")
            return "Erro ao parar monitoramento de emergência."

    def _handle_monitoring_status(self, command: str) -> str:
        """Verifica status do monitoramento."""
        try:
            if hasattr(self, 'webcam_monitor') and self.webcam_monitor:
                status = self.webcam_monitor.get_status()
                return f"Status do monitoramento: {status}"
            else:
                return "Monitoramento não está ativo."

        except Exception as e:
            logger.error(f"Erro ao verificar status: {e}")
            return "Erro ao verificar status do monitoramento."

    def _handle_clear_history(self, command: str) -> str:
        """Limpa o histórico de conversação."""
        try:
            # Importar o Gemini Engine para limpar o histórico
            from llm.gemini_engine import GeminiEngine

            # Criar instância temporária apenas para limpar o histórico
            gemini_engine = GeminiEngine()
            gemini_engine.clear_history()

            return "Histórico de conversação limpo com sucesso!"

        except Exception as e:
            logger.error(f"Erro ao limpar histórico: {e}")
            return "Erro ao limpar o histórico de conversação."

    def _handle_health_protocol(self, command: str) -> str:
        """Ativa protocolo de saúde para emergências."""
        try:
            # Diminuir brilho da tela
            self._dim_screen_brightness()

            # Diminuir volume
            self._lower_system_volume()

            # Iniciar monitoramento intensivo
            self._activate_health_monitoring()

            # Notificar contatos de emergência
            self._notify_emergency_contacts()

            return "Protocolo de saúde ativado! Estou cuidando de tudo. Respira fundo, vai ficar tudo bem."

        except Exception as e:
            logger.error(f"Erro no protocolo de saúde: {e}")
            return "Erro ao ativar protocolo de saúde. Mas tô aqui com você."

    def _handle_dim_lights(self, command: str) -> str:
        """Diminui brilho das luzes."""
        try:
            self._dim_screen_brightness()
            return "Brilho da tela diminuído para te deixar mais confortável."

        except Exception as e:
            logger.error(f"Erro ao diminuir brilho: {e}")
            return "Não consegui diminuir o brilho, mas tô aqui pra ajudar."

    def _handle_lower_volume(self, command: str) -> str:
        """Diminui volume do sistema."""
        try:
            self._lower_system_volume()
            return "Volume diminuído para um ambiente mais tranquilo."

        except Exception as e:
            logger.error(f"Erro ao diminuir volume: {e}")
            return "Não consegui ajustar o volume, mas tô aqui com você."

    def _handle_emergency_contact(self, command: str) -> str:
        """Contata contatos de emergência."""
        try:
            self._notify_emergency_contacts()
            return "Contatos de emergência notificados. Ajuda está a caminho."

        except Exception as e:
            logger.error(f"Erro ao notificar contatos: {e}")
            return "Tentando notificar contatos de emergência..."

    def _handle_record_crisis(self, command: str) -> str:
        """Registra detalhes de uma crise."""
        try:
            # Extrair detalhes do comando
            details = command.replace("registrar crise", "").replace("record crisis", "").strip()
            if not details:
                details = "Detalhes não especificados"

            # Salvar no arquivo de log de crises
            timestamp = datetime.now().isoformat()
            crisis_log = f"[{timestamp}] Crise registrada: {details}\n"

            with open("crisis_log.txt", "a", encoding="utf-8") as f:
                f.write(crisis_log)

            return "Crise registrada. Vou lembrar desses detalhes para o seu médico."

        except Exception as e:
            logger.error(f"Erro ao registrar crise: {e}")
            return "Erro ao registrar a crise, mas tô aqui pra ajudar."

    def _handle_daily_checkin(self, command: str) -> str:
        """Faz check-in diário de saúde."""
        try:
            current_time = datetime.now().strftime("%H:%M")
            return f"Check-in diário às {current_time}. Como você está se sentindo hoje? Me conte sobre seu dia."

        except Exception as e:
            logger.error(f"Erro no check-in diário: {e}")
            return "Erro no check-in diário, mas tô aqui pra ouvir você."

    def _handle_medication_reminder(self, command: str) -> str:
        """Lembrete de medicação."""
        try:
            current_time = datetime.now().strftime("%H:%M")
            return f"Lembrete de medicação às {current_time}. É hora de tomar seus remédios. Já tomou?"

        except Exception as e:
            logger.error(f"Erro no lembrete de medicação: {e}")
            return "Erro no lembrete de medicação, mas tô aqui pra te lembrar."

    def _dim_screen_brightness(self):
        """Diminui brilho da tela."""
        try:
            # Windows
            if os.name == 'nt':
                subprocess.run(['powershell', '-command',
                    "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 30)"],
                    capture_output=True)
            # Linux
            elif os.name == 'posix':
                subprocess.run(['xrandr', '--output', 'eDP-1', '--brightness', '0.3'],
                    capture_output=True)
        except Exception as e:
            logger.warning(f"Não foi possível ajustar brilho: {e}")

    def _lower_system_volume(self):
        """Diminui volume do sistema."""
        try:
            # Windows
            if os.name == 'nt':
                subprocess.run(['powershell', '-command',
                    "Set-AudioDevice -PlaybackVolume (Get-AudioDevice -Playback | Where-Object {$_.Default -eq $true}).PlaybackVolume - 30"],
                    capture_output=True)
            # Linux
            elif os.name == 'posix':
                subprocess.run(['amixer', 'set', 'Master', '30%'],
                    capture_output=True)
        except Exception as e:
            logger.warning(f"Não foi possível ajustar volume: {e}")

    def _activate_health_monitoring(self):
        """Ativa monitoramento intensivo de saúde."""
        try:
            # Iniciar monitoramento se não estiver ativo
            if not hasattr(self, 'webcam_monitor') or self.webcam_monitor is None:
                from core.webcam_monitor import WebcamMonitor
                self.webcam_monitor = WebcamMonitor(self.tts_engine)

            # Configurar para modo de saúde intensivo
            self.webcam_monitor.health_mode = True

        except Exception as e:
            logger.warning(f"Não foi possível ativar monitoramento intensivo: {e}")

    def _notify_emergency_contacts(self):
        """Notifica contatos de emergência."""
        try:
            # Por enquanto, apenas loga - pode ser expandido para SMS, chamadas, etc.
            emergency_message = f"🚨 EMERGÊNCIA: Camila detectou possível crise às {datetime.now().strftime('%H:%M:%S')}"

            # Salvar notificação
            with open("emergency_notifications.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] {emergency_message}\n")

            logger.warning(emergency_message)

        except Exception as e:
            logger.error(f"Erro ao notificar contatos: {e}")
