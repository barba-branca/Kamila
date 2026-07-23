# Documentação Técnica: Controle de Computador (`.kamila/core/computer_control.py`)

Esta documentação detalha o funcionamento do módulo **`computer_control.py`**, representado pela classe `ComputerControl`. Este componente é a interface de automação de Interface Gráfica do Usuário (GUI) da assistente **Kamila**, atuando como seus "braços e pernas" virtuais para controlar o Sistema Operacional por meio de visão computacional e linguagem natural.

---

## 1. Visão Geral da Arquitetura

O módulo utiliza a tecnologia de ponta **Agent S3** (`gui_agents.s3`) aliada à biblioteca `pyautogui`. Ele permite que a Kamila receba comandos em português (ex: *"abrir o bloco de notas"*, *"clicar no botão salvar"*) e converta essas instruções em ações de mouse e teclado em tempo real com base no que está visível na tela.

```mermaid
flowchart TD
    USER[Instrução em Linguagem Natural] -->|execute_instruction| CC[ComputerControl]
    
    subgraph Captura de Tela
        CC --> PAG[pyautogui.screenshot]
        PAG --> MEM[io.BytesIO / PNG Bytes]
    end

    subgraph Raciocínio & Grounding (Agent S3)
        MEM --> OBS[Observação: Screenshot + Instrução]
        OBS --> GROUND[OSWorldACI - Mecanismo de Ancoragem Visual]
        GROUND --> AGENT[AgentS3 - Predição de Ação]
    end

    subgraph Execução no SO
        AGENT --> CODE[Código Python de Ação (ex: pyautogui.click)]
        CODE --> EXEC[exec - Execução Direta no SO]
    end
```

---

## 2. Bibliotecas e Dependências

| Biblioteca | Papel no Módulo |
| :--- | :--- |
| **`gui_agents.s3.agents.agent_s.AgentS3`** | Agente principal responsável por planejar e prever a sequência de ações na GUI. |
| **`gui_agents.s3.agents.grounding.OSWorldACI`** | Motor de ancoragem visual que traduz elementos gráficos do screenshot para coordenadas $(X, Y)$. |
| **`pyautogui`** | Captura a dimensão da tela (`pyautogui.size()`), tira screenshots e executa os comandos físicos de mouse/teclado. |
| **`PIL.Image` & `io.BytesIO`** | Converte a imagem capturada da tela em um buffer de bytes PNG para transmissão sem necessidade de salvar arquivo em disco. |

---

## 3. Detalhamento da Classe `ComputerControl`

### 3.1 Inicialização (`__init__`)

```python
def __init__(self, platform="windows"):
```

- **Captura de Resolução**: Obtém a largura (`width`) e altura (`height`) nativas do monitor principal usando `pyautogui.size()`.
- **Configuração de Provedor LLM**:
  - `LLM_PROVIDER`: Provedor do modelo multimodal (Lido de `.env`, padrão: `"openai"`).
  - `LLM_MODEL`: Modelo de visão para interpretação da interface (Lido de `.env`, padrão: `"gpt-4o"`).
  - `OPENAI_API_KEY`: Chave de acesso à API do provedor visual.
- **Mecânica de Grounding e Agente**:
  - Instancia o `OSWorldACI` configurando a resolução de ancoragem.
  - Inicializa o `AgentS3` combinando o modelo de geração com o agente de grounding.
  - **Tratamento de Exceções**: Se a chave de API estiver ausente ou as bibliotecas de Agente S3 não estiverem instaladas, o sistema captura a exceção e marca `self.agent = None`, permitindo que o restante da assistente Kamila continue funcionando normalmente sem quebras.

---

### 3.2 Execução de Instruções (`execute_instruction`)

```python
def execute_instruction(self, instruction: str) -> str:
```

Este é o método público chamado pelo `ActionManager` (através da intenção `execute_on_pc`).

#### Fluxo Passo a Passo:
1. **Validação de Prontidão**: Verifica se `self.agent` foi inicializado corretamente.
2. **Captura Visual em Tempo Real**:
   - Tira um screenshot do estado atual da área de trabalho: `pyautogui.screenshot()`.
   - Converte e compacta a imagem em formato PNG em memória usando `io.BytesIO()`.
3. **Montagem da Observação**:
   - Cria o dicionário `obs = {"screenshot": screenshot_bytes}`.
4. **Predição Multimodal via Agent S3**:
   - Chama `self.agent.predict(instruction=instruction, observation=obs)`.
   - O agente analisa a imagem e a instrução recebida, retornando a tupla `(info, action)`.
5. **Execução Nativa**:
   - O objeto `action[0]` contém uma instrução em código Python (ex: `pyautogui.click(x=450, y=300)` ou `pyautogui.write('Bloco de Notas')`).
   - O módulo executa a ação diretamente no sistema através do interpretador dinâmico `exec(action[0])`.
6. **Retorno de Status**: Retorna uma mensagem de confirmação para ser lida/falada pela Kamila para o usuário.

---

## 4. Variáveis de Ambiente Relevantes (`.env`)

| Variável | Valor Padrão | Descrição |
| :--- | :--- | :--- |
| `LLM_PROVIDER` | `openai` | Provedor da LLM de visão (OpenAI, Anthropic, etc.). |
| `LLM_MODEL` | `gpt-4o` | Modelo multimodal responsável por "olhar" para a tela do PC. |
| `OPENAI_API_KEY` | - | Chave de API necessária para rodar o Agent S3. |

---

## 5. Exemplo de Uso Interno

```python
from core.computer_control import ComputerControl

# Inicialização
cc = ComputerControl(platform="windows")

# Execução de comando visual
resultado = cc.execute_instruction("Abrir o bloco de notas e digitar Olá Kamila")
print(resultado)
```
