# GGUF Model Sources

This file tracks GGUF-only models where full PyTorch versions are not available.

## Qwen3-VL-8B-Instruct-abliterated-v2.0

**Status**: Only available in GGUF format (no original PyTorch weights)

**Source Repository**: [mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF](https://huggingface.co/mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF)

### Required Files

#### F16 Model (Full Precision)
- **File**: `Qwen3-VL-8B-Instruct-abliterated-v2.0.f16.gguf`
- **URL**: https://huggingface.co/mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF/blob/main/Qwen3-VL-8B-Instruct-abliterated-v2.0.f16.gguf
- **Size**: ~15-16 GB
- **Purpose**: Base model for conversion to PyTorch format

#### Vision Projector (Multimodal)
- **File**: `Qwen3-VL-8B-Instruct-abliterated-v2.0.mmproj-f16.gguf`
- **URL**: https://huggingface.co/mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF/blob/main/Qwen3-VL-8B-Instruct-abliterated-v2.0.mmproj-f16.gguf
- **Size**: ~1-2 GB
- **Purpose**: Vision encoder for processing images

### Download Instructions

```bash
# Create GGUF models directory
mkdir -p models-gguf/Qwen3-VL-8B-Instruct-abliterated-v2.0
cd models-gguf/Qwen3-VL-8B-Instruct-abliterated-v2.0

# Download F16 model
huggingface-cli download mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF \
  Qwen3-VL-8B-Instruct-abliterated-v2.0.f16.gguf \
  --local-dir . \
  --local-dir-use-symlinks False

# Download vision projector
huggingface-cli download mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF \
  Qwen3-VL-8B-Instruct-abliterated-v2.0.mmproj-f16.gguf \
  --local-dir . \
  --local-dir-use-symlinks False
```

### Conversion to PyTorch

To fine-tune, convert F16 GGUF to HuggingFace format:

```bash
# Using llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

python convert-gguf-to-hf.py \
  --input ../models-gguf/Qwen3-VL-8B-Instruct-abliterated-v2.0/Qwen3-VL-8B-Instruct-abliterated-v2.0.f16.gguf \
  --output ../models-gguf/Qwen3-VL-8B-Instruct-abliterated-v2.0/hf_model \
  --outtype f16
```

### Notes

- F16 GGUF is functionally equivalent to full precision for fine-tuning
- Vision projector (mmproj) required for multimodal inference
- Text-only fine-tuning doesn't require mmproj
- After conversion, use standard LoRA training pipeline
- Keep GGUF files for efficient inference after training

---

## Storage Location

GGUF models stored in: `models-gguf/` (excluded from Git)
Converted models stored in: `models-gguf/<model-name>/hf_model/`
