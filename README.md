# Conta tu o Conto

Protótipo de narrativa interativa: cria uma personagem, escolhe um cenário e continua a história escolhendo uma de três alternativas geradas por IA.

Esta recuperação utiliza **GPT-2 pré-treinado**, sem o modelo LoRA nem os dados do treino original, que já não estão disponíveis. Não equivale à qualidade ou ao comportamento da versão treinada. GPT-2 pode produzir texto incoerente ou inadequado; revê sempre os resultados. Não há filtros de conteúdo nem adequação infantil garantida.

## Estado do treino e do modelo

### Trabalho original

O projeto original incluiu trabalho de treino de GPT-2 com **LoRA/PEFT**, com o objetivo de o adaptar à geração de contos. Nuno Fernandes desenvolveu a interface Streamlit completa e foi responsável pelo treino e pela implementação do código LoRA, num projeto colaborativo.

O código e os notebooks foram preservados em `legacy/`, incluindo a configuração LoRA com `r=8`, `lora_alpha=32` e `lora_dropout=0.1`. Contudo, os **artefactos do modelo treinado e os dados utilizados já não estão disponíveis**. O código preservado não substitui esses ficheiros e requer revisão antes de um novo treino.

### Versão recuperada

A aplicação atual carrega **`openai-community/gpt2` pré-treinado**, sem os pesos ou adaptadores do treino original. Não foi realizado um novo treino durante esta recuperação. O download dos modelos no primeiro uso serve apenas para os carregar e gerar texto; **não treina o modelo**, nem as escolhas do utilizador atualizam os seus pesos.

No modo português, um modelo traduz o contexto para inglês, GPT-2 gera três continuações e outro modelo traduz essas continuações para português. Esses tradutores também são modelos pré-treinados, utilizados sem novo treino nesta versão.

### O que esperar dos resultados

Esta versão permite demonstrar a interface, a escolha de continuações e a integração dos modelos. Como GPT-2 não recebeu aqui a adaptação original a contos, pode produzir excertos em estilo de blogue, referências soltas, repetições ou mudanças de tema e de personagens. A tradução pode introduzir outras diferenças. A história conserva o texto completo para exportação, mas o modelo recebe apenas contexto recente e pode esquecer acontecimentos anteriores.

Não estão disponíveis métricas nem uma comparação reproduzível entre o modelo original e o atual. Por isso, não se afirma uma melhoria ou degradação medida, nem equivalência à versão treinada.

### Para voltar a treinar

Será necessário selecionar um novo conjunto de dados com origem e condições de utilização documentadas, rever o código de treino e definir uma avaliação. Um novo treino deve guardar o modelo base e a sua revisão, tokenizer, adaptadores LoRA, configuração, versões das dependências e resultados de avaliação, juntamente com instruções para os carregar na aplicação. Até isso acontecer, o projeto deve ser descrito como **protótipo recuperado com GPT-2 pré-treinado e código histórico de treino LoRA preservado**.

## Começar em Windows

1. Extrai o ZIP para uma pasta normal, fora do próprio ZIP.
2. Instala **Python 3.11 de 64 bits** a partir de [python.org](https://www.python.org/downloads/), se necessário.
3. Abre `install_windows.bat`. A instalação cria um ambiente local e instala PyTorch para CPU e as dependências.
4. Abre `start_windows.bat`. Mantém a janela aberta enquanto usas a aplicação.
5. O navegador deverá abrir em [localhost:8501](http://localhost:8501). Se não abrir, visita esse endereço.

O primeiro pedido de geração descarrega os modelos públicos do Hugging Face. Precisas de Internet, espaço para vários GB de cache e memória livre. A velocidade depende do computador; o modo português carrega mais modelos e consome mais recursos. Não há necessidade de API paga ou chave de API para os modelos públicos predefinidos.

Para o primeiro teste, escolhe **English** e escreve a ocupação em inglês: só carrega GPT-2. Depois testa **Português**, que traduz o contexto para inglês e as continuações para português.

## Instalação manual

Python suportado por este pacote: 3.10 a 3.12; 3.11 recomendado. Na pasta do projeto:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "torch>=2.6,<3" --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Em macOS/Linux, usa `python3.11 -m venv .venv` e `.venv/bin/python` nos comandos seguintes. Instala PyTorch de acordo com a [documentação oficial](https://pytorch.org/get-started/locally/) se o índice CPU não tiver uma distribuição para o teu sistema.

## O que foi corrigido

- O modelo passa a ser público e pré-treinado; a aplicação não depende de `model/` ou `raw_data/`.
- Os modelos só são carregados ao gerar o conto e ficam em cache durante o processo.
- O contexto traduz-se uma vez por ronda; as três alternativas são traduzidas em conjunto.
- As escolhas mantêm-se durante atualizações da página. Selecionar uma acrescenta exatamente a opção apresentada e inicia outra ronda.
- Todo o formulário é validado; as chaves dos botões são estáveis.
- Imagens e configuração são localizadas relativamente ao projeto, não ao diretório de trabalho.
- Os fundos originais foram preservados. Texto do utilizador/modelo não é inserido em HTML.
- O conto completo pode ser guardado em `.txt`. A geração usa o contexto recente, com limite de tokens; não mantém memória ilimitada da história.
- Pré-visualizações extrativas substituem o modelo de resumo BART para reduzir downloads e consumo de memória. Isto é uma alteração deliberada de comportamento.
- API separada, com validação, falhas explícitas e endpoint de saúde sem descarregar modelos.
- Dependências mínimas sem a lista de pacotes CUDA/Linux exportada no projeto original.

## Modelos e configuração

Não é preciso criar `.env`: existem valores predefinidos. Para alterar, copia `.env.example` para `.env` e reinicia o processo. O `.env` antigo não deve ser reutilizado automaticamente.

| Uso | Modelo predefinido |
|---|---|
| Geração em inglês | `openai-community/gpt2` |
| Português para inglês | `Helsinki-NLP/opus-mt-ROMANCE-en` |
| Inglês para português | `Helsinki-NLP/opus-mt-tc-big-en-pt`, prefixo `>>por<<` |

`DEVICE=cpu` é o valor predefinido. Só muda para `cuda` se tiveres PyTorch e GPU compatíveis. `LOCAL_FILES_ONLY=1` impede downloads e exige todos os modelos/tokenizers na cache. Não ativares essa opção antes do primeiro teste online.

As versões são intervalos de compatibilidade, **não um ambiente bloqueado e validado de ponta a ponta**. Depois de uma execução bem-sucedida, regista as versões com `python -m pip freeze` no teu ambiente.

## Testar

Testes de lógica e de integração com modelos simulados:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Sem dependências externas, os testes de lógica continuam a correr e os testes HTTP/Streamlit são assinalados como ignorados. Esses testes não comprovam a qualidade nem a disponibilidade dos modelos reais.

Teste de geração **real**, com downloads no primeiro uso:

```powershell
.\.venv\Scripts\python.exe -m project.smoke --language en
.\.venv\Scripts\python.exe -m project.smoke --language pt --context "Era uma vez uma viajante que encontrou um castelo misterioso."
```

Na interface, verifica: submissão de campos vazios, geração de três alternativas, seleção de uma delas, nova ronda, guardar conto e novo conto. Consulta `VALIDACAO.md` para saber o que foi efetivamente executado nesta entrega.

## API opcional

A interface chama o motor diretamente: não precisa de um segundo servidor API para funcionar.

```powershell
.\.venv\Scripts\python.exe -m uvicorn project.api:app --host 127.0.0.1 --port 8000
```

- `GET /health`: estado do processo e modelos carregados. Um resultado saudável não prova inferência.
- `POST /generate`: JSON `{"context":"Once upon a time...","language":"en"}`. Devolve `continuations` e `labels`.
- `GET /generate_outputs?context=...&language=en`: formato legado `[continuações, rótulos]`. Prefere POST para novos clientes.
- [Documentação local](http://127.0.0.1:8000/docs).

Usa a API localmente. Não está preparada com autenticação, quotas ou controlo de abuso para exposição pública.

## Docker opcional

```text
docker build -t conta-tu-o-conto .
docker run --rm -p 8501:8501 -v conta-model-cache:/root/.cache/huggingface conta-tu-o-conto
```

O Dockerfile inicia a interface. O volume conserva os downloads. Esta construção não foi executada no ambiente de recuperação.

## Preservação do trabalho original

O código de interface, treino com LoRA e notebooks recebidos no ZIP foram preservados em `legacy/`. São referência histórica: não são importados nem executados pela nova aplicação. Têm os requisitos e problemas antigos e não são um comando de treino pronto a usar. Os pesos treinados e os dados não foram recuperados nem substituídos por resultados inventados.

## Referências e atribuição dos modelos

- [GPT-2: modelo](https://huggingface.co/openai-community/gpt2) e [documentação](https://huggingface.co/docs/transformers/v4.51.3/en/model_doc/gpt2).
- [OPUS-MT ROMANCE → inglês](https://huggingface.co/Helsinki-NLP/opus-mt-ROMANCE-en).
- [OPUS-MT inglês → português](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt), disponibilizado pelo grupo Helsinki-NLP / projeto OPUS-MT, sob CC BY 4.0 conforme a ficha do modelo. O modelo é utilizado sem alteração nesta configuração; o texto de entrada recebe o prefixo de português indicado pelos autores. Consulta a ficha para publicações, autoria e licença.
- [Repositório original de Nuno Fernandes e colaboradores](https://github.com/mmf3358/Conta_tu_o_Conto). Esta recuperação não altera a autoria original nem publica alterações no GitHub.
