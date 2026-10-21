"""Hugging Face inference and optional LoRA training utilities."""
from functools import lru_cache
import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling,
    Trainer, TrainingArguments, pipeline,
)
from peft import LoraConfig, TaskType, get_peft_model
from project.params import (
    MODEL_PATH, SUMMARIZATION_MODEL, R, LORA_ALPHA, LORA_DROPOUT,
    LEARNING_RATE, LOGGING_STEPS, TEMPERATURE,
)


@lru_cache(maxsize=8)
def _pipeline(task, model):
    if not model:
        raise RuntimeError(f"Modelo não configurado para {task}.")
    return pipeline(task, model=model)


def generate_text(sequence, temperature=TEMPERATURE):
    generator = _pipeline("text-generation", MODEL_PATH)
    return generator(sequence, max_new_tokens=65, do_sample=True,
                     temperature=temperature, pad_token_id=generator.tokenizer.eos_token_id)


def summarizer(output, max_length=24, min_length=5):
    if not output.strip():
        return [{"summary_text": ""}]
    return _pipeline("summarization", SUMMARIZATION_MODEL)(
        output, max_length=max_length, min_length=min_length, do_sample=False, truncation=True
    )


def translator(inputs, model, max_length=128, min_length=1):
    return _pipeline("translation", model)(
        inputs, max_length=max_length, min_length=min_length, truncation=True
    )


def train(train_file_path, model_name, output_dir, overwrite_output_dir,
          per_device_train_batch_size, num_train_epochs, save_steps):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    with open(train_file_path, encoding="utf-8") as source:
        text = source.read()
    tokens = tokenizer(text, return_tensors="pt", truncation=False)["input_ids"][0]
    block_size = 128
    blocks = [tokens[i:i + block_size].tolist()
              for i in range(0, len(tokens), block_size)
              if len(tokens[i:i + block_size]) >= 8]
    if not blocks:
        raise ValueError("O ficheiro de treino não contém texto suficiente.")
    dataset = [{"input_ids": item, "attention_mask": [1] * len(item)} for item in blocks]
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model = get_peft_model(model, LoraConfig(
        task_type=TaskType.CAUSAL_LM, inference_mode=False,
        r=R, lora_alpha=LORA_ALPHA, lora_dropout=LORA_DROPOUT
    ))
    args = TrainingArguments(
        output_dir=output_dir, overwrite_output_dir=overwrite_output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        num_train_epochs=num_train_epochs, save_steps=save_steps,
        learning_rate=LEARNING_RATE, logging_steps=LOGGING_STEPS,
        report_to="none"
    )
    trainer = Trainer(
        model=model, args=args, train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)


def load_model(model_path):
    return AutoModelForCausalLM.from_pretrained(model_path)


def load_tokenizer(tokenizer_path):
    return AutoTokenizer.from_pretrained(tokenizer_path)
