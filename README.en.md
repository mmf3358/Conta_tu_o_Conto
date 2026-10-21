# Conta tu o Conto

[Português](README.md) | English

The idea behind this application is to create an endless story generator. The user chooses a character and a theme. The story unfolds in rounds, each offering three possible continuations. Whenever the user decides the story is complete, they can save the result.

The application combines a **Streamlit** interface, text generation with **GPT-2**, and translation between Portuguese and English. The story grows through the user's choices and can be saved as a text file.

## Features

- Set the story title and the character's name, age, and occupation.
- Choose from three settings: a castle, a forest, and a fairy kingdom.
- Generate three alternatives per round for the user to choose from.
- Continue the narrative based on previous choices.
- Portuguese and English modes.
- Export the complete story as a `.txt` file.
- Illustrated interface with text cards and internal scrolling.
- Optional FastAPI API for integrating text generation into other applications.

## Model and training

The project includes code for training GPT-2 with **LoRA/PEFT**. **The training data and trained model artifacts are not available in this repository.**

The application runs with **pretrained GPT-2**, preserving its core functionality: generating alternatives, letting the user choose one, and continuing the story. The demonstration does not require the training files. Experimental code and notebooks are located in `legacy/` and are not executed by the application.

In Portuguese mode, the context is translated into English before generation, and the continuations are translated back into Portuguese. In English mode, only GPT-2 is required. Downloading the models does not train them, and the user's choices do not update their weights.

GPT-2 is a general-purpose model: it may produce repetition, unrelated references, or changes in theme and characters. The application supports continuing a story across multiple rounds, but uses only recent context for text generation, without unlimited narrative memory.

## Technologies

Python · Streamlit · FastAPI · PyTorch · Hugging Face Transformers · GPT-2 · LoRA/PEFT

| Component | Model used by the application |
|---|---|
| English text generation | `openai-community/gpt2` |
| Portuguese-to-English translation | `Helsinki-NLP/opus-mt-ROMANCE-en` |
| English-to-Portuguese translation | `Helsinki-NLP/opus-mt-tc-big-en-pt`, with the `>>por<<` prefix |

API previews are extracted from the beginning of each continuation, without an additional summarization model.

## Getting started on Windows

1. Download the repository and extract the ZIP into a regular folder.
2. Make sure **64-bit Python 3.10, 3.11, or 3.12** is installed. Python 3.11 is recommended and is available from [python.org](https://www.python.org/downloads/).
3. Open `install_windows.bat`. The installer creates a local environment and installs the dependencies, including PyTorch for CPU.
4. Open `start_windows.bat` and keep the window open while using the application.
5. Visit [localhost:8501](http://localhost:8501) if the browser does not open automatically.

If you use Python Install Manager and do not have a compatible version, run `py install 3.11` before starting the installation.

The first generation request downloads the public models from Hugging Face. Internet access, disk space for the cache, and available memory are required. No API key or paid inference service is needed for the default models.

For a less resource-intensive first test, select **English** and enter the character details in English. Portuguese mode also requires both translation models.

## Manual installation

From the project folder, with Python 3.11 installed:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "torch>=2.6,<3" --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS/Linux, create the environment with `python3.11 -m venv .venv` and use `.venv/bin/python` in the subsequent commands. See the [official PyTorch installation instructions](https://pytorch.org/get-started/locally/) to select the appropriate distribution for your system.

## Configuration

The default settings allow the application to start without a `.env` file. To customize them, copy `.env.example` to `.env`, change the values, and restart the process.

| Variable | Purpose |
|---|---|
| `MODEL_NAME` | Generation model identifier |
| `TRANSLATOR_PT_EN` | Translation model for English output |
| `TRANSLATOR_EN_PT` | Translation model for Portuguese output |
| `PORTUGUESE_PREFIX` | Target-language prefix for the Portuguese translator |
| `DEVICE` | `cpu` by default; `cuda` requires compatible hardware and software |
| `MAX_NEW_TOKENS` | Maximum number of generated tokens per continuation |
| `TEMPERATURE` | Controls generation randomness |
| `CONTEXT_TOKENS` | Maximum recent context sent to the generator |
| `LOCAL_FILES_ONLY` | Set to `1` to use only previously downloaded models |

Models are loaded on the first request and reused throughout the process. The complete story remains available for export, even when the context sent to the model is limited.

## Tests

Install the test dependencies and run the suite:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests cover narrative logic, choice persistence, validation, configuration, the API, and the interface. API and interface tests are skipped when their dependencies are not installed. Tests using simulated models do not evaluate the quality of actual text generation.

To test inference with the models:

```powershell
.\.venv\Scripts\python.exe -m project.smoke --language en
.\.venv\Scripts\python.exe -m project.smoke --language pt --context "Era uma vez uma viajante que encontrou um castelo misterioso."
```

The application has been used locally to generate Portuguese text and continue stories across multiple rounds. Narrative quality has not been evaluated using formal metrics.

## Optional API

The interface calls the generation engine directly and does not require a separate API server. To use the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn project.api:app --host 127.0.0.1 --port 8000
```

- `GET /health`: process status and an indication of which models are loaded.
- `POST /generate`: accepts `{"context":"Once upon a time...","language":"en"}` and returns `continuations` and `labels`.
- `GET /generate_outputs`: compatibility endpoint returning `[continuations, labels]`.
- [Local interactive documentation](http://127.0.0.1:8000/docs).

The API is intended for local use. Public deployment requires authentication, usage limits, and access control.

## Docker

```text
docker build -t conta-tu-o-conto .
docker run --rm -p 8501:8501 -v conta-model-cache:/root/.cache/huggingface conta-tu-o-conto
```

The container starts the Streamlit interface. The volume preserves the model cache between runs. The Docker build has not been validated in this environment.

## Contributions

A collaborative project. **Nuno Fernandes** developed the complete Streamlit interface and was responsible for the training work and implementation of the LoRA code.

## References

- [GPT-2](https://huggingface.co/openai-community/gpt2) and the [Transformers documentation](https://huggingface.co/docs/transformers/v4.51.3/en/model_doc/gpt2).
- [OPUS-MT ROMANCE → English](https://huggingface.co/Helsinki-NLP/opus-mt-ROMANCE-en).
- [OPUS-MT English → Portuguese](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt), from the Helsinki-NLP group / OPUS-MT project, licensed under CC BY 4.0 according to the model card. It is used without modification, with the Portuguese prefix specified by its authors. See the model card for authorship, publications, and licensing details.
