# Documentação Técnica: Arquivo de Unidade `kamila.service` (`deployment/systemd/kamila.service`)

Esta documentação descreve as diretivas e o funcionamento do arquivo de unidade do **systemd** **`kamila.service`**, localizado em `deployment/systemd/kamila.service`. Este arquivo define o comportamento da assistente **Kamila** como um **serviço nativo do Linux**, controlando sua inicialização, recuperação de crashes e gerenciamento de logs.

---

## 1. Conteúdo do Arquivo `kamila.service`

```ini
[Unit]
Description=Assistente Virtual Kamila
After=network-online.target sound.target

[Service]
Type=simple
User=martins
Group=martins
# CAMINHOS CORRIGIDOS SEM ESPAÇOS
WorkingDirectory="/home/martins/Desktop/kamila_instalador_completo/kamila_avancada/.kamila"
ExecStart="/home/martins/Desktop/kamila_instalador_completo/venv/bin/python3" "/home/martins/Desktop/kamila_instalador_completo/kamila_avancada/.kamila/main.py"
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## 2. Análise Detalhada das Diretivas

### 2.1 Seção `[Unit]` (Dependências e Ordem de Carga)
- **`Description=Assistente Virtual Kamila`**: Nome do serviço exibido no `systemctl status` e nos logs do sistema.
- **`After=network-online.target sound.target`**:
  - **`network-online.target`**: Garante conexão ativa com a internet antes do início para permitir requisições à API do Gemini e AI Studio.
  - **`sound.target`**: Garante que o subsistema de áudio (ALSA/PulseAudio/PipeWire) já tenha inicializado as placas de som e microfones.

---

### 2.2 Seção `[Service]` (Execução e Resiliência)
- **`Type=simple`**: Modelo padrão onde o systemd considera o serviço ativo assim que o processo filho disparado por `ExecStart` é executado.
- **`User=martins` & `Group=martins`**: Executa o processo sob a conta do usuário não-root `martins`.
- **`WorkingDirectory="..."`**: Define o diretório de execução raiz para que o Python localize `.env`, logs e modelos vetoriais em caminhos relativos.
- **`ExecStart="..."`**: Especifica o caminho completo do executável Python no ambiente virtual e a classe principal `.kamila/main.py`.
- **`Restart=on-failure`**: Reinicia a assistente automaticamente caso o processo seja interrompido por um código de erro diferente de 0.
- **`RestartSec=5s`**: Aguarda um intervalo de 5 segundos antes de tentar reabrir o processo após uma falha.
- **`StandardOutput=journal` / `StandardError=journal`**: Redireciona mensagens do `print()` e do `logging` para o `journald`.

---

### 2.3 Seção `[Install]` (Alvo de Boot)
- **`WantedBy=multi-user.target`**: Habilita o serviço no *runlevel* padrão do sistema operacional (boot multi-usuário com/sem interface gráfica).

---

## 3. Comandos de Gerenciamento

```bash
# Copiar o arquivo para o repositório de serviços do systemd
sudo cp deployment/systemd/kamila.service /etc/systemd/system/kamila.service

# Notificar o systemd sobre o novo arquivo
sudo systemctl daemon-reload

# Ativar no boot do sistema
sudo systemctl enable kamila.service

# Iniciar o serviço imediatamente
sudo systemctl start kamila

# Consultar logs de execução ao vivo
journalctl -fu kamila
```
