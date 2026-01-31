"""
Auto-fix wrapper for training - handles common errors and retries
"""
import os
import sys
import subprocess
import time
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

MAX_RETRIES = 5
LOG_FILE = "training_log_auto.txt"
STATUS_FILE = "training_status_auto.json"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def check_and_fix_errors(log_content, attempt):
    """Analyze errors and apply fixes"""
    fixes_applied = []
    
    # CUDA OOM
    if "CUDA out of memory" in log_content or "OutOfMemoryError" in log_content:
        log("FIX: CUDA OOM - Reducing batch size")
        try:
            with open("train_nigel_values.py", "r") as f:
                content = f.read()
            
            # Reduce batch size progressively
            new_batch = max(2, 8 // (attempt + 1))
            content = content.replace('"batch_size": 8', f'"batch_size": {new_batch}')
            
            with open("train_nigel_values.py", "w") as f:
                f.write(content)
            
            fixes_applied.append(f"batch_size -> {new_batch}")
        except Exception as e:
            log(f"Failed to apply OOM fix: {e}")
    
    # Network errors
    if "Connection" in log_content or "TimeoutError" in log_content:
        log("FIX: Network issue - Waiting before retry")
        time.sleep(30)
        fixes_applied.append("network_wait_30s")
    
    # Missing dependencies
    if "ImportError" in log_content or "ModuleNotFoundError" in log_content:
        log("FIX: Missing dependency - Installing")
        try:
            python_exe = Path.home() / "miniconda3" / "envs" / "train_for_nigel" / "python.exe"
            pip_exe = Path.home() / "miniconda3" / "envs" / "train_for_nigel" / "Scripts" / "pip.exe"
            subprocess.run([
                str(pip_exe), "install", "-q", "--upgrade",
                "transformers", "peft", "datasets", "accelerate", "bitsandbytes"
            ], check=True)
            fixes_applied.append("reinstalled_deps")
        except:
            pass
    
    # Corrupt cache
    if "safetensors" in log_content and ("corrupt" in log_content or "invalid" in log_content):
        log("FIX: Corrupt download - Clearing cache")
        cache_path = Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen2.5-7B-Instruct"
        if cache_path.exists():
            import shutil
            shutil.rmtree(cache_path)
            fixes_applied.append("cleared_cache")
    
    return fixes_applied

def run_training():
    """Run training with auto-recovery"""
    log(">> Auto-Recovery Training Started")
    log("=" * 50)
    
    for attempt in range(MAX_RETRIES):
        log(f">> Attempt {attempt + 1}/{MAX_RETRIES}")
        
        # Run training
        try:
            # Use direct python from the environment
            python_exe = Path.home() / "miniconda3" / "envs" / "train_for_nigel" / "python.exe"
            if not python_exe.exists():
                python_exe = "python"  # Fallback
            
            result = subprocess.run(
                [str(python_exe), "train_nigel_values.py"],
                capture_output=True,
                text=True,
                timeout=4 * 3600,  # 4 hour timeout
                cwd=Path(__file__).parent
            )
            
            # Save logs
            full_log = result.stdout + "\n" + result.stderr
            with open(LOG_FILE, "w") as f:
                f.write(full_log)
            
            # Save status
            status = {
                "attempt": attempt + 1,
                "exit_code": result.returncode,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(STATUS_FILE, "w") as f:
                json.dump(status, f, indent=2)
            
            # Check result
            if result.returncode == 0:
                log("SUCCESS: Training completed successfully!")
                log(f"SUCCESS: Adapter saved to: ./nigel_lora_adapter/")
                
                # Show summary
                log("\nFinal Training Summary:")
                for line in full_log.split("\n")[-20:]:
                    if any(kw in line.lower() for kw in ["loss", "epoch", "saved", "complete"]):
                        print(line)
                
                return True
            
            else:
                log(f"WARNING: Training failed with exit code {result.returncode}")
                log("\nLast 20 lines of log:")
                for line in full_log.split("\n")[-20:]:
                    print(line)
                
                # Try to fix
                fixes = check_and_fix_errors(full_log, attempt)
                if fixes:
                    log(f"FIXES APPLIED: {', '.join(fixes)}")
                
                if attempt < MAX_RETRIES - 1:
                    log("Retrying in 60 seconds...")
                    time.sleep(60)
        
        except subprocess.TimeoutExpired:
            log("TIMEOUT: Training timeout (4 hours) - likely hung")
            if attempt < MAX_RETRIES - 1:
                log("Retrying...")
                time.sleep(30)
        
        except Exception as e:
            log(f"ERROR: Unexpected error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(60)
    
    log(f"\nFAILED: Training failed after {MAX_RETRIES} attempts")
    log(f"Check log: {LOG_FILE}")
    return False

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    success = run_training()
    sys.exit(0 if success else 1)
