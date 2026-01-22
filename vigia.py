import win32con
import win32ts
import time
import requests
import logging

# Configuração do Logging
logging.basicConfig(filename='vigia.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Nome de usuário do Windows (verifique o seu no Gerenciador de Tarefas > Usuários)
USER_NAME = "kauen" 
KAMILA_API_URL = "http://127.0.0.1:5000/trigger_greeting"

logging.info("Vigia iniciado. Monitorando sessões de login.")
print("Vigia iniciado. Monitorando sessões de login.")

last_state = None

try:
    while True:
        # Pega a lista de sessões ativas no computador
        sessions = win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE)
        
        current_state = 'LOCKED' # Assume que está bloqueado por padrão
        
        for session in sessions:
            # Pega o nome do usuário da sessão
            user = win32ts.WTSQuerySessionInformation(win32ts.WTS_CURRENT_SERVER_HANDLE, 
                                                      session['SessionId'], 
                                                      win32ts.WTSUserName)
            
            # Pega o estado da conexão (ativo, desconectado, etc.)
            conn_state = session['State']

            # Verifica se é a sua sessão e se ela está ATIVA (não na tela de bloqueio)
            if user.lower() == USER_NAME.lower() and conn_state == 0: # 0 representa o estado WTSActive
                current_state = 'UNLOCKED'
                break

        # A mágica acontece aqui: detecta a TRANSIÇÃO de bloqueado para desbloqueado
        if current_state == 'UNLOCKED' and last_state == 'LOCKED':
            logging.info(f"Usuário '{USER_NAME}' acabou de desbloquear o computador!")
            print(f"Usuário '{USER_NAME}' acabou de desbloquear o computador!")
            
            try:
                logging.info("Notificando Kamila para fazer a saudação...")
                print("Notificando Kamila para fazer a saudação...")
                requests.post(KAMILA_API_URL, json={'user': USER_NAME})
                logging.info("Notificação enviada com sucesso.")
                print("Notificação enviada com sucesso.")
            except Exception as e:
                logging.error(f"Não foi possível notificar Kamila. Ela está rodando? Erro: {e}")
                print(f"Não foi possível notificar Kamila. Ela está rodando? Erro: {e}")

        # Atualiza o estado para a próxima verificação
        if current_state != last_state:
            last_state = current_state
            logging.info(f"Estado da sessão mudou para: {current_state}")
            print(f"Estado da sessão mudou para: {current_state}")

        # Verifica a cada 2 segundos
        time.sleep(2)

except KeyboardInterrupt:
    logging.info("Vigia encerrado.")
    print("Vigia encerrado.")