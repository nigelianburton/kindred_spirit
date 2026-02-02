"""
Convert the Nigel LoRA adapter to GGUF format for llama-server.

This script:
1. Loads the base Qwen2.5-7B model
2. Merges the LoRA adapter weights
3. Saves as a new standalone model
4. Converts to GGUF format using llama.cpp tools

Usage: conda activate train_for_nigel && python convert_to_gguf.py
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os
import subprocess
from pathlib import Path

# Configuration
BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"
ADAPTER_PATH = "./nigel_lora_adapter"
MERGED_MODEL_PATH = "./nigel_merged_model"
GGUF_OUTPUT_PATH = "./nigel_merged_model.gguf"

# Quantization options
QUANTIZATION_LEVELS = {
    "Q4_K_M": "Recommended - Good balance of size and quality",
    "Q5_K_M": "Higher quality, larger size",
    "Q6_K": "Very high quality, even larger",
    "Q8_0": "Maximum quality, largest size",
    "Q4_K_S": "Smaller size, slightly lower quality"
}

def merge_adapter():
    """Merge LoRA adapter with base model"""
    print("="*80)
    print("STEP 1: Merging LoRA adapter with base model")
    print("="*80)
    
    if not os.path.exists(ADAPTER_PATH):
        print(f"ERROR: Adapter not found at {ADAPTER_PATH}")
        return False
    
    print(f"\nLoading base model: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print(f"Loading LoRA adapter: {ADAPTER_PATH}")
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    
    print("Merging adapter weights into base model...")
    model = model.merge_and_unload()
    
    print(f"\nSaving merged model to: {MERGED_MODEL_PATH}")
    os.makedirs(MERGED_MODEL_PATH, exist_ok=True)
    model.save_pretrained(MERGED_MODEL_PATH)
    tokenizer.save_pretrained(MERGED_MODEL_PATH)
    
    print("✓ Merge complete!\n")
    return True

def convert_to_gguf(quant_level="Q4_K_M"):
    """Convert merged model to GGUF format"""
    print("="*80)
    print("STEP 2: Converting to GGUF format")
    print("="*80)
    
    # Check for llama.cpp convert script
    llamacpp_path = Path("C:/Llama")
    convert_script = llamacpp_path / "convert_hf_to_gguf.py"
    quantize_exe = llamacpp_path / "llama-quantize.exe"
    
    if not convert_script.exists():
        print(f"\nERROR: llama.cpp convert script not found at {convert_script}")
        print("\nManual conversion instructions:")
        print(f"1. Download llama.cpp from https://github.com/ggerganov/llama.cpp")
        print(f"2. Run: python convert_hf_to_gguf.py {MERGED_MODEL_PATH}")
        print(f"3. Run: llama-quantize {MERGED_MODEL_PATH}/model.gguf {GGUF_OUTPUT_PATH} {quant_level}")
        return False
    
    # Convert to GGUF (FP16 first)
    print(f"\nConverting to FP16 GGUF...")
    fp16_output = f"{MERGED_MODEL_PATH}/model-f16.gguf"
    
    cmd = [
        "python",
        str(convert_script),
        str(MERGED_MODEL_PATH),
        "--outtype", "f16",
        "--outfile", fp16_output
    ]
    
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("✓ FP16 conversion complete!\n")
    except subprocess.CalledProcessError as e:
        print(f"ERROR during conversion: {e}")
        print(e.stderr)
        return False
    
    # Quantize
    if quantize_exe.exists():
        print(f"Quantizing to {quant_level}...")
        quantized_output = f"nigel_merged_{quant_level}.gguf"
        
        cmd = [
            str(quantize_exe),
            fp16_output,
            quantized_output,
            quant_level
        ]
        
        print(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"✓ Quantization complete!\n")
            print(f"Final GGUF model: {quantized_output}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"ERROR during quantization: {e}")
            print(e.stderr)
            return False
    else:
        print(f"✓ FP16 GGUF created: {fp16_output}")
        print(f"\nNote: llama-quantize not found. You can quantize manually:")
        print(f"  llama-quantize {fp16_output} nigel_merged_{quant_level}.gguf {quant_level}")
        return True

def main():
    print("\n" + "="*80)
    print("NIGEL VALUES MODEL - LoRA to GGUF Converter")
    print("="*80 + "\n")
    
    # Choose quantization level
    print("Available quantization levels:")
    for i, (level, desc) in enumerate(QUANTIZATION_LEVELS.items(), 1):
        print(f"{i}. {level:10} - {desc}")
    
    print("\nRecommended: Q4_K_M (best balance of quality and size)")
    choice = input("\nSelect quantization level (1-5) or press Enter for Q4_K_M: ").strip()
    
    if choice:
        try:
            idx = int(choice) - 1
            quant_level = list(QUANTIZATION_LEVELS.keys())[idx]
        except (ValueError, IndexError):
            print("Invalid choice, using Q4_K_M")
            quant_level = "Q4_K_M"
    else:
        quant_level = "Q4_K_M"
    
    print(f"\nUsing quantization level: {quant_level}\n")
    
    # Step 1: Merge adapter
    if not merge_adapter():
        return
    
    # Step 2: Convert to GGUF
    convert_to_gguf(quant_level)
    
    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
    print(f"\nYour Nigel-tuned model is ready!")
    print(f"\nTo use with llama-server:")
    print(f"1. Copy the .gguf file to your models directory")
    print(f"2. Update ChatLlama settings to point to the new model")
    print(f"3. Launch and test with value-based scenarios")

if __name__ == "__main__":
    main()
