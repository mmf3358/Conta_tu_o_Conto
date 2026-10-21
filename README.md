# Conta tu o Conto

A idéia por trás detas aplicação é a da criação de um gerador de contos infinitos. O Usuário escolhe um personagem, um tema e o conto começa a desenrolar-se de três em três opções de continuação. 

A aplicação combina uma interface **Streamlit**, geração de texto com **GPT-2** e tradução entre português e inglês. O conto cresce com as escolhas do utilizador e pode ser guardado num ficheiro de texto.

## Funcionalidades

- Configuração do título, nome, idade e ocupação da personagem.
- Três cenários: castelo, floresta e reino de fadas.
- Geração de três alternativas por ronda, com seleção pelo utilizador.
- Continuação da narrativa a partir das escolhas anteriores.
- Modos português e inglês.
- Exportação do conto completo em `.txt`.
- Interface ilustrada, com cartões de texto e deslocamento interno.
- API FastAPI opcional para integrar a geração noutras aplicações.

## Modelo e treino

O projeto inclui código de treino de GPT-2 com **LoRA/PEFT**. **Os dados de treino e os artefactos do modelo treinado não estão disponíveis neste repositório.**

A aplicação funciona com **GPT-2 pré-treinado**, mantendo a sua essência: gerar alternativas, permitir que o utilizador escolha uma e continuar o conto. A demonstração não necessita dos ficheiros de treino. O código experimental e os notebooks estão em `legacy/`; não são executados pela aplicação.

No modo português, o contexto é traduzido para inglês antes da geração e as continuações são traduzidas para português. No modo inglês, apenas GPT-2 é necessário. O download inicial dos modelos não realiza treino e as escolhas do utilizador não alteram os seus pesos.

GPT-2 é um modelo de uso geral: pode produzir repetições, referências soltas ou mudanças de tema e de personagens. A aplicação permite continuar o conto por várias rondas, mas utiliza apenas contexto recente para gerar texto, sem memória ilimitada da narrativa. 

## Tecnologias

Python · Streamlit · FastAPI · PyTorch · Hugging Face Transformers · GPT-2 · LoRA/PEFT

| Componente | Modelo utilizado na aplicação |
|---|---|
| Geração em inglês | `openai-community/gpt2` |
| Tradução de português para inglês | `Helsinki-NLP/opus-mt-ROMANCE-en` |
| Tradução de inglês para português | `Helsinki-NLP/opus-mt-tc-big-en-pt`, com prefixo `>>por<<` |

As pré-visualizações da API são extraídas do início de cada continuação, sem um modelo adicional de resumo.

## Começar em Windows

1. Descarregar o repositório e extrair o ZIP para uma pasta normal.
2. Confirmar que tem **Python 3.10, 3.11 ou 3.12 de 64 bits**. Recomenda-se Python 3.11, disponível em [python.org](https://www.python.org/downloads/).
3. Abrir `install_windows.bat`. O instalador cria um ambiente local e instala as dependências, incluindo PyTorch para CPU.
4. Abrir `start_windows.bat` e manter a janela aberta durante a utilização.
5. Aceder a [localhost:8501](http://localhost:8501), caso o navegador não abra automaticamente.

Se utilizar o Python Install Manager e faltar uma versão compatível, executar `py install 3.11` antes de iniciar a instalação.

O primeiro pedido de geração descarrega os modelos públicos do Hugging Face. É necessário acesso à Internet, espaço em disco para a cache e memória disponível. Não é necessária uma chave de API ou um serviço de inferência pago para os modelos predefinidos.

Para experimentar com menos recursos, escolher **English** e preencher os dados da personagem em inglês. O modo português necessita também dos dois modelos de tradução.

## Instalação manual

Na pasta do projeto, com Python 3.11 instalado:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "torch>=2.6,<3" --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Em macOS/Linux, criar o ambiente com `python3.11 -m venv .venv` e utiliza `.venv/bin/python` nos comandos seguintes. Consultar a [instalação oficial de PyTorch](https://pytorch.org/get-started/locally/) para escolher a distribuição adequada ao sistema em questão.

## Configuração

Os valores predefinidos permitem iniciar a aplicação sem criar um ficheiro `.env`. Para personalizar, copiar `.env.example` para `.env`, alterar os valores e reiniciar o processo.

| Variável | Utilização |
|---|---|
| `MODEL_NAME` | Identificador do modelo de geração |
| `TRANSLATOR_PT_EN` | Modelo de tradução para inglês |
| `TRANSLATOR_EN_PT` | Modelo de tradução para português |
| `PORTUGUESE_PREFIX` | Prefixo de língua do tradutor para português |
| `DEVICE` | `cpu` por defeito; `cuda` requer hardware e instalação compatíveis |
| `MAX_NEW_TOKENS` | Limite de tokens gerados por continuação |
| `TEMPERATURE` | Controlo da aleatoriedade da geração |
| `CONTEXT_TOKENS` | Limite de contexto recente enviado ao gerador |
| `LOCAL_FILES_ONLY` | `1` utiliza apenas modelos já descarregados |

Os modelos são carregados no primeiro pedido e reutilizados durante o processo. A história completa permanece disponível para exportação, mesmo quando o contexto enviado ao modelo é limitado.

## Testes

Instala as dependências de teste e executa a suite:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes cobrem a lógica da narrativa, persistência das escolhas, validação, configuração, API e interface. Os testes de API e interface são ignorados quando as respetivas dependências não estão instaladas. Os testes com modelos simulados não avaliam a qualidade da geração real.

Para testar a inferência com os modelos:

```powershell
.\.venv\Scripts\python.exe -m project.smoke --language en
.\.venv\Scripts\python.exe -m project.smoke --language pt --context "Era uma vez uma viajante que encontrou um castelo misterioso."
```

A aplicação foi utilizada localmente com geração em português e continuação por várias rondas. A qualidade narrativa não foi avaliada através de métricas formais.

## API opcional

A interface chama o motor diretamente e não necessita de um servidor API separado. Para utilizar a API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn project.api:app --host 127.0.0.1 --port 8000
```

- `GET /health`: estado do processo e indicação dos modelos carregados.
- `POST /generate`: recebe `{"context":"Once upon a time...","language":"en"}` e devolve `continuations` e `labels`.
- `GET /generate_outputs`: endpoint de compatibilidade que devolve `[continuações, rótulos]`.
- [Documentação interativa local](http://127.0.0.1:8000/docs).

A API destina-se a utilização local. Uma publicação aberta requer autenticação, limites de utilização e controlo de acesso.

## Docker

```text
docker build -t conta-tu-o-conto .
docker run --rm -p 8501:8501 -v conta-model-cache:/root/.cache/huggingface conta-tu-o-conto
```

O contentor inicia a interface Streamlit. O volume mantém a cache dos modelos entre execuções. A construção Docker não foi validada neste ambiente.

## Contribuições

Projeto colaborativo. **Nuno Fernandes** desenvolveu a interface Streamlit completa e foi responsável pelo trabalho de treino e pela implementação do código LoRA.

## Referências

- [GPT-2](https://huggingface.co/openai-community/gpt2) e [documentação de Transformers](https://huggingface.co/docs/transformers/v4.51.3/en/model_doc/gpt2).
- [OPUS-MT ROMANCE → inglês](https://huggingface.co/Helsinki-NLP/opus-mt-ROMANCE-en).
- [OPUS-MT inglês → português](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt), do grupo Helsinki-NLP / projeto OPUS-MT, sob CC BY 4.0 conforme a ficha do modelo. É utilizado sem alteração, com o prefixo de português indicado pelos autores. Consulta a ficha para autoria, publicações e licença.
