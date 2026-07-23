import sys
import os
import logging

# Configuração de paths para simular o ambiente da Kamila
project_root = r"c:\Users\Kaue_Martins\Desktop\Agent-S\Kamila"
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, '.kamila'))

logging.basicConfig(level=logging.INFO)

try:
    from core.computer_control import ComputerControl
    print("Tentando inicializar ComputerControl...")
    # Não vamos inicializar de fato se exigir chaves de API imediatas que podem falhar o teste
    # Mas vamos ver se os imports funcionam
    import gui_agents
    print(f"gui-agents importado com sucesso (versão {gui_agents.__version__})")
    
    # Check if AgentS3 can be imported
    from gui_agents.s3.agents.agent_s import AgentS3
    print("AgentS3 importado com sucesso.")
    
    print("✅ Verificação de dependências concluída!")
except Exception as e:
    print(f"❌ Erro na verificação: {e}")
    import traceback
    traceback.print_exc()
