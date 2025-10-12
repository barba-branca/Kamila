# 📁 Pasta LLM - Large Language Models

Esta pasta contém todos os módulos relacionados a modelos de linguagem (Large Language Models) e integração com IA generativa.

## 🗂️ **Estrutura da Pasta:**

```
.kamila/llm/
├── README.md                    # Este arquivo
├── gemini_engine.py            # Motor Google Gemini AI
├── ai_studio_integration.py    # Integração com AI Studio
├── test_llm_modules.py         # Testes dos módulos LLM
├── requirements_gemini.txt      # Dependências do Gemini
└── main_with_llm.py           # Main com integração LLM
```

## 🤖 **Módulos Disponíveis:**

### **1. Gemini Engine (`gemini_engine.py`)**
- **Função:** Integração com Google Gemini Pro
- **Recursos:**
  - Geração de texto avançada
  - Chat completion
  - Histórico de conversação
  - Modo simulado (sem API)
  - Análise de contexto

### **2. AI Studio Integration (`ai_studio_integration.py`)**
- **Função:** Integração com Google AI Studio
- **Recursos:**
  - Múltiplos modelos generativos
  - Análise de sentimento
  - Geração de texto personalizada
  - Suporte a diferentes temperaturas
  - Modo simulado

## 🚀 **Como Usar:**

### **Instalação:**
```bash
# Instalar dependências
pip install -r .kamila/llm/requirements_gemini.txt
```

### **Execução Básica:**
```bash
# Executar assistente com LLM
python .kamila/llm/main_with_llm.py

# Testar módulos LLM
python .kamila/llm/test_llm_modules.py
```

### **Importação nos Outros Módulos:**
```python
# Importar módulos LLM
from llm.gemini_engine import GeminiEngine
from llm.ai_studio_integration import AIStudioIntegration

# Inicializar engines
gemini = GeminiEngine()
ai_studio = AIStudioIntegration()

# Usar funcionalidades
response = gemini.chat("Olá! Como você está?")
sentiment = ai_studio.analyze_sentiment("Estou feliz!")
```

## ⚙️ **Configuração:**

### **Variáveis de Ambiente (.kamila/.env):**
```env
# API Keys para LLM
GOOGLE_AI_API_KEY=sua_chave_google_ai_aqui

# Configurações LLM
LLM_MODEL=gemini-pro
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
```

### **Modo Simulado:**
Se não houver API key configurada, os módulos funcionarão em modo simulado com respostas pré-programadas.

## 🧪 **Testes:**

### **Executar Todos os Testes:**
```bash
python .kamila/llm/test_llm_modules.py
```

### **Testes Individuais:**
```python
from llm.gemini_engine import GeminiEngine
from llm.ai_studio_integration import AIStudioIntegration

# Testar Gemini
gemini = GeminiEngine()
print(gemini.chat("Olá!"))

# Testar AI Studio
ai_studio = AIStudioIntegration()
print(ai_studio.generate_text("Conte uma piada"))
```

## 📊 **Funcionalidades Avançadas:**

### **Análise de Sentimento:**
```python
from llm.ai_studio_integration import AIStudioIntegration

ai_studio = AIStudioIntegration()
result = ai_studio.analyze_sentiment("Estou muito feliz hoje!")
print(result)
# Output: {'sentimento': 'positivo', 'confianca': 0.8, 'emocoes': ['feliz', 'contente']}
```

### **Chat com Contexto:**
```python
from llm.gemini_engine import GeminiEngine

gemini = GeminiEngine()
context = {
    'user_name': 'João',
    'mood': 'alegre',
    'conversation_history': [...]
}
response = gemini.chat("Como você está?", context)
```

## 🔧 **Troubleshooting:**

### **Problema: ImportError**
```bash
# Solução: Verificar se está na pasta correta
cd /caminho/para/projeto/kamila
python .kamila/llm/test_llm_modules.py
```

### **Problema: API Key não configurada**
- Os módulos funcionarão em modo simulado
- Configure `GOOGLE_AI_API_KEY` no arquivo `.kamila/.env`
- Obtenha chave em: https://aistudio.google.com/

### **Problema: Módulos não encontrados**
```bash
# Solução: Instalar dependências
pip install -r .kamila/llm/requirements_gemini.txt
```

## 📈 **Performance:**

- **Modo Simulado:** Respostas instantâneas
- **Modo API:** Latência de 1-3 segundos
- **Memória:** ~50MB por instância
- **CPU:** Uso mínimo em modo simulado

## 🔄 **Atualizações:**

Para atualizar os módulos LLM:
```bash
pip install --upgrade google-generativeai
```

## 📝 **Logs:**

Os módulos geram logs detalhados em:
- `logs/kamila.log` (logs principais)
- Console (logs em tempo real)

## 🎯 **Próximos Passos:**

1. **Integração com outros LLMs:**
   - OpenAI GPT
   - Anthropic Claude
   - Modelos locais (Llama, etc.)

2. **Funcionalidades Avançadas:**
   - Geração de imagens
   - Análise de áudio
   - Tradução em tempo real

3. **Otimização:**
   - Cache de respostas
   - Compressão de contexto
   - Processamento em lote

---

**📞 Suporte:** Para problemas ou dúvidas, consulte os logs ou abra uma issue no repositório.

**🤝 Contribuição:** Novos módulos LLM são bem-vindos! Siga o padrão dos módulos existentes.
