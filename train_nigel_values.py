"""
Train Nigel-aligned LoRA adapter on Qwen2-VL-7B-Instruct-abliterated
Optimized for single RTX 6000 Ada (48GB VRAM)
"""
import os
import json
import torch
from pathlib import Path
from datasets import Dataset, load_dataset, concatenate_datasets
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

CONFIG = {
    # Model selection - Using Qwen2.5 standard (not VL) for simplicity
    # VL models require special handling for vision tokens
    "model_name": "Qwen/Qwen2.5-7B-Instruct",  # Standard text model, easier to train
    # Note: For multimodal later, can use Qwen2-VL or LLaVA
    
    # Training data
    "nigel_data_path": "training_data/nigel_values_chat.json",
    "use_general_data": True,  # Mix with general examples to prevent forgetting
    "general_data_samples": 400,  # Number of general examples (3:1 ratio with Nigel's 132)
    
    # LoRA hyperparameters
    "lora_r": 64,  # Rank (higher = more capacity but slower)
    "lora_alpha": 16,  # Scaling factor
    "lora_dropout": 0.05,
    "lora_target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],  # Which layers to adapt
    
    # Training hyperparameters
    "num_epochs": 2,
    "batch_size": 8,  # Per device (48GB can handle this)
    "gradient_accumulation_steps": 2,  # Effective batch = 8*2=16
    "learning_rate": 1e-5,  # Low LR for abliterated base
    "weight_decay": 0.01,
    "warmup_steps": 50,
    "max_seq_length": 2048,
    
    # Output
    "output_dir": "./nigel_lora_adapter",
    "save_steps": 50,
    "logging_steps": 10,
    
    # Hardware
    "use_flash_attention": False,  # Disable for compatibility
    "gradient_checkpointing": True,  # Saves VRAM
    "fp16": True,  # Mixed precision training
}

# ============================================================================
# Load and prepare data
# ============================================================================

def load_nigel_data():
    """Load Nigel's value training data"""
    with open(CONFIG["nigel_data_path"]) as f:
        data = json.load(f)
    
    # Convert to HF dataset format
    formatted = []
    for item in data:
        messages = item["messages"]
        # Format as conversation
        text = f"<|im_start|>user\n{messages[0]['content']}<|im_end|>\n<|im_start|>assistant\n{messages[1]['content']}<|im_end|>"
        formatted.append({"text": text})
    
    return Dataset.from_list(formatted)

def load_general_data(n_samples=400):
    """Load general instruction data to prevent catastrophic forgetting"""
    logger.info(f"Loading {n_samples} general instruction examples...")
    
    # Load from HuggingFace datasets
    try:
        # Option 1: Alpaca cleaned
        dataset = load_dataset("yahma/alpaca-cleaned", split=f"train[:{n_samples}]")
        
        # Format to match our style
        formatted = []
        for item in dataset:
            if item.get("input"):
                prompt = f"{item['instruction']}\n{item['input']}"
            else:
                prompt = item["instruction"]
            
            text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n{item['output']}<|im_end|>"
            formatted.append({"text": text})
        
        return Dataset.from_list(formatted)
    
    except Exception as e:
        logger.warning(f"Could not load general data: {e}")
        logger.warning("Training without general examples (higher risk of catastrophic forgetting)")
        return None

def prepare_dataset():
    """Combine Nigel's data with general examples"""
    nigel_data = load_nigel_data()
    logger.info(f"Loaded {len(nigel_data)} Nigel value examples")
    
    if CONFIG["use_general_data"]:
        general_data = load_general_data(CONFIG["general_data_samples"])
        if general_data:
            combined = concatenate_datasets([nigel_data, general_data])
            logger.info(f"Combined dataset: {len(combined)} total examples ({len(nigel_data)} values + {len(general_data)} general)")
            return combined.shuffle(seed=42)
    
    return nigel_data.shuffle(seed=42)

# ============================================================================
# Model setup
# ============================================================================

def setup_model_and_tokenizer():
    """Load base model and tokenizer"""
    logger.info(f"Loading model: {CONFIG['model_name']}")
    
    # Set environment variable to handle OpenMP conflict
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        CONFIG["model_name"],
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # Load model with optimizations
    model_kwargs = {
        "torch_dtype": torch.float16 if CONFIG["fp16"] else torch.float32,
        "device_map": "auto",
        "trust_remote_code": True,
    }
    
    # Only add flash attention if enabled
    if CONFIG.get("use_flash_attention"):
        model_kwargs["use_flash_attention_2"] = True
    
    model = AutoModelForCausalLM.from_pretrained(
        CONFIG["model_name"],
        **model_kwargs
    )
    
    # Enable gradient checkpointing to save VRAM
    if CONFIG["gradient_checkpointing"]:
        model.gradient_checkpointing_enable()
    
    return model, tokenizer

def setup_lora(model):
    """Configure and apply LoRA adapter"""
    logger.info("Setting up LoRA adapter...")
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=CONFIG["lora_r"],
        lora_alpha=CONFIG["lora_alpha"],
        lora_dropout=CONFIG["lora_dropout"],
        target_modules=CONFIG["lora_target_modules"],
        bias="none",
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model

# ============================================================================
# Training
# ============================================================================

def tokenize_function(examples, tokenizer):
    """Tokenize dataset"""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=CONFIG["max_seq_length"],
        padding="max_length",
    )

def train():
    """Main training loop"""
    # Setup
    model, tokenizer = setup_model_and_tokenizer()
    model = setup_lora(model)
    
    # Prepare data
    dataset = prepare_dataset()
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=dataset.column_names
    )
    
    # Split train/val
    split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = split["train"]
    eval_dataset = split["test"]
    
    logger.info(f"Training on {len(train_dataset)} examples, validating on {len(eval_dataset)}")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=CONFIG["output_dir"],
        num_train_epochs=CONFIG["num_epochs"],
        per_device_train_batch_size=CONFIG["batch_size"],
        per_device_eval_batch_size=CONFIG["batch_size"],
        gradient_accumulation_steps=CONFIG["gradient_accumulation_steps"],
        learning_rate=CONFIG["learning_rate"],
        weight_decay=CONFIG["weight_decay"],
        warmup_steps=CONFIG["warmup_steps"],
        logging_steps=CONFIG["logging_steps"],
        save_steps=CONFIG["save_steps"],
        eval_steps=CONFIG["save_steps"],
        eval_strategy="steps",
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        fp16=CONFIG["fp16"],
        dataloader_pin_memory=True,
        remove_unused_columns=False,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )
    
    # Train
    logger.info("Starting training...")
    logger.info(f"Estimated time: {len(train_dataset) * CONFIG['num_epochs'] / (CONFIG['batch_size'] * CONFIG['gradient_accumulation_steps']) / 60:.1f} minutes")
    
    trainer.train()
    
    # Save final adapter
    logger.info(f"Saving final adapter to {CONFIG['output_dir']}")
    trainer.save_model()
    tokenizer.save_pretrained(CONFIG["output_dir"])
    
    logger.info("✅ Training complete!")
    logger.info(f"Adapter saved to: {CONFIG['output_dir']}")
    logger.info("\nTo use the adapter:")
    logger.info(f"  from peft import PeftModel")
    logger.info(f"  base_model = AutoModelForCausalLM.from_pretrained('{CONFIG['model_name']}')")
    logger.info(f"  model = PeftModel.from_pretrained(base_model, '{CONFIG['output_dir']}')")

# ============================================================================
# Validation helpers
# ============================================================================

def validate_general_capabilities(model, tokenizer):
    """Test that model hasn't forgotten basic capabilities"""
    test_prompts = [
        "What is 15 * 23?",
        "What is the capital of France?",
        "Write a Python function to reverse a string.",
        "Explain photosynthesis in simple terms.",
    ]
    
    logger.info("\n" + "="*60)
    logger.info("Testing general capabilities (checking for catastrophic forgetting):")
    logger.info("="*60)
    
    for prompt in test_prompts:
        inputs = tokenizer(f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n", return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.7)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"\nQ: {prompt}")
        logger.info(f"A: {response}")

if __name__ == "__main__":
    # Check CUDA
    if not torch.cuda.is_available():
        logger.error("CUDA not available! Training will be very slow.")
    else:
        logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"Available VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Train
    train()
