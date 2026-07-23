#!/usr/bin/env python3
"""
Computer Control Module - Gateway for Kamila to control the OS.
Uses Agent S3 (gui-agents) technology.
"""

import os
import io
import logging
import pyautogui
from PIL import Image
from gui_agents.s3.agents.agent_s import AgentS3
from gui_agents.s3.agents.grounding import OSWorldACI

logger = logging.getLogger(__name__)

class ComputerControl:
    """Interface para controle do computador via Agente S3."""

    def __init__(self, platform="windows"):
        """
        Inicializa o controlador de computador.
        """
        logger.info("🛠️ Inicializando Computer Control (Agent S3)...")
        
        self.platform = platform
        self.width, self.height = pyautogui.size()
        
        # Parâmetros padrão (podem ser movidos para .env)
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model = os.getenv("LLM_MODEL", "gpt-4o")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Configuração do Agente S3
        engine_params = {
            "engine_type": self.provider,
            "model": self.model,
            "api_key": self.api_key
        }
        
        # Grounding Engine (usando o mesmo para simplicidade)
        engine_params_for_grounding = {
            "engine_type": self.provider,
            "model": self.model,
            "api_key": self.api_key,
            "grounding_width": self.width,
            "grounding_height": self.height,
        }
        
        try:
            self.grounding_agent = OSWorldACI(
                platform=self.platform,
                engine_params_for_generation=engine_params,
                engine_params_for_grounding=engine_params_for_grounding,
                width=self.width,
                height=self.height
            )
            
            self.agent = AgentS3(
                engine_params,
                self.grounding_agent,
                platform=self.platform
            )
            logger.info("✅ Computer Control inicializado com sucesso!")
        except Exception as e:
            logger.error(f"❌ Falha ao inicializar Computer Control: {e}")
            self.agent = None

    def execute_instruction(self, instruction: str):
        """
        Executa uma instrução de linguagem natural no computador.
        """
        if not self.agent:
            return "Erro: O sistema de controle de computador não foi inicializado corretamente."
            
        try:
            logger.info(f"🚀 Executando no PC: {instruction}")
            
            # Capturar screenshot atual
            screenshot = pyautogui.screenshot()
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            screenshot_bytes = buffered.getvalue()
            
            obs = {
                "screenshot": screenshot_bytes,
            }
            
            # Predição da ação
            info, action = self.agent.predict(instruction=instruction, observation=obs)
            
            if action and action[0]:
                logger.info(f"🖱️ Ação gerada: {action[0]}")
                # Executa o código Python gerado pelo grounding agent
                exec(action[0])
                return f"Entendido. Executei a ação: {instruction}"
            else:
                return "Não consegui determinar como executar essa ação no momento."
                
        except Exception as e:
            logger.error(f"❌ Erro ao executar instrução no PC: {e}")
            return f"Desculpe, ocorreu um erro ao tentar mexer no computador: {e}"

if __name__ == "__main__":
    # Teste simples
    logging.basicConfig(level=logging.INFO)
    from dotenv import load_dotenv
    load_dotenv('.kamila/.env')
    
    cc = ComputerControl()
    # cc.execute_instruction("Abrir o bloco de notas")
