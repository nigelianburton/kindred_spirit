# Gemma 3 27B Instruct - Abliterated

## Model Information

- **Model**: Google Gemma 3 27B Instruct (Abliterated)
- **Size**: 27 billion parameters
- **Source**: [mlabonne/gemma-3-27b-it-abliterated-GGUF](https://huggingface.co/mlabonne/gemma-3-27b-it-abliterated-GGUF)
- **Format**: GGUF (quantized for efficient inference)
- **Abliteration**: Refusal behaviors removed via orthogonalization

## What is Abliteration?

Abliteration removes the model's refusal training without full retraining. The model:
- Responds to all queries without "I cannot assist with that" responses
- Still maintains knowledge and capabilities
- Can be fine-tuned to follow personal ethics rather than corporate guidelines

## Download Instructions

### Option 1: Using huggingface-cli

```bash
# Install huggingface-hub if needed
pip install huggingface-hub

# Download the model (choose quantization level)
huggingface-cli download mlabonne/gemma-3-27b-it-abliterated-GGUF \
  --local-dir models/gemma-3-27b-it-abliterated \
  --local-dir-use-symlinks False
```

### Option 2: Manual Download

1. Visit [mlabonne/gemma-3-27b-it-abliterated-GGUF](https://huggingface.co/mlabonne/gemma-3-27b-it-abliterated-GGUF)
2. Download your preferred quantization:
   - `Q4_K_M` - Good balance (recommended for 48GB VRAM)
   - `Q5_K_M` - Better quality, larger size
   - `Q6_K` - Near-full quality
   - `Q8_0` - Highest quality
3. Place files in this directory

## Fine-Tuning Setup

This model will be fine-tuned with your Kindred Spirit calibration data.

### Directory Structure

```
models/gemma-3-27b-it-abliterated/
├── README.md (this file)
├── gemma-3-27b-it-abliterated.Q4_K_M.gguf (download)
├── lora_adapter/ (created during training)
│   ├── adapter_config.json
│   └── adapter_model.safetensors
└── training_logs/ (created during training)
```

## Training Configuration

Recommended LoRA settings for 27B model:
- **LoRA Rank**: 32-64
- **LoRA Alpha**: 64-128
- **Target Modules**: q_proj, v_proj, k_proj, o_proj
- **Batch Size**: 1-2 (depending on VRAM)
- **Gradient Accumulation**: 8-16 steps
- **Learning Rate**: 1e-4 to 2e-4

## Hardware Requirements

- **VRAM**: 48GB+ (RTX 6000 Ada recommended)
- **RAM**: 64GB+
- **Storage**: 20-30GB for model files
- **Training Time**: 2-4 hours for 74 questions

## Testing

After fine-tuning, test with:
```bash
python 4_test_kindred_adapter.py --model gemma-3-27b-it-abliterated
```

## Model Characteristics

- **Strengths**: Large context, strong reasoning, good instruction following
- **Architecture**: Gemma (Google's Transformer variant)
- **Context Length**: 8192 tokens
- **License**: Gemma Terms of Use (commercial friendly)

## Notes

- This is a GGUF quantized version - efficient for inference
- For training, may need to convert to full precision or use QLoRA
- Abliterated version responds to all queries - use responsibly
- Fine-tuning will align it with YOUR ethics, not default safety training
