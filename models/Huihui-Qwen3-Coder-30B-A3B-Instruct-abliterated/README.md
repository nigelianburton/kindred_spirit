# Huihui Qwen3 Coder 30B A3B Instruct - Abliterated

## Model Information

- **Model**: Huihui Qwen3 Coder 30B A3B Instruct (Abliterated)
- **Size**: 30 billion parameters
- **Source**: [mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-i1-GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-i1-GGUF)
- **Format**: GGUF (quantized for efficient inference)
- **Abliteration**: Refusal behaviors removed via orthogonalization
- **Specialization**: Code-focused with strong ethical reasoning

## What Makes This Special?

This model combines:
- **Qwen3**: Alibaba's latest architecture with excellent multilingual support
- **Coder**: Enhanced code understanding and generation
- **A3B**: Alignment without corporate censorship
- **Abliteration**: Responds to all queries without refusal

## Download Instructions

### Option 1: Using huggingface-cli

```bash
# Install huggingface-hub if needed
pip install huggingface-hub

# Download the model (choose quantization level)
huggingface-cli download mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-i1-GGUF \
  --local-dir models/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated \
  --local-dir-use-symlinks False
```

### Option 2: Manual Download

1. Visit [mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-i1-GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-i1-GGUF)
2. Download your preferred quantization:
   - `Q4_K_M` - Good balance (recommended)
   - `Q5_K_M` - Better quality
   - `Q6_K` - Near-full quality
   - `IQ4_XS` - Innovative quantization (smaller, good quality)
3. Place files in this directory

## Fine-Tuning Setup

### Directory Structure

```
models/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated/
├── README.md (this file)
├── Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated.Q4_K_M.gguf (download)
├── lora_adapter/ (created during training)
│   ├── adapter_config.json
│   └── adapter_model.safetensors
└── training_logs/ (created during training)
```

## Training Configuration

Recommended LoRA settings for 30B model:
- **LoRA Rank**: 32-64
- **LoRA Alpha**: 64-128
- **Target Modules**: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- **Batch Size**: 1-2 (depending on VRAM)
- **Gradient Accumulation**: 8-16 steps
- **Learning Rate**: 1e-4 to 2e-4

## Hardware Requirements

- **VRAM**: 48GB+ (RTX 6000 Ada recommended)
- **RAM**: 64GB+
- **Storage**: 25-35GB for model files
- **Training Time**: 2-5 hours for 74 questions

## Testing

After fine-tuning, test with:
```bash
python 4_test_kindred_adapter.py --model Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated
```

## Model Characteristics

- **Strengths**: 
  - Code generation and understanding
  - Ethical reasoning without censorship
  - Multilingual support (excellent Chinese/English)
  - Long context handling
- **Architecture**: Qwen3 (Alibaba's Transformer variant)
- **Context Length**: 32768 tokens (32K!)
- **License**: Apache 2.0 (fully open source)

## Why Qwen3 Coder?

1. **Code Ethics**: Understanding both technical and ethical implications of code
2. **Reasoning**: Strong logical reasoning for ethical dilemmas
3. **Context**: 32K context handles full conversations
4. **Open**: Apache 2.0 license - truly yours

## Notes

- GGUF format optimized for inference
- A3B alignment means it starts closer to uncensored reasoning
- Abliteration removes remaining refusals
- Fine-tuning will align with YOUR ethical framework
- Strong performance on coding + ethics combination
