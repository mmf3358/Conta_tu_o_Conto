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
    
    
    
stopping_criteria = DotStoppingCriteria()
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
    
    train_dataset = load_dataset(train_file_path, tokenizer)
    
    data_collator = load_data_collator(tokenizer)
    
    tokenizer.save_pretrained(output_dir)
    
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.config.attention_dropout = 0.1  
    model.config.dropout = 0.1  
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
    
    trainer.train()
    trainer.save_model()
    
    
    
def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model



def load_tokenizer(tokenizer_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer



def generate_text(sequence,temperature = TEMPERATURE):
    gerador = pipeline('text-generation',model=MODEL_PATH)
    return gerador(
        sequence,
        max_length=80,
        min_length=35,
        truncation=True,
        pad_token_id=50256,
        stopping_criteria=stopping_criteria,
        do_sample=True,
        temperature=temperature
    )
    
    
    
def summarizer(output,max_length,min_length):
    summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL,stopping_criteria=stopping_criteria)
    return summarizer(
        output,
        do_sample=False,
        max_length=max_length,
        min_length=min_length
        )
    
    
    
def translator(inputs,model,max_length,min_length):
    translator = pipeline("translation", model)
    return translator(inputs,
                     do_sample= False,
                     max_length=max_length,
                     min_length=min_length
                    )