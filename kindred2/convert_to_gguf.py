#!/usr/bin/env python3
"""
Convert a trained Kindred2 adapter to GGUF with Q4/Q6/Q8 presets.
"""
import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Kindred2 adapter to GGUF")
    parser.add_argument("--model-folder", required=True, help="Path to ethical model folder")
    parser.add_argument("--quant", default="Q4_K_M", help="Quantization preset (Q4_K_M/Q6_K/Q8_0)")
    return parser.parse_args(argv)


def resolve_base_model(model_folder: Path) -> str:
    base_model_file = model_folder / "base_model.txt"
    if base_model_file.exists():
        try:
            value = base_model_file.read_text(encoding="utf-8").strip()
            if value:
                return value
        except Exception:
            pass
    return "D:/_GITN/kindred_spirit/models/Huihui-Qwen3-VL-8B-Instruct-abliterated"


def merge_adapter(base_model: str, adapter_path: Path, merged_path: Path) -> None:
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True
    )
    model = PeftModel.from_pretrained(model, str(adapter_path))
    model = model.merge_and_unload()

    merged_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(merged_path)
    tokenizer.save_pretrained(merged_path)


def convert_hf_to_gguf(merged_path: Path, gguf_path: Path, quant: str) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    llama_dir = repo_root / "llama.cpp"
    convert_script = llama_dir / "convert_hf_to_gguf.py"

    if not convert_script.exists():
        raise FileNotFoundError(f"llama.cpp convert script not found: {convert_script}")

    fp16_out = gguf_path.with_suffix("").with_name(gguf_path.stem + "-f16.gguf")

    cmd = [
        "python",
        str(convert_script),
        str(merged_path),
        "--outtype", "f16",
        "--outfile", str(fp16_out)
    ]
    subprocess.run(cmd, check=True)

    quantize_exe = None
    for name in ["llama-quantize.exe", "llama-quantize"]:
        candidate = llama_dir / name
        if candidate.exists():
            quantize_exe = candidate
            break

    if quantize_exe:
        cmd = [str(quantize_exe), str(fp16_out), str(gguf_path), quant]
        subprocess.run(cmd, check=True)
    else:
        fp16_out.replace(gguf_path)


def main() -> None:
    args = parse_args(__import__("sys").argv[1:])
    model_folder = Path(args.model_folder)
    if not model_folder.exists():
        raise FileNotFoundError(f"Model folder not found: {model_folder}")

    adapter_path = model_folder / "finetuned_adapter"
    if not adapter_path.exists():
        raise FileNotFoundError(f"finetuned_adapter not found: {adapter_path}")

    base_model = resolve_base_model(model_folder)
    merged_path = model_folder / "merged_model"

    merge_adapter(base_model, adapter_path, merged_path)

    quant = args.quant
    gguf_name = f"finetuned_model_{quant}.gguf".lower()
    gguf_path = model_folder / gguf_name

    convert_hf_to_gguf(merged_path, gguf_path, quant)


if __name__ == "__main__":
    main()
