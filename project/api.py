from typing import Literal
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from project.engine import ModelUnavailable, get_engine
from project.story import choice_label

app = FastAPI(title='Conta tu o Conto', version='0.1.0')


class GenerateRequest(BaseModel):
    context: str = Field(min_length=1, max_length=20000)
    language: Literal['pt', 'en'] = 'pt'


class GenerateResponse(BaseModel):
    continuations: list[str]
    labels: list[str]


def _outputs(context, language):
    if not context.strip():
        raise HTTPException(status_code=422, detail='O contexto não pode estar vazio.')
    try:
        texts = get_engine().generate(context, language)
    except ModelUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return texts, [choice_label(t) for t in texts]


@app.get('/health')
def health():
    return {'status': 'ok', **get_engine().status()}


@app.post('/generate', response_model=GenerateResponse)
def generate(request: GenerateRequest):
    texts, labels = _outputs(request.context, request.language)
    return GenerateResponse(continuations=texts, labels=labels)


@app.get('/generate_outputs', deprecated=True)
def generate_outputs(context: str = Query(min_length=1, max_length=20000), language: Literal['pt', 'en'] = 'pt'):
    """Compatibility with the original HTTP response: [continuations, labels]."""
    return _outputs(context, language)
