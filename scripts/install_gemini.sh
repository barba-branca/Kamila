#!/bin/bash
# Script de instalação dos módulos Gemini AI para Kamila
# Uso: chmod +x install_gemini.sh && ./install_gemini.sh

echo "🤖 Instalando Módulos Gemini AI para Kamila..."
echo "================================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3 primeiro."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale pip3 primeiro."
    exit 1
fi

echo "✅ Python e pip verificados"

# Instalar dependências básicas
echo "📦 Instalando dependências básicas..."
pip3 install -r config/requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências básicas"
    exit 1
fi

echo "✅ Dependências básicas instaladas"

# Instalar dependências do Gemini
echo "🧠 Instalando dependências do Gemini AI..."
pip3 install -r .kamila/requirements_gemini.txt

if [ $? -ne 0 ]; then
    echo "⚠️  Erro ao instalar dependências do Gemini (algumas podem não ser críticas)"
    echo "🔄 Continuando com dependências básicas..."
fi

echo "✅ Dependências do Gemini instaladas"

# Verificar instalação
echo "🔍 Verificando instalação dos módulos..."

python3 -c "
try:
    import speech_recognition
    print('✅ speech_recognition: OK')
except ImportError:
    print('❌ speech_recognition: FALHOU')
"

python3 -c "
try:
    import pyttsx3
    print('✅ pyttsx3: OK')
except ImportError:
    print('❌ pyttsx3: FALHOU')
"

python3 -c "
try:
    import google.generativeai
    print('✅ google-generativeai: OK')
except ImportError:
    print('⚠️  google-generativeai: NÃO INSTALADO (modo simulado disponível)')
"

echo "================================================="
echo "🎉 Instalação dos Módulos Gemini Concluída!"
echo "================================================="
echo ""
echo "📋 Próximos passos:"
echo "1. Configure suas API Keys em .kamila/.env"
echo "2. Execute: python .kamila/test_gemini_modules.py"
echo "3. Execute: python .kamila/main_with_gemini.py"
echo ""
echo "🔗 Para obter API Keys:"
echo "• Google AI Studio: https://aistudio.google.com/"
echo "• Picovoice Console: https://console.picovoice.ai/"
echo ""
echo "💡 Dica: Se não tiver API Keys, os módulos funcionarão em modo simulado!"
