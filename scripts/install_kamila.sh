#!/bin/bash

# Kamila Assistant - Installation Script
# Script de instalação automatizada para Linux

set -e

echo "🤖 Kamila Assistant - Instalação Automatizada"
echo "============================================="

# Verificar se está rodando como root (para algumas operações)
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  AVISO: Não execute este script como root!"
   exit 1
fi

# Verificar sistema operacional
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Este script é apenas para Linux!"
    exit 1
fi

echo "📋 Verificando dependências do sistema..."

# Atualizar lista de pacotes
sudo apt update

# Instalar dependências do sistema
echo "🔧 Instalando dependências do sistema..."
sudo apt install -y python3-pip python3-dev portaudio19-dev libasound2-dev

# Instalar Python dependencies
echo "🐍 Instalando dependências Python..."
pip3 install -r config/requirements.txt

# Criar arquivo .env se não existir
if [[ ! -f .kamila/.env ]]; then
    echo "📝 Criando arquivo de configuração..."
    cp .kamila/.env.example .kamila/.env
    echo "⚠️  IMPORTANTE: Edite o arquivo .kamila/.env com suas chaves de API!"
    echo "   - PICOVOICE_API_KEY (obtenha em: https://console.picovoice.ai/)"
    echo "   - GOOGLE_API_KEY (para reconhecimento de voz)"
    echo "   - GOOGLE_AI_API_KEY (para IA conversacional)"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p logs data audio/samples models/wake_words models/porcupine_models

# Configurar permissões
echo "🔐 Configurando permissões..."
chmod +x .kamila/main.py

# Instalar serviço systemd (opcional)
read -p "📦 Deseja instalar o serviço systemd para inicialização automática? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⚙️  Instalando serviço systemd..."

    # Criar arquivo de serviço
    sudo tee /etc/systemd/system/kamila.service > /dev/null << EOF
[Unit]
Description=Kamila Voice Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
ExecStart=$PWD/.kamila/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

    # Recarregar systemd e habilitar serviço
    sudo systemctl daemon-reload
    sudo systemctl enable kamila.service

    echo "✅ Serviço systemd instalado!"
    echo "   Para iniciar: sudo systemctl start kamila"
    echo "   Para verificar status: sudo systemctl status kamila"
fi

# Testar instalação
echo "🧪 Testando instalação..."
python3 -c "import pyttsx3, speech_recognition; print('✅ Dependências básicas OK!')"

echo ""
echo "🎉 Instalação concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo .kamila/.env com suas chaves de API"
echo "2. Execute: python3 .kamila/main.py"
echo "3. Diga 'kamila' para ativar a assistente"
echo ""
echo "💡 Comandos de teste:"
echo "   - 'kamila oi' (para saudar)"
echo "   - 'kamila que horas são' (para saber o horário)"
echo "   - 'kamila conta uma piada' (para ouvir uma piada)"
echo "   - 'kamila tchau' (para encerrar)"
echo ""
echo "📚 Para mais informações, consulte: docs/README.md"
echo ""
echo "🚀 Kamila está pronta para uso!"
