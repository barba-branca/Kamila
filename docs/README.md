# 🤖 Kamila – Assistente Virtual com IA e Voz

Kamila é uma assistente virtual pessoal feita em Python com Processamento de Linguagem Natural (PLN), reconhecimento de voz, TTS, memória persistente, ações contextuais e ativa<h1 align="center">🤖 Kamila – Assistente Virtual com Voz e IA</h1>

<p align="center">
  Assistente pessoal em Python, ativada por voz, com memória emocional, ações inteligentes e TTS offline.
  <br> Feita para evoluir com propósito. 💡
</p>

<p align="center">
  <img src="https://img.shields.io/badge/feito%20com-Python-blue?style=flat-square">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=flat-square">
  <img src="https://img.shields.io/github/license/barba-branca/kamila?style=flat-square">
</p>

<p align="center">
  <img src="assets/demo.gif" alt="Demonstração da Kamila" width="600">
</p>

---
## ✨ Funcionalidades

- 🗣️ **Comando por voz** com ativação pela palavra-chave “Jarvis”
- 🎙️ **Reconhecimento de fala (STT)** com Google Speech API
- 🧠 **Interpretação de intenções** com NLP customizada
- 🔊 **Texto para fala (TTS)** usando `pyttsx3` (offline)
- 💾 **Memória persistente** em JSON com estados emocionais
- ⚙️ **Módulo de ações** personalizadas como:
  - Ver hora atual
  - Previsão do tempo (simulada ou real)
- 📦 Serviço systemd para **inicialização automática no Linux**
- 🐍 Projeto modular e extensível

### 🏥 **Sistema de Protocolo de Saúde (NOVO)**
- 🚨 **Monitoramento de Emergência**: Detecção automática de convulsões e quedas via webcam
- 🩺 **Protocolo de Saúde Completo**: Ativação de modo de emergência com múltiplas ações
- 💡 **Controle Ambiental**: Dimerização automática de luzes para conforto
- 🔊 **Controle de Volume**: Redução de estímulos sonoros durante crises
- 📞 **Contatos de Emergência**: Notificação automática de contatos configurados
- 📋 **Registro de Crises**: Documentação automática de eventos médicos
- 📅 **Check-in Diário**: Monitoramento diário de saúde
- 💊 **Lembretes de Medicação**: Alertas para horários de medicamentos
- 🔒 **Controle de Privacidade**: Limpeza segura do histórico de conversas
- 📊 **Status de Monitoramento**: Verificação em tempo real do estado do sistema

### 🛠️ **Recursos Avançados**
- 🤖 Integração com **Google Gemini AI** para respostas inteligentes
- 📹 **Monitoramento por Webcam** com detecção de movimento
- 🎵 **Controle de Mídia** e entretenimento

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Linux (testado no Ubuntu 22.04) ou Raspberry Pi OS
- Microfone
- Conta gratuita no [Picovoice Console](https://console.picovoice.ai/) para obter uma **Access Key**
- Conta no [Google AI Studio](https://aistudio.google.com/) para obter uma **API Key do Google Generative AI**
- Para versão avançada: Arduino Uno/Nano, sensores (temperatura, toque), LEDs RGB

### Configuração das variáveis de ambiente

Antes de executar Kamila, você precisa configurar as variáveis de ambiente. Um exemplo de arquivo `.env` está disponível em `.kamila/.env.example`. Copie este arquivo para `.kamila/.env` e preencha com suas chaves de API reais.

### Instalação automatizada (Linux)

```bash
git clone https://github.com/barba-branca/kamila.git
cd kamila
chmod +x install_kamila.sh
./install_kamila.sh
```

Após a instalação, Kamila será iniciada automaticamente com o sistema.
Para iniciar manualmente:
systemctl --user start kamila

### Configuração para Raspberry Pi e Arduino

#### Hardware Necessário
- Raspberry Pi 4/5 com Raspberry Pi OS
- Arduino Uno/Nano
- Sensor de temperatura (DHT11)
- Sensor de toque capacitivo
- LED RGB
- Cabo USB para comunicação serial

#### Passos de Configuração
1. **Instalar dependências no Raspberry Pi:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev libportaudio2 libasound2-dev
   pip install -r requirements.txt
   ```

2. **Configurar Arduino:**
   - Conecte sensores e LED ao Arduino
   - Faça upload do sketch `arduino_sketch.ino` (criar arquivo com código para ler sensores e controlar LED via serial)
   - Porta serial padrão: `/dev/ttyUSB0`

3. **Instalar IPFS (opcional para backup):**
   ```bash
   wget https://dist.ipfs.tech/kubo/v0.20.0/kubo_v0.20.0_linux-arm64.tar.gz
   tar -xvzf kubo_v0.20.0_linux-arm64.tar.gz
   cd kubo
   sudo bash install.sh
   ipfs init
   ipfs daemon &
   ```

4. **Executar Kamila:**
   ```bash
   cd kamila_avancada/.kamila
   python main.py
   ```

## 🗣️ Comandos de Voz

### **Comandos Gerais**
- "Kamila, que horas são?" - Ver hora atual
- "Kamila, qual é a previsão do tempo?" - Previsão do tempo
- "Kamila, toca uma música" - Controle de mídia
- "Kamila, me lembre de..." - Criar lembretes

### **🏥 Comandos do Protocolo de Saúde (NOVOS)**
- "Kamila, ativa protocolo de saúde" - Ativa modo de emergência completo
- "Kamila, diminui o brilho" - Dimeriza luzes para conforto
- "Kamila, diminui o volume" - Reduz estímulos sonoros
- "Kamila, chama emergência" - Notifica contatos de emergência
- "Kamila, registra crise" - Documenta evento médico
- "Kamila, faz check-in diário" - Monitoramento diário de saúde
- "Kamila, lembrete de medicação" - Alerta para medicamentos
- "Kamila, inicia monitoramento" - Ativa monitoramento por webcam
- "Kamila, para monitoramento" - Desativa monitoramento
- "Kamila, status do monitoramento" - Verifica estado do sistema
- "Kamila, limpa histórico" - Remove conversas para privacidade

🛠️ Estrutura do Projeto
```bash
kamila/
│
├── .kamila/              # Módulos internos da assistente
│   ├── main.py           # Loop principal (Porcupine + interação)
│   ├── core/
│   │   ├── actions.py    # Ações mapeadas por intenção
│   │   ├── interpreter.py# Interpretação das falas
│   │   ├── memory_manager.py # Gerenciamento de memória persistente
│   │   ├── stt_engine.py # Reconhecimento de voz (Google)
│   │   └── tts_engine.py # Fala (pyttsx3)
│
├── install_kamila.sh     # Script de instalação automatizada
├── kamila.service        # Arquivo systemd
├── memory.json           # Estado salvo da memória
└── README.md             # Este arquivo
```
🧪 Testes rápidos

### **Teste Básico**
Testar microfone com log:
```bash
python3 teste_com_log.py
```

### **Teste de Voz**
Testar funcionalidades de voz:
```bash
python test_voice_kamila.py
```

### **Teste do Protocolo de Saúde**
Testar funcionalidades de saúde:
```bash
python -c "
from .kamila.core.actions import ActionManager
from .kamila.core.tts_engine import TTSEngine
tts = TTSEngine()
actions = ActionManager(tts)
print('Testando ações de saúde...')
actions.execute_action('health_protocol', 'ativa protocolo de saúde')
actions.execute_action('dim_lights', 'diminui o brilho')
actions.execute_action('lower_volume', 'diminui o volume')
print('✅ Teste do protocolo de saúde concluído!')
"
```


📈 Roadmap
 Integração com Vosk (STT offline)

 Personalidade emocional adaptativa

 Acesso a APIs externas reais (clima, calendário, música)

 Embark em hardware (ESP32 ou Raspberry Pi)

 Comandos visuais (controle do SO)

🤝 Contribuições
Contribuições são bem-vindas!
Para colaborar:

1. Faça um fork

2. Crie uma branch (git checkout -b nova-funcionalidade)

3. Commit suas mudanças (git commit -m 'feat: adiciona nova funcionalidade')

4. Push para a branch (git push origin nova-funcionalidade)

5. Abra um Pull Request

👨‍💻 Autor
Desenvolvido por Kauê Martins – @kauemartinsofc
GitHub: barba-branca
Twitter: @Kauemartins23

📝 Licença
Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.

“Kamila nasceu para transformar comandos em conversas, e conversas em conexão real.”
— Kauê Martins