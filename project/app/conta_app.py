"""Story generation service. Model inference is lazy-loaded by model_utils."""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from project.model_utils import generate_text, summarizer, translator
from project.params import TRANSLATOR_EN_PT, TRANSLATOR_PT_EN

app = FastAPI(title="Conta Tu o Conto")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])


def generate_outputs(context: str):
    if not context or not context.strip():
        raise ValueError("O contexto não pode estar vazio.")
    if not TRANSLATOR_PT_EN or not TRANSLATOR_EN_PT:
        raise RuntimeError("Configure TRANSLATOR_PT_EN e TRANSLATOR_EN_PT no ambiente.")

    context_en = translator(context, TRANSLATOR_PT_EN, max_length=256, min_length=1)[0]["translation_text"]
    outputs, summaries = [], []
    for _ in range(3):
        generated = generate_text(context_en)[0]["generated_text"]
        continuation = generated[len(context_en):].strip() if generated.startswith(context_en) else generated.strip()
        if not continuation:
            continuation = generated.strip()
        output_pt = translator(continuation, TRANSLATOR_EN_PT, max_length=128, min_length=1)[0]["translation_text"].strip()
        outputs.append(output_pt)
        summaries.append(summarizer(output_pt, max_length=24, min_length=5)[0]["summary_text"])
    return outputs, summaries


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/generate_outputs")
def generate_outputs_endpoint(context: str = Query(min_length=1)):
    try:
        outputs, summaries = generate_outputs(context)
        return {"outputs": outputs, "summaries": summaries}
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
