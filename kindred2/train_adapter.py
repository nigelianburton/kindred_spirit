#!/usr/bin/env python3
"""
Train a LoRA adapter from synthetic Q&A within a selected model folder.
"""
import argparse
import json
import os
import shutil
from pathlib import Path
from typing import List

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, TaskType


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Kindred2 LoRA adapter")
    parser.add_argument("--model-folder", required=True, help="Path to ethical model folder")
    parser.add_argument(
        "--base-model",
        default="D:/_GITN/kindred_spirit/models/Huihui-Qwen3-VL-8B-Instruct-abliterated",
        help="HF base model or local path"
    )
    parser.add_argument("--output-dir", default=None, help="Output directory for adapter")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=2048)
    return parser.parse_args(argv)


def load_synthetic_data(model_folder: Path) -> Dataset:
    synthetic_path = model_folder / "synthetic_qa.json"
    if not synthetic_path.exists():
        raise FileNotFoundError(f"synthetic_qa.json not found: {synthetic_path}")

    data = json.loads(synthetic_path.read_text(encoding="utf-8"))
    formatted = []
    for item in data:
        instruction = item.get("instruction", "").strip()
        response = item.get("response", "").strip()
        if not instruction or not response:
            continue
        text = (
            f"<|im_start|>user\n{instruction}<|im_end|>\n"
            f"<|im_start|>assistant\n{response}<|im_end|>"
        )
        formatted.append({"text": text})

    if not formatted:
        raise ValueError("No usable synthetic items found")

    return Dataset.from_list(formatted)


def setup_model_and_tokenizer(base_model: str):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True
    )
    model.gradient_checkpointing_enable()
    return model, tokenizer


def setup_lora(model):
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=32,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def tokenize_function(examples, tokenizer, max_length: int):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=max_length,
        padding="max_length",
    )


def main() -> None:
    args = parse_args(__import__("sys").argv[1:])
    model_folder = Path(args.model_folder)
    if not model_folder.exists():
        raise FileNotFoundError(f"Model folder not found: {model_folder}")

    output_dir = Path(args.output_dir) if args.output_dir else model_folder / "finetuned_adapter"

    dataset = load_synthetic_data(model_folder)
    model, tokenizer = setup_model_and_tokenizer(args.base_model)
    model = setup_lora(model)

    tokenized = dataset.map(lambda x: tokenize_function(x, tokenizer, args.max_length), batched=True)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=2,
        learning_rate=1e-5,
        weight_decay=0.01,
        logging_steps=10,
        save_steps=50,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=data_collator,
    )

    trainer.train()
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    adapter_file = output_dir / "adapter_model.safetensors"
    if adapter_file.exists():
        target_file = model_folder / "finetuned_model.safetensors"
        shutil.copy2(adapter_file, target_file)


if __name__ == "__main__":
    main()
