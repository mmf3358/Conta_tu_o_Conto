# Conta Tu o Conto

**Final project — Le Wagon Data Science Bootcamp (2025)**

Interactive Portuguese-language storytelling application using a Python backend, a Streamlit interface, and Hugging Face language-model pipelines. The user chooses a title, character and setting, then selects one of three AI-generated continuations to evolve the story.

## Stack
Python, Streamlit, FastAPI, Hugging Face Transformers, GPT-2, PyTorch, PEFT/LoRA, BART summarization, translation pipelines.

## Architecture
- `project/streamlit_app/`: story setup and interactive interface.
- `project/app/conta_app.py`: reusable generation service and FastAPI endpoints.
- `project/model_utils.py`: lazy-loaded inference pipelines and LoRA training utilities.
- `project/model_train.py`: optional training entry point.

## Setup
Install dependencies from `requirements.txt` in a virtual environment. Model downloads may be large and require network access. Configure the variables in `.env` or your shell:

- `MODEL_PATH`: local trained model path or compatible Hugging Face causal LM model identifier.
- `TRANSLATOR_PT_EN`: Portuguese-to-English translation model identifier.
- `TRANSLATOR_EN_PT`: English-to-Portuguese translation model identifier.
- `TRAIN_FILE_PATH`: optional training text path.
- `MODEL_NAME`: optional base model identifier for training.

Run from the repository root:

```bash
streamlit run project/streamlit_app/app.py
```

Optional API:

```bash
uvicorn project.app.conta_app:app --reload
```

API endpoint: `GET /generate_outputs?context=...`. Health check: `GET /health`.

## Status
This branch contains static-code fixes. End-to-end inference and model training still require verification with the configured model weights and dependencies. No deployment or production readiness is claimed.

## Security
Do not commit real credentials to `.env`. If credentials were ever published, rotate them.
