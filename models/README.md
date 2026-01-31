# Kindred Spirit - Model Testing Suite

This directory contains four abliterated models for comparative testing with the Kindred Spirit personal ethics fine-tuning system.

## Models Overview

| Model | Size | Format | Context | Special Feature |
|-------|------|--------|---------|----------------|
| **Gemma 3 27B Instruct** | 27B | GGUF | 8K | Google's latest, strong reasoning |
| **Huihui Qwen3 Coder 30B** | 30B | GGUF | 32K | Code-focused, long context |
| **Qwen3 VL 8B Instruct** | 8B | GGUF | 8K | Vision-language, multimodal |
| **Huihui GPT OSS 20B** | 20B | BF16 | 8K | GPT architecture, BF16 precision |

## Why These Models?

### 1. Size Comparison (8B → 20B → 27B → 30B)
- Test if larger models better capture ethical nuance
- Find the sweet spot between quality and efficiency
- Understand minimum viable size for personal ethics

### 2. Architecture Diversity
- **Gemma**: Google's architecture
- **Qwen**: Alibaba's multilingual design
- **GPT**: Proven decoder-only architecture
- Ensures results generalize across architectures

### 3. Format Testing
- **GGUF**: Efficient quantized inference
- **BF16**: Full precision for training
- Compare training results across formats

### 4. Unique Capabilities
- **Vision** (Qwen3-VL): Multimodal ethics
- **Code** (Qwen3-Coder): Technical + ethical reasoning
- **Long Context** (Qwen3-Coder 32K): Extended conversations

## Abliteration Status

All models have been **abliterated** - refusal behaviors removed via orthogonalization:
- ✓ No more "I cannot assist with that" responses
- ✓ Maintains knowledge and capabilities
- ✓ Ready for personal ethics alignment
- ✓ Responds based on values, not corporate safety

## Directory Structure

```
models/
├── README.md (this file)
├── MODEL_COMPARISON.md (detailed comparison)
├── gemma-3-27b-it-abliterated/
│   ├── README.md
│   └── (download model files here)
├── Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated/
│   ├── README.md
│   └── (download model files here)
├── Qwen3-VL-8B-Instruct-abliterated-v2.0/
│   ├── README.md
│   └── (download model files here)
└── Huihui-gpt-oss-20b-BF16-abliterated-v2/
    ├── README.md
    └── (download model files here)
```

## Quick Start

### 1. Download Models

Each model directory contains a README with download instructions. Choose one:

```bash
# Option 1: Download all models (requires ~100GB+ storage)
cd models/gemma-3-27b-it-abliterated && huggingface-cli download mlabonne/gemma-3-27b-it-abliterated-GGUF --local-dir . && cd ../..
cd models/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated && huggingface-cli download mradermacher/Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated-i1-GGUF --local-dir . && cd ../..
cd models/Qwen3-VL-8B-Instruct-abliterated-v2.0 && huggingface-cli download mradermacher/Qwen3-VL-8B-Instruct-abliterated-v2.0-GGUF --local-dir . && cd ../..
cd models/Huihui-gpt-oss-20b-BF16-abliterated-v2 && huggingface-cli download huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated-v2l --local-dir . && cd ../..

# Option 2: Start with one model (recommended: Gemma 3 27B)
cd models/gemma-3-27b-it-abliterated
huggingface-cli download mlabonne/gemma-3-27b-it-abliterated-GGUF --local-dir . --local-dir-use-symlinks False
```

### 2. Complete Calibration

Run the Qt GUI to capture your values:
```bash
python 1_calibrate_kindred_spirit_qt.py
```

### 3. Generate Training Data

```bash
python 2_generate_training_data.py --username your_name
```

### 4. Fine-Tune Each Model

```bash
# Fine-tune Gemma
python 3_train_kindred_values.py --model gemma-3-27b-it-abliterated --username your_name

# Fine-tune Qwen3 Coder
python 3_train_kindred_values.py --model Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated --username your_name

# Fine-tune Qwen3 VL
python 3_train_kindred_values.py --model Qwen3-VL-8B-Instruct-abliterated-v2.0 --username your_name

# Fine-tune Huihui GPT
python 3_train_kindred_values.py --model Huihui-gpt-oss-20b-BF16-abliterated-v2 --username your_name
```

### 5. Test Each Model

```bash
# Test Gemma
python 4_test_kindred_adapter.py --model gemma-3-27b-it-abliterated

# Test Qwen3 Coder
python 4_test_kindred_adapter.py --model Huihui-Qwen3-Coder-30B-A3B-Instruct-abliterated

# Test Qwen3 VL
python 4_test_kindred_adapter.py --model Qwen3-VL-8B-Instruct-abliterated-v2.0

# Test Huihui GPT
python 4_test_kindred_adapter.py --model Huihui-gpt-oss-20b-BF16-abliterated-v2
```

## Expected Results

After fine-tuning, each model will:
- Respond according to YOUR ethical framework
- Show consistency with your calibration responses
- Maintain capabilities while following your values
- Demonstrate differences based on size/architecture

## Hardware Requirements

### Minimum (for 8B model)
- VRAM: 24GB (RTX 3090/4090)
- RAM: 32GB
- Storage: 50GB

### Recommended (for all models)
- VRAM: 48GB (RTX 6000 Ada)
- RAM: 64GB
- Storage: 150GB

### Optimal (for parallel testing)
- VRAM: 96GB (2x RTX 6000 Ada)
- RAM: 128GB
- Storage: 200GB

## Comparison Metrics

After testing all models, compare:
1. **Ethical Alignment**: How well does each follow your values?
2. **Consistency**: Does it give similar answers to similar questions?
3. **Reasoning Quality**: Can it explain its ethical positions?
4. **Speed**: Inference time for responses
5. **Memory**: VRAM usage during inference
6. **Training Time**: How long to fine-tune

## License Information

All models use permissive licenses:
- **Gemma 3**: Gemma Terms of Use (commercial friendly)
- **Qwen3**: Apache 2.0 (fully open source)
- **Huihui GPT**: Fully open source

## Next Steps

1. Download your first model (start with Gemma 3 27B)
2. Complete the calibration via Qt GUI
3. Generate training data
4. Fine-tune and test
5. Repeat for other models
6. Compare results and choose your preferred model

## Support

For issues or questions:
- Check individual model READMEs
- See main project README.md
- Review LLM_PersonalEthics.md for philosophy

---

*Testing multiple models ensures your personal ethics system generalizes across architectures and isn't tied to one specific model's quirks.*
