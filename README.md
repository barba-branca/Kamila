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

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Linux (testado no Ubuntu 22.04)
- Microfone
- Conta gratuita no [Picovoice Console](https://console.picovoice.ai/) para obter uma **Access Key**

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
Testar microfone com log:

```bash
python3 teste_com_log.py
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