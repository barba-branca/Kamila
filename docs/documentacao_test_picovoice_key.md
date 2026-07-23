# Documentação Técnica: Validador de Credenciais Picovoice (`testes/test_picovoice_key.py`)

Esta documentação descreve as especificações do script de validação de credenciais **`test_picovoice_key.py`**, localizado em `testes/test_picovoice_key.py`. Este módulo é um **utilitário de teste de bancada (*smoke test*) para autenticação**, projetado para verificar a autenticidade e a cota ativa da `PICOVOICE_API_KEY` no arquivo `.kamila/.env`.

---

## 1. Visão Geral da Arquitetura do Teste

O `test_picovoice_key.py` executa o carregamento das variáveis de ambiente com `dotenv` e realiza uma tentativa real de instanciação da biblioteca `pvporcupine` contra os modelos binários da assistente **Kamila**.

```mermaid
flowchart TD
    START[Início: python testes/test_picovoice_key.py] --> LOAD_ENV[Carrega .kamila/.env]
    LOAD_ENV --> CHECK_KEY{PICOVOICE_API_KEY é válida?}
    
    CHECK_KEY -->|Ausente ou Padrão| FAIL[Exibe aviso: PRECISA CONFIGURAÇÃO - Retorna False]
    
    CHECK_KEY -->|Chave Encontrada| TRY_INIT[pvporcupine.create com camila.ppn e params.pv]
    TRY_INIT -->|Sucesso de Conexão| OK[Exibe: Porcupine inicializado - Chama delete() e Retorna True]
    TRY_INIT -->|Chave Invalida / Expirada| ERR[Exibe erro de autenticação e Retorna False]
```

---

## 2. Detalhes das Funções do Script

### 2.1 `test_picovoice_key() -> bool`
1. Requisita `os.getenv('PICOVOICE_API_KEY')`.
2. Garante que a chave não possui o placeholder padrão (`"your_picovoice_api_key_here"`).
3. Tenta instanciar o motor Picovoice:
   ```python
   porcupine = create_porcupine(
       access_key=api_key,
       keyword_paths=["models/wake_words/camila_pt_windows_v3_0_0.ppn"],
       model_path="models/porcupine_models/porcupine_params_pt.pv"
   )
   porcupine.delete()
   ```
4. Libera a memória imediatamente com `porcupine.delete()`.

---

### 2.2 `test_google_key() -> bool`
Valida a presença opcional da `GOOGLE_API_KEY` para recursos adicionais de fala e busca.

---

## 3. Como Executar

No terminal:

```bash
python testes/test_picovoice_key.py
```
