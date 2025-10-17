"""
Memory Manager - Gerenciamento de Memória para Kamila
Sistema de memória persistente para personalização da assistente.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class MemoryManager:
    """Gerencia a memória persistente da assistente."""

    def __init__(self):
        """Inicializa o gerenciador de memória."""
        logger.info("Inicializando Memory Manager...")

        self.memory_file = "data/memory.json"
        self.memory_data = self._load_memory()

        # Configurações padrão
        self.max_interactions = 1000  # Máximo de interações armazenadas
        self.max_memory_age = 30      # Dias para manter memórias

        logger.info(" Memory Manager inicializado com sucesso!")

    def _load_memory(self) -> Dict[str, Any]:
        """Carrega dados de memória do arquivo JSON."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f" Memória carregada: {len(data.get('interactions', []))} interações")
                    return data
            else:
                logger.info(" Arquivo de memória não encontrado, criando novo")
                return self._create_default_memory()

        except Exception as e:
            logger.error(f" Erro ao carregar memória: {e}")
            return self._create_default_memory()

    def _create_default_memory(self) -> Dict[str, Any]:
        """Cria estrutura de memória padrão."""
        return {
            "user_profile": {
                "name": None,
                "preferences": {},
                "created_at": datetime.now().isoformat(),
                "last_interaction": None
            },
            "interactions": [],
            "health_log": [],  
            "learned_commands": {},
            "statistics": {
                "total_interactions": 0,
                "successful_commands": 0,
                "failed_commands": 0,
                "wake_ups": 0
            }
        }

    def _save_memory(self):
        """Salva dados de memória no arquivo JSON."""
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)

            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, indent=2, ensure_ascii=False)

            logger.debug("Memória salva com sucesso")

        except Exception as e:
            logger.error(f" Erro ao salvar memória: {e}")

    def get_user_name(self) -> Optional[str]:
        """Retorna o nome do usuário."""
        return self.memory_data["user_profile"].get("name")

    def set_user_name(self, name: str):
        """Define o nome do usuário."""
        if name and name.strip():
            self.memory_data["user_profile"]["name"] = name.strip()
            self._save_memory()
            logger.info(f"Nome do usuário definido: {name}")

    def update_interaction(self):
        """Atualiza timestamp da última interação."""
        self.memory_data["user_profile"]["last_interaction"] = datetime.now().isoformat()
        self._save_memory()

    def add_interaction(self, command: str, intent: str, response: str):
        """
        Adiciona uma nova interação à memória.

        Args:
            command (str): Comando dado pelo usuário
            intent (str): Intenção interpretada
            response (str): Resposta da assistente
        """
        try:
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "intent": intent,
                "response": response,
                "success": bool(response)
            }

            # Adicionar à lista de interações
            self.memory_data["interactions"].append(interaction)

            # Atualizar estatísticas
            self.memory_data["statistics"]["total_interactions"] += 1
            if response:
                self.memory_data["statistics"]["successful_commands"] += 1
            else:
                self.memory_data["statistics"]["failed_commands"] += 1

            # Limitar número de interações armazenadas
            if len(self.memory_data["interactions"]) > self.max_interactions:
                # Remover interações mais antigas
                self.memory_data["interactions"] = self.memory_data["interactions"][-self.max_interactions:]

            # Salvar memória
            self._save_memory()

            logger.debug(f" Interação adicionada: {intent}")

        except Exception as e:
            logger.error(f" Erro ao adicionar interação: {e}")

    def get_recent_interactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna interações recentes."""
        return self.memory_data["interactions"][-limit:] if self.memory_data["interactions"] else []

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        return self.memory_data["statistics"].copy()

    def learn_command(self, command: str, intent: str, response: str):
        """
        Aprende um novo comando personalizado.

        Args:
            command (str): Comando a ser aprendido
            intent (str): Intenção do comando
            response (str): Resposta padrão para o comando
        """
        try:
            self.memory_data["learned_commands"][command.lower()] = {
                "intent": intent,
                "response": response,
                "learned_at": datetime.now().isoformat(),
                "usage_count": 0
            }

            self._save_memory()
            logger.info(f" Comando aprendido: {command} -> {intent}")

        except Exception as e:
            logger.error(f" Erro ao aprender comando: {e}")

    def get_learned_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Retorna um comando aprendido se existir."""
        return self.memory_data["learned_commands"].get(command.lower())

    def increment_command_usage(self, command: str):
        """Incrementa contador de uso de um comando aprendido."""
        if command.lower() in self.memory_data["learned_commands"]:
            self.memory_data["learned_commands"][command.lower()]["usage_count"] += 1
            self._save_memory()

    def get_user_preferences(self) -> Dict[str, Any]:
        """Retorna preferências do usuário."""
        return self.memory_data["user_profile"].get("preferences", {})

    def set_user_preference(self, key: str, value: Any):
        """Define uma preferência do usuário."""
        self.memory_data["user_profile"]["preferences"][key] = value
        self._save_memory()
        logger.debug(f"  Preferência definida: {key} = {value}")

    def get_memory_summary(self) -> Dict[str, Any]:
        """Retorna resumo da memória."""
        return {
            "user_name": self.get_user_name(),
            "total_interactions": self.memory_data["statistics"]["total_interactions"],
            "learned_commands": len(self.memory_data["learned_commands"]),
            "last_interaction": self.memory_data["user_profile"].get("last_interaction"),
            "memory_age_days": (datetime.now() - datetime.fromisoformat(
                self.memory_data["user_profile"]["created_at"]
            )).days if self.memory_data["user_profile"].get("created_at") else 0
        }
    def add_health_event(self, event_type: str, details: Dict[str, Any]):
        """
        Adiciona um novo evento ao log de saúde.

        Args:
            event_type (str): O tipo de evento (ex: 'crise', 'medicacao', 'humor').
            details (Dict): Um dicionário com detalhes sobre o evento.
        """
        try:
            health_event = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "details": details
            }

            # Garante que a chave 'health_log' exista
            if "health_log" not in self.memory_data:
                self.memory_data["health_log"] = []
            
            self.memory_data["health_log"].append(health_event)
            self._save_memory()
            logger.info(f"Novo evento de saúde registrado: {event_type}")

        except Exception as e:
            logger.error(f"Erro ao adicionar evento de saúde: {e}")
            
    def cleanup_old_memories(self):
        """Remove memórias antigas baseado na configuração."""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.max_memory_age)

            # Filtrar interações antigas
            original_count = len(self.memory_data["interactions"])
            self.memory_data["interactions"] = [
                interaction for interaction in self.memory_data["interactions"]
                if datetime.fromisoformat(interaction["timestamp"]) > cutoff_date
            ]

            removed_count = original_count - len(self.memory_data["interactions"])

            if removed_count > 0:
                logger.info(f" Removidas {removed_count} interações antigas")
                self._save_memory()

        except Exception as e:
            logger.error(f" Erro ao limpar memórias antigas: {e}")

    def export_memory(self, filepath: str):
        """Exporta memória para arquivo."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, indent=2, ensure_ascii=False)
            logger.info(f" Memória exportada para: {filepath}")
        except Exception as e:
            logger.error(f" Erro ao exportar memória: {e}")

    def import_memory(self, filepath: str):
        """Importa memória de arquivo."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)

            # Mesclar dados importados com dados existentes
            self.memory_data["interactions"].extend(imported_data.get("interactions", []))
            self.memory_data["learned_commands"].update(imported_data.get("learned_commands", {}))
            self.memory_data["statistics"]["total_interactions"] += imported_data.get("statistics", {}).get("total_interactions", 0)

            self._save_memory()
            logger.info(f" Memória importada de: {filepath}")

        except Exception as e:
            logger.error(f" Erro ao importar memória: {e}")

    def reset_memory(self):
        """Reseta toda a memória."""
        try:
            self.memory_data = self._create_default_memory()
            self._save_memory()
            logger.info(" Memória resetada com sucesso")
        except Exception as e:
            logger.error(f" Erro ao resetar memória: {e}")
