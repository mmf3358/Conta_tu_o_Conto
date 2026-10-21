"""Lazy pretrained inference. Importing the app never downloads models."""
from functools import lru_cache
from threading import RLock
import logging
from project.settings import Settings
from project.story import clean_text

logger = logging.getLogger(__name__)


class ModelUnavailable(RuntimeError):
    pass


class StoryEngine:
    def __init__(self, settings=None):
        self.settings = settings or Settings.from_env()
        self._generator = None
        self._translators = {}
        self._lock = RLock()

    def _libraries(self):
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
        except ImportError as exc:
            raise ModelUnavailable('Faltam dependências. Executa: python -m pip install -r requirements.txt') from exc
        return torch, AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

    def _load(self, model_id, causal):
        torch, tokenizer_cls, causal_cls, seq_cls = self._libraries()
        opts = {'local_files_only': self.settings.local_files_only, 'trust_remote_code': False}
        tokenizer = tokenizer_cls.from_pretrained(model_id, **opts)
        model = (causal_cls if causal else seq_cls).from_pretrained(model_id, **opts)
        model.to(self.settings.device)
        model.eval()
        return tokenizer, model

    def _translate(self, texts, direction):
        if direction not in self._translators:
            model_id = self.settings.translator_pt_en if direction == 'pt_en' else self.settings.translator_en_pt
            self._translators[direction] = self._load(model_id, causal=False)
        tokenizer, model = self._translators[direction]
        if direction == 'en_pt':
            texts = [self.settings.portuguese_prefix + t for t in texts]
        tokenizer.truncation_side = 'left'
        inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=384)
        inputs = {key: value.to(self.settings.device) for key, value in inputs.items()}
        torch = self._libraries()[0]
        with torch.inference_mode():
            outputs = model.generate(**inputs, max_new_tokens=160, num_beams=2)
        return [clean_text(t) for t in tokenizer.batch_decode(outputs, skip_special_tokens=True)]

    def _generate_english(self, context):
        if self._generator is None:
            self._generator = self._load(self.settings.model, causal=True)
        tokenizer, model = self._generator
        tokenizer.truncation_side = 'left'
        window = min(getattr(model.config, 'max_position_embeddings', 1024), 1024)
        budget = min(self.settings.context_tokens, window - self.settings.max_new_tokens)
        if budget < 1:
            raise ValueError('O modelo não tem contexto suficiente para esta configuração.')
        inputs = tokenizer(context, return_tensors='pt', truncation=True, max_length=budget)
        inputs = {key: value.to(self.settings.device) for key, value in inputs.items()}
        prompt_length = inputs['input_ids'].shape[-1]
        torch = self._libraries()[0]
        with torch.inference_mode():
            outputs = model.generate(
                **inputs, max_new_tokens=self.settings.max_new_tokens, min_new_tokens=16,
                do_sample=True, temperature=self.settings.temperature,
                top_p=0.92, top_k=50, repetition_penalty=1.15,
                no_repeat_ngram_size=3, num_return_sequences=3,
                pad_token_id=tokenizer.eos_token_id,
            )
        return [clean_text(tokenizer.decode(row[prompt_length:], skip_special_tokens=True)) for row in outputs]

    def generate(self, context, language='pt'):
        if language not in ('pt', 'en'):
            raise ValueError('Idioma não suportado.')
        if not isinstance(context, str) or not context.strip():
            raise ValueError('O contexto não pode estar vazio.')
        with self._lock:
            try:
                english = self._translate([context], 'pt_en')[0] if language == 'pt' else context
                if not english.strip():
                    raise ValueError('A tradução do contexto ficou vazia.')
                choices = self._generate_english(english)
                if language == 'pt':
                    choices = self._translate(choices, 'en_pt')
                if len(choices) != 3 or any(not t.strip() for t in choices):
                    raise ValueError('O modelo devolveu uma continuação vazia.')
                return choices
            except ModelUnavailable:
                raise
            except Exception as exc:
                logger.exception('Generation failed')
                raise ModelUnavailable(
                    'Não foi possível gerar o conto. Confirma a Internet no primeiro uso, '
                    'o espaço em disco, a memória e os modelos do .env. '
                    'O modo English usa apenas GPT-2 e dispensa os tradutores. '
                    'Detalhes técnicos estão no terminal.'
                ) from exc

    def status(self):
        return {'generator_loaded': self._generator is not None, 'translation_models_loaded': len(self._translators)}


@lru_cache(maxsize=1)
def get_engine():
    return StoryEngine()
