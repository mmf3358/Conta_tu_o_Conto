from dataclasses import dataclass
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv(ROOT / '.env', override=False)


@dataclass(frozen=True)
class Settings:
    model: str = 'openai-community/gpt2'
    translator_pt_en: str = 'Helsinki-NLP/opus-mt-ROMANCE-en'
    translator_en_pt: str = 'Helsinki-NLP/opus-mt-tc-big-en-pt'
    portuguese_prefix: str = '>>por<< '
    device: str = 'cpu'
    max_new_tokens: int = 80
    temperature: float = 0.85
    context_tokens: int = 384
    local_files_only: bool = False

    @classmethod
    def from_env(cls):
        settings = cls(
            model=os.getenv('MODEL_NAME', cls.model),
            translator_pt_en=os.getenv('TRANSLATOR_PT_EN', cls.translator_pt_en),
            translator_en_pt=os.getenv('TRANSLATOR_EN_PT', cls.translator_en_pt),
            portuguese_prefix=os.getenv('PORTUGUESE_PREFIX', '>>por<< '),
            device=os.getenv('DEVICE', 'cpu'),
            max_new_tokens=int(os.getenv('MAX_NEW_TOKENS', '80')),
            temperature=float(os.getenv('TEMPERATURE', '0.85')),
            context_tokens=int(os.getenv('CONTEXT_TOKENS', '384')),
            local_files_only=os.getenv('LOCAL_FILES_ONLY', '0') == '1',
        )
        if not 16 <= settings.max_new_tokens <= 160:
            raise ValueError('MAX_NEW_TOKENS deve estar entre 16 e 160.')
        if not 0.1 <= settings.temperature <= 2:
            raise ValueError('TEMPERATURE deve estar entre 0.1 e 2.')
        if not 64 <= settings.context_tokens <= 384:
            raise ValueError('CONTEXT_TOKENS deve estar entre 64 e 384.')
        return settings
