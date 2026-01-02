# 🧪 Pasta de Testes - Projeto Kamila

Esta pasta contém todos os arquivos de teste do projeto Kamila, organizados por categoria e funcionalidade.

## 📁 Estrutura dos Testes

### 🏠 Testes Principais (Raiz)
- **`teste_rapido.py`** - Teste rápido de verificação de arquivos
- **`test_kamila_completa.py`** - Teste completo da assistente
- **`test_kamila_simples.py`** - Teste simplificado dos módulos
- **`test_kamila_final.py`** - Teste final de integração
- **`test_kamila_corrigido.py`** - Versão corrigida dos testes

### 🧠 Testes de Módulos Core
- **`test_kamila.py`** - Testes dos módulos principais (core)

### 🤖 Testes de IA Generativa
- **`test_llm_modules.py`** - Testes dos módulos de IA generativa (LLM)

## 📚 Documentação Completa

Para documentação detalhada de cada teste, consulte:
- **`DOCUMENTACAO_COMPLETA_TESTES.md`** - Documentação completa e detalhada
- Este arquivo - Visão geral e instruções básicas

## 🚀 Como Executar os Testes

### Teste Rápido (Recomendado)
```bash
python testes/teste_rapido.py
```
Verifica se todos os arquivos essenciais estão presentes.

### Testes de Módulos
```bash
# Teste dos módulos principais
python testes/test_kamila.py

# Teste dos módulos de IA
python testes/test_llm_modules.py
```

### Testes Completos
```bash
# Teste completo da assistente
python testes/test_kamila_completa.py

# Teste simplificado
python testes/test_kamila_simples.py
```

## 📊 Cobertura dos Testes

### ✅ Funcionalidades Testadas

#### Módulos Core:
- [x] **STT Engine** - Reconhecimento de voz
- [x] **TTS Engine** - Síntese de voz
- [x] **Interpreter** - Interpretação de comandos
- [x] **Memory Manager** - Gerenciamento de memória
- [x] **Action Manager** - Sistema de ações

#### Módulos LLM:
- [x] **Gemini Engine** - Integração com Google Gemini
- [x] **AI Studio Integration** - Múltiplos modelos
- [x] **Modo Simulado** - Funcionamento sem API
- [x] **Análise de Sentimento** - Detecção de emoções

### 🔧 Dependências para Testes

```bash
# Instalar dependências básicas
pip install -r config/requirements.txt

# Instalar dependências de IA (opcional)
pip install -r .kamila/llm/requirements_gemini.txt
```

## 📋 Ordem Recomendada de Execução

1. **`teste_rapido.py`** - Verificar se tudo está no lugar
2. **`test_kamila.py`** - Testar módulos principais
3. **`test_llm_modules.py`** - Testar módulos de IA
4. **`test_kamila_simples.py`** - Teste de integração básico
5. **`test_kamila_completa.py`** - Teste completo

## 🐛 Troubleshooting

### Erro: "Módulo não encontrado"
```bash
# Verificar se está na pasta correta
cd /caminho/para/projeto/kamila

# Executar teste rápido primeiro
python testes/teste_rapido.py
```

### Erro: "API Key não configurada"
- Os testes funcionam em modo simulado
- Configure `.kamila/.env` para funcionalidades completas

### Erro: "Microfone não encontrado"
- Testes de áudio podem falhar sem microfone
- Use modo simulado para testes básicos

## 📈 Resultados Esperados

### Teste Rápido:
```
🚀 TESTE RÁPIDO DO PROJETO KAMILA
==================================================
✅ .kamila/main.py
✅ .kamila/main_with_llm.py
✅ .kamila/core/stt_engine.py
✅ .kamila/core/tts_engine.py
✅ .kamila/core/interpreter.py
✅ .kamila/core/memory_manager.py
✅ .kamila/core/actions.py
✅ .kamila/llm/gemini_engine.py
✅ .kamila/llm/ai_studio_integration.py
✅ .kamila/llm/test_llm_modules.py
✅ config/requirements.txt
✅ data/memory.json
✅ docs/README.md
==================================================
RESULTADO: 13/13 arquivos encontrados
🎉 PROJETO KAMILA 100% RECUPERADO!
```

## 🎯 Objetivos dos Testes

1. **Verificação de Integridade** - Garantir que todos os arquivos estão presentes
2. **Teste de Funcionalidades** - Validar que os módulos funcionam corretamente
3. **Teste de Integração** - Verificar se os módulos trabalham juntos
4. **Teste de Performance** - Avaliar velocidade e uso de recursos
5. **Teste de Compatibilidade** - Verificar funcionamento em diferentes ambientes

## 📝 Logs de Teste

Todos os testes geram logs detalhados em:
- `logs/kamila.log` - Logs principais
- `logs/current_run.log` - Logs da execução atual

## 🔄 Manutenção

Para adicionar novos testes:
1. Criar arquivo na pasta apropriada
2. Seguir padrão de nomenclatura: `test_nome_descriptivo.py`
3. Incluir docstring explicando o que o teste faz
4. Adicionar ao README.md

---

**🎉 Testes organizados e prontos para uso!**

**📖 Para documentação completa, consulte: `DOCUMENTACAO_COMPLETA_TESTES.md`**
