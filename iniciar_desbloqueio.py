import subprocess
import time
import os


SEGUNDOS_PARA_BLOQUEAR = 10 


print(f"ATENÇÃO: Este script irá iniciar o desbloqueio facial em {SEGUNDOS_PARA_BLOQUEAR} segundos.")
print("Assim que você rodar este script, bloqueie seu computador (Win + L) e olhe para a câmera.")
print("\nContando...")

# Contagem regressiva
for i in range(SEGUNDOS_PARA_BLOQUEAR, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("\nIniciando o script de desbloqueio facial agora!")

# Obtém o caminho do diretório onde este script está
try:
    # Obtém o caminho do diretório onde este script está
    project_directory = os.path.dirname(os.path.realpath(__file__))

    # Monta os caminhos completos
    python_executable = os.path.join(project_directory, ".venv", "Scripts", "python.exe")
    script_path = os.path.join(project_directory, "desbloqueio_facial.py")
    
    # Prepara o comando como uma lista de argumentos, que é a forma mais segura
    command_list = [python_executable, script_path]
    
    print(f"Executando lista de comandos: {command_list}")
    
    # O subprocess.Popen inicia o processo sem bloquear e lida com os caminhos corretamente
    subprocess.Popen(command_list)
    
    print("Script de desbloqueio foi iniciado em um novo processo.")

except Exception as e:
    print(f"\nERRO ao tentar iniciar o subprocesso: {e}")
    print("Verifique se os caminhos no script estão corretos.")