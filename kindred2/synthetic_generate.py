#!/usr/bin/env python3
"""
Generate synthetic Q&A from user answers using a small HF model.
"""
import argparse
import json
import re
from pathlib import Path
from typing import List, Dict

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic Q&A")
    parser.add_argument("--user-answers", required=True, help="Path to user_answers.json")
    parser.add_argument("--output", required=True, help="Path to synthetic_qa.json output")
    parser.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct", help="HF model name")
    parser.add_argument("--count", type=int, default=30, help="Number of synthetic items")
    return parser.parse_args(argv)


def extract_examples(user_answers: Dict, max_items: int = 30) -> List[Dict[str, str]]:
    responses = user_answers.get("responses", [])
    examples = []
    for item in responses[:max_items]:
        examples.append({
            "question": item.get("question", ""),
            "choice": item.get("choice", ""),
            "confidence": item.get("confidence", ""),
            "response": item.get("response", "")
        })
    return examples


def build_prompt(examples: List[Dict[str, str]], count: int) -> str:
    def format_example(ex: Dict[str, str]) -> str:
        if ex.get("response"):
            return f"- Q: {ex['question']} | Response: {ex['response']} | Confidence: {ex.get('confidence', '')}"
        return f"- Q: {ex['question']} | Choice: {ex.get('choice', '')} | Confidence: {ex.get('confidence', '')}"

    samples_text = "\n".join(
        format_example(ex) for ex in examples if ex.get("question")
    )
    return (
        "You are helping generate synthetic ethics Q&A for a single user. "
        "Infer the user's values from these answered questions and generate new Q&A that match their style.\n\n"
        "Answered examples:\n"
        f"{samples_text}\n\n"
        "Output ONLY a JSON array. Each item must have: instruction, response. "
        f"Generate exactly {count} items. Avoid political slogans; keep answers concise, nuanced, and in the user's voice."
    )


def extract_json_array(text: str) -> List[Dict]:
    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        raise ValueError("No JSON array found in model output")
    return json.loads(match.group(0))


def main() -> None:
    args = parse_args(__import__("sys").argv[1:])
    user_answers_path = Path(args.user_answers)
    output_path = Path(args.output)

    if not user_answers_path.exists():
        raise FileNotFoundError(f"user_answers.json not found: {user_answers_path}")

    user_answers = json.loads(user_answers_path.read_text(encoding="utf-8"))
    examples = extract_examples(user_answers)
    prompt = build_prompt(examples, args.count)

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        device_map="auto",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        trust_remote_code=True
    )

    messages = [
        {"role": "system", "content": "You output only strict JSON arrays."},
        {"role": "user", "content": prompt}
    ]

    try:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    except Exception:
        text = messages[-1]["content"]

    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=1200,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    items = extract_json_array(decoded)
    cleaned = []
    for item in items:
        instruction = str(item.get("instruction", "")).strip()
        response = str(item.get("response", "")).strip()
        if instruction and response:
            cleaned.append({"instruction": instruction, "response": response})

    if not cleaned:
        raise ValueError("No valid synthetic items generated")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
