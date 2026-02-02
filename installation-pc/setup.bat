@echo off
REM ============================================================================
REM Kindred Spirit - Automated Environment Setup
REM Windows + NVIDIA RTX 6000 Pro (CUDA 12.8)
REM ============================================================================

echo.
echo ========================================
echo Kindred Spirit Environment Setup
echo ========================================
echo.

REM Check if conda is available
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda not found in PATH
    echo Please install Miniconda or Anaconda first
    echo https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

REM Store the current directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo Step 1: Creating conda environment from YAML...
echo.
conda env create -f "%SCRIPT_DIR%kindred_conda.yaml"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to create conda environment
    echo.
    echo If the environment already exists, remove it first:
    echo   conda env remove -n kindred_conda
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Installing PyTorch with CUDA 12.8...
echo ========================================
echo.

REM Activate environment and install PyTorch
call conda activate kindred_conda
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate kindred_conda environment
    pause
    exit /b 1
)

pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu128
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install PyTorch
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 3: Verifying Installation...
echo ========================================
echo.

python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Installation verification failed
    echo Please check your NVIDIA drivers and CUDA installation
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Environment: kindred_conda
echo.
echo To activate the environment:
echo   conda activate kindred_conda
echo.
echo To test the calibration GUI:
echo   python 1_calibrate_kindred_spirit_qt.py
echo.
echo To begin the 5-stage workflow:
echo   1. python 1_calibrate_kindred_spirit.py
echo   2. python 2_generate_training_data.py
echo   3. python 3_train_kindred_values.py
echo   4. python 4_test_kindred_adapter.py
echo   5. python 5_convert_to_gguf.py
echo.
pause
