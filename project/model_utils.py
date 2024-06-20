from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from transformers.generation.stopping_criteria import StoppingCriteria
from peft import LoraConfig, TaskType, get_peft_model
from datasets import load_dataset

import pandas as pd
import numpy as np
import re
import torch

from project.params import *

class DotStoppingCriteria(StoppingCriteria):
    def __init__(self):
        super().__init__()
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        return torch.any(input_ids == 46)  # 46 is the index of the dot (.) in the tokenizer
    def __len__(self):
        return 1
    def __iter__(self):
        return iter([self])
    def stop(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        return torch.any(input_ids == 46) or torch.any(input_ids == 44)


device = 'cuda' if torch.cuda.is_available() else 'cpu'

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT

    )


def load_dataset(file_path, tokenizer, block_size = 128):
    dataset = TextDataset(
        tokenizer = tokenizer,
        file_path = file_path,
        block_size = block_size,
    )
    return dataset


def load_data_collator(tokenizer, mlm = False):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=mlm,
    )
    return data_collator


def train(train_file_path,model_name,
          output_dir,
          overwrite_output_dir,
          per_device_train_batch_size,
          num_train_epochs,
          save_steps):

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    
    print(f'\n\n\t Loading DataSet from {TRAIN_FILE_PATH} ...')
    train_dataset = load_dataset(train_file_path, tokenizer)
    data_collator = load_data_collator(tokenizer)

    tokenizer.save_pretrained(output_dir)

    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.config.attention_dropout = 0.1  # Exemplo de configuração de dropout para a camada de atenção
    model.config.dropout = 0.1  # Exemplo de configuração de dropout para outras camadas
    model = get_peft_model(model, peft_config)

    model.save_pretrained(output_dir)

    training_args = TrainingArguments(
          output_dir=output_dir,
          overwrite_output_dir=overwrite_output_dir,
          per_device_train_batch_size=per_device_train_batch_size,
          num_train_epochs=num_train_epochs,
          learning_rate=LEARNING_RATE,
          logging_steps=LOGGING_STEPS
    )


    trainer = Trainer(
          model=model,
          args=training_args,
          data_collator=data_collator,
          train_dataset=train_dataset,
    )
    print('\n\n\t Starting Training ...')
    trainer.train()
    
    print(f'\n\n\t Saving Trained Model at {MODEL_PATH} ...')
    trainer.save_model()


def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model


def load_tokenizer(tokenizer_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer




def generate_text(sequence, max_length, temperature = TEMPERATURE):
    model = load_model(MODEL_PATH)
    tokenizer = load_tokenizer(MODEL_PATH)
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
    final_outputs = model.generate(
        ids,
        do_sample=True,
        max_length=max_length,
        pad_token_id=model.config.eos_token_id,
        top_k=50,
        top_p=0.95,
    )
    return(tokenizer.decode(final_outputs[0], skip_special_tokens=True))


def summarizer(output):

    summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL)

    return summarizer(
        output,
        max_length=SUMMARIZER_MAX_LENGTH,
        min_length=SUMMARIZER_MIN_LENGTH,
        do_sample=False
        )

def translator(inputs,model):

    translator = pipeline("translation", model)

    return translator(inputs,
                     max_length= 256,
                     do_sample= False
                     )
