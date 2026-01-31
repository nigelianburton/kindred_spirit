# Huihui GPT OSS 20B BF16 - Abliterated v2

## Model Information

- **Model**: Huihui GPT OSS 20B BF16 (Abliterated v2)
- **Size**: 20 billion parameters
- **Source**: [huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated-v2l](https://huggingface.co/huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated-v2l)
- **Format**: BF16 (BFloat16 precision - full weights)
- **Abliteration**: v2 - Enhanced refusal removal
- **Special Feature**: GPT architecture variant, fully open source

## What Makes This Special?

- **BF16 Format**: Brain Float 16 - better than FP16 for training
- **GPT Architecture**: Different from Qwen/Gemma - good for comparison
- **Fully Open**: OSS (Open Source Software) variant
- **Mid-Size**: 20B - sweet spot between quality and efficiency
- **v2 Abliteration**: Improved refusal removal process

## Download Instructions

### Option 1: Using huggingface-cli

```bash
# Install huggingface-hub if needed
pip install huggingface-hub

# Download the model
huggingface-cli download huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated-v2l \
  --local-dir models/Huihui-gpt-oss-20b-BF16-abliterated-v2 \
  --local-dir-use-symlinks False
```

### Option 2: Manual Download

1. Visit [huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated-v2l](https://huggingface.co/huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated-v2l)
2. Download all model files:
   - `model-*.safetensors` (multiple shards)
   - `config.json`
   - `tokenizer.json`
   - `tokenizer_config.json`
3. Place files in this directory

## Fine-Tuning Setup

### Directory Structure

```
models/Huihui-gpt-oss-20b-BF16-abliterated-v2/
├── README.md (this file)
├── config.json (download)
├── model-00001-of-00004.safetensors (download)
├── model-00002-of-00004.safetensors (download)
├── model-00003-of-00004.safetensors (download)
├── model-00004-of-00004.safetensors (download)
├── tokenizer.json (download)
├── tokenizer_config.json (download)
├── lora_adapter/ (created during training)
│   ├── adapter_config.json
│   └── adapter_model.safetensors
└── training_logs/ (created during training)
```

## Training Configuration

Recommended LoRA settings for 20B model:
- **LoRA Rank**: 64-128
- **LoRA Alpha**: 128-256
- **Target Modules**: q_proj, v_proj, k_proj, o_proj, mlp.up_proj, mlp.down_proj
- **Batch Size**: 2-4
- **Gradient Accumulation**: 4-8 steps
- **Learning Rate**: 2e-4 to 3e-4
- **Precision**: BF16 (native format)

## Hardware Requirements

- **VRAM**: 48GB+ for training (24GB for inference)
- **RAM**: 48GB+
- **Storage**: 40-50GB for model files (BF16 is larger)
- **Training Time**: 2-3 hours for 74 questions

## Testing

After fine-tuning, test with:
```bash
python 4_test_kindred_adapter.py --model Huihui-gpt-oss-20b-BF16-abliterated-v2
```

## Model Characteristics

- **Strengths**: 
  - GPT architecture (proven effective)
  - BF16 precision (better training stability)
  - Mid-size efficiency
  - Open source transparency
- **Architecture**: GPT variant (decoder-only Transformer)
- **Context Length**: 8192 tokens
- **License**: Fully open source

## Why BF16 Format?

BFloat16 (Brain Float 16) advantages:
- **Training Stability**: Better than FP16 for fine-tuning
- **Dynamic Range**: Same as FP32, better than FP16
- **Hardware Support**: Modern GPUs (Ampere+) have BF16 acceleration
- **LoRA Compatible**: Excellent for LoRA fine-tuning

## GPT Architecture Benefits

Compared to Qwen/Gemma:
- Different attention patterns
- Proven track record
- Extensive research backing
- Good baseline for comparison

## v2 Abliteration Features

The v2 abliteration process:
- More complete refusal removal
- Better capability preservation
- Improved ethical reasoning
- Fewer edge case refusals

## Notes

- This is NOT a quantized model - full BF16 weights
- Larger file size but better training results
- GPT architecture provides good comparison to Qwen/Gemma
- 20B parameters - sweet spot for quality/efficiency
- BF16 format ideal for LoRA fine-tuning
- May need more disk space than GGUF models
