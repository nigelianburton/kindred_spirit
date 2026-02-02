# Kindred Spirit Environment Installation (Windows + RTX 6000 Pro)

## Prerequisites
- Windows 10/11
- NVIDIA RTX 6000 Pro (48GB VRAM)
- CUDA 12.8+ drivers installed (required for RTX 6000 Pro instruction set)
- Miniconda3 or Anaconda

## Quick Start (Automated)

Run the automated setup script:

```bash
cd c:/_GITN/kindred_spirit/installation-pc
setup.bat
```

This will:
1. Create the conda environment with all dependencies
2. Install PyTorch with CUDA 12.8 support
3. Verify the installation
4. Display next steps

## Manual Installation Steps

### Step 1: Create Conda Environment

The environment now includes PyTorch with CUDA 12.8 in the YAML:

```bash
cd c:/_GITN/kindred_spirit
conda env create -f installation-pc/kindred_conda.yaml
```

### Step 2: Activate Environment

```bash
conda activate kindred_conda
```

### Step 3: Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

Expected output:
```
PyTorch: 2.x.x+cu128
CUDA Available: True
CUDA Version: 12.8
GPU: NVIDIA RTX 6000 Pro
```

## Environment Details

- **Python**: 3.11.14
- **PyTorch**: 2.x.x+cu128
- **CUDA**: 12.8
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
2. Check CUDA version: Should be 12.8 or higher (required for RTX 6000 Pro)
3. Reinstall PyTorch with correct CUDA version

### Import Errors
```bash
# Reinstall problematic package
pip install --force-reinstall <package-name>
```

## Why CUDA 12.8?

- **RTX 6000 Pro**: Different instruction set requires CUDA 12.8 minimum
- **Performance**: CUDA 12.8 optimized for professional GPU architecture
- **Compatibility**: Ensures all features work with 48GB VRAM
- **Required**: Lower CUDA versions will not work properly with RTX 6000 Pro

## Quick Test

After installation, test the Qt GUI:
```bash
python 1_calibrate_kindred_spirit_qt.py
```

## Notes

- The conda yaml excludes PyTorch to avoid version conflicts
- Always install PyTorch with `--index-url` for CUDA builds
- Environment variable `KMP_DUPLICATE_LIB_OK=TRUE` prevents OpenMP conflicts
