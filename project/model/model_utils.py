from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from peft import LoraConfig, TaskType, get_peft_model
from datasets import load_dataset

import pandas as pd
import numpy as np
import re
import torch

from project.params import *

import os

print(os.getcwd())

print(TRAIN_FILE_PATH)

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

    trainer.train()
    trainer.save_model()
    
 
### Treina o Modelo
train(
    train_file_path=TRAIN_FILE_PATH,
    model_name=MODEL_NAME,
    output_dir=MODEL_PATH,
    overwrite_output_dir=True,
    per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
    num_train_epochs=NUM_TRAIN_EPOCHS,
    save_steps=SAVE_STEPS
)

