"""Story state independent of UI, models and network access."""
from dataclasses import dataclass, field
import re

MAX_CONTEXT_CHARS = 20000


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def make_context(name, age, occupation, theme, language='pt'):
    values = [name, str(age), occupation, theme]
    if not all(str(v).strip() for v in values):
        raise ValueError('Preenche todos os dados da personagem e escolhe um tema.')
    if language not in ('pt', 'en'):
        raise ValueError('Idioma não suportado.')
    name, age, occupation, theme = [clean_text(str(v)) for v in values]
    if language == 'en':
        places = {'Castelo': 'a mysterious castle', 'Floresta': 'an enchanted forest', 'Fadas': 'a fairy kingdom'}
        return f'Once upon a time, {name}, a {age}-year-old {occupation}, discovered {places[theme]}. It was the beginning of an unexpected adventure.'
    places = {'Castelo': 'um castelo misterioso', 'Floresta': 'uma floresta encantada', 'Fadas': 'um reino de fadas'}
    return f'Era uma vez, {name}, de {age} anos, que trabalhava como {occupation}. Um dia descobriu {places[theme]}. Era o início de uma aventura inesperada.'


def choice_label(text, limit=110):
    """Extractive preview, not a separate summarisation model."""
    text = clean_text(text)
    sentence = re.split(r'(?<=[.!?])\s+', text)[0]
    if len(sentence) <= limit:
        return sentence
    return sentence[:limit - 1].rsplit(' ', 1)[0] + '…'


@dataclass
class StoryState:
    title: str
    opening: str
    language: str = 'pt'
    paragraphs: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    round: int = 0

    @property
    def text(self):
        return '\n\n'.join([self.opening, *self.paragraphs])

    @property
    def prompt(self):
        # The downloadable story stays complete; model input uses recent context.
        return self.text[-MAX_CONTEXT_CHARS:]

    def ensure_choices(self, generate):
        if not self.alternatives:
            candidates = generate(self.prompt, self.language)
            if len(candidates) != 3 or any(not clean_text(t) for t in candidates):
                raise ValueError('O modelo não devolveu três continuações válidas. Tenta novamente.')
            self.alternatives = [clean_text(t) for t in candidates]
        return self.alternatives

    def choose(self, index):
        if index not in range(len(self.alternatives)):
            raise ValueError('Escolha inválida ou já utilizada.')
        self.paragraphs.append(self.alternatives[index])
        self.alternatives = []
        self.round += 1

    def export(self):
        return self.title.strip() + '\n\n' + self.text + '\n'
