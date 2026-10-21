from transformers import pipeline
from transformers.generation.stopping_criteria import StoppingCriteria
import torch
class DotStoppingCriteria(StoppingCriteria):
    def __init__(self):
        super().__init__()
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        return torch.any(input_ids == 46)  # 46 is the index of the dot (.) in the tokenizer
    def __len__(self):
        return 1
    def __iter__(self):
        return iter([self])
# Load the model and tokenizer
model = pipeline('text-generation', model='gpt2')
# Create an instance of the custom stopping criteria
stopping_criteria = DotStoppingCriteria()
# Generate text with the stopping criteria
output = model("Hello, I'm a language model,", max_length=60, num_return_sequences=1, truncation=True, pad_token_id=50256, stopping_criteria=stopping_criteria)
# Generate text with the stopping criteria
output = model("Hello, I'm a language model,", max_length=60, num_return_sequences=1, truncation=True, pad_token_id=50256, stopping_criteria=stopping_criteria)
