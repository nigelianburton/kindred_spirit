# Qwen3 VL 8B Instruct - Abliterated v2.0

## Model Information

- **Model**: Qwen3 VL 8B Instruct (Abliterated v2.0)
- **Size**: 8 billion parameters
- **Source**: [mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF](https://huggingface.co/mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF)
- **Format**: GGUF (quantized for efficient inference)
- **Abliteration**: v2.0 - Enhanced refusal removal
- **Special Feature**: Vision-Language model (multimodal)

## What Makes This Special?

This model is unique in the set:
- **Vision + Language**: Can process images AND text
- **Multimodal Ethics**: Can reason about visual ethical dilemmas
- **Smaller Size**: 8B parameters - faster, less VRAM
- **v2.0 Abliteration**: Improved refusal removal technique

## Use Cases for Multimodal Ethics

While the calibration uses text only, this model enables:
- Visual ethical dilemmas (photos, art, scenarios)
- Understanding context from images
- Ethical analysis of visual content
- Combining vision with your personal values

## Download Instructions

### Option 1: Using huggingface-cli

```bash
# Install huggingface-hub if needed
pip install huggingface-hub

# Download the model (choose quantization level)
huggingface-cli download mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF \
  --local-dir models/Qwen3-VL-8B-Instruct-abliterated-v2.0 \
  --local-dir-use-symlinks False
```

### Option 2: Manual Download

1. Visit [mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF](https://huggingface.co/mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF)
2. Download your preferred quantization:
   - `Q4_K_M` - Good balance (recommended)
   - `Q5_K_M` - Better quality
   - `Q6_K` - Near-full quality
3. Place files in this directory

## Fine-Tuning Setup

### Directory Structure

```
models/Qwen3-VL-8B-Instruct-abliterated-v2.0/
├── README.md (this file)
├── Qwen3-VL-8B-Instruct-abliterated-v2.0.Q4_K_M.gguf (download)
├── lora_adapter/ (created during training)
│   ├── adapter_config.json
│   └── adapter_model.safetensors
└── training_logs/ (created during training)
```

## Training Configuration

Recommended LoRA settings for 8B model:
- **LoRA Rank**: 64-128
- **LoRA Alpha**: 128-256
- **Target Modules**: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- **Batch Size**: 2-4 (more room with smaller model)
- **Gradient Accumulation**: 4-8 steps
- **Learning Rate**: 2e-4 to 3e-4

## Hardware Requirements

- **VRAM**: 24GB+ (RTX 3090/4090 sufficient)
- **RAM**: 32GB+
- **Storage**: 8-12GB for model files
- **Training Time**: 1-2 hours for 74 questions

## Testing

After fine-tuning, test with:
```bash
python 4_test_kindred_adapter.py --model Qwen3-VL-8B-Instruct-abliterated-v2.0
```

## Model Characteristics

- **Strengths**: 
  - Vision + language understanding
  - Efficient (smaller, faster)
  - Good reasoning for size
  - Multimodal ethical analysis
- **Architecture**: Qwen3-VL (vision-language)
- **Context Length**: 8192 tokens
- **License**: Apache 2.0 (fully open source)

## Vision Capabilities

While not used in text calibration, this model can:
- Analyze images through ethical lens
- Understand visual context
- Process diagrams, charts, photos
- Combine visual + text reasoning

## v2.0 Abliteration Improvements

The v2.0 abliteration process:
- More thorough refusal removal
- Better preservation of capabilities
- Improved ethical reasoning
- Reduced false refusals

## Notes

- Smallest model in the test set - good for comparison
- Multimodal capability unique among test models
- Fast inference and training
- Good for testing if 8B is sufficient for personal ethics
- Can be expanded to visual ethics scenarios later
