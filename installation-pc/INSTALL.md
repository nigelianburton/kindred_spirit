# Kindred Spirit Environment Installation (Windows + RTX 6000 Ada)

## Prerequisites
- Windows 10/11
- NVIDIA RTX 6000 Ada (48GB VRAM)
- CUDA 12.6+ drivers installed
- Miniconda3 or Anaconda

## Installation Steps

### Step 1: Create Conda Environment (Without PyTorch)

```bash
cd c:/_GITN/kindred_spirit
conda env create -f installation-pc/kindred_conda.yaml
```

### Step 2: Activate Environment

```bash
conda activate kindred_conda
```

### Step 3: Install PyTorch with CUDA 12.6 Support

**CRITICAL**: This project requires PyTorch with CUDA 12.6+ for RTX 6000 Ada compatibility.

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

### Step 4: Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

Expected output:
```
PyTorch: 2.5.1+cu126
CUDA Available: True
CUDA Version: 12.6
GPU: NVIDIA RTX 6000 Ada Generation
```

### Step 5: Install Unsloth (Optional but Recommended)

For efficient LoRA training:

```bash
pip install "unsloth[cu126] @ git+https://github.com/unslothai/unsloth.git"
```

## Environment Details

- **Python**: 3.11.14
- **PyTorch**: 2.5.1+cu126
- **CUDA**: 12.6
- **Key Libraries**:
  - transformers==5.0.0
  - peft==0.18.1
  - accelerate==1.12.0
  - bitsandbytes==0.49.1
  - datasets==4.5.0
  - safetensors==0.7.0

## Troubleshooting

### CUDA Out of Memory
If you encounter OOM errors during training:
```bash
# Set environment variable
set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

### PyTorch Not Seeing GPU
1. Verify NVIDIA drivers: `nvidia-smi`
2. Check CUDA version: Should be 12.6 or higher
3. Reinstall PyTorch with correct CUDA version

### Import Errors
```bash
# Reinstall problematic package
pip install --force-reinstall <package-name>
```

## Why CUDA 12.6?

- **RTX 6000 Ada**: Requires CUDA 12.x for full feature support
- **Performance**: CUDA 12.6 optimized for Ada Lovelace architecture
- **Compatibility**: Ensures all features work with 48GB VRAM
- **Future-proof**: Latest stable CUDA release

## Quick Test

After installation, test the Qt GUI:
```bash
python 1_calibrate_kindred_spirit_qt.py
```

## Notes

- The conda yaml excludes PyTorch to avoid version conflicts
- Always install PyTorch with `--index-url` for CUDA builds
- Environment variable `KMP_DUPLICATE_LIB_OK=TRUE` prevents OpenMP conflicts
