import os
import sys
import subprocess

def run_command(command, shell=True):
    """Runs a shell command and streams the output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell, text=True)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()
    process.stdout.close()
    return process.wait()

def check_gpu():
    print("=" * 60)
    print("CHECKING GPU AVAILABILITY")
    print("=" * 60)
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")
        if cuda_available:
            print(f"Device Name   : {torch.cuda.get_device_name(0)}")
            print(f"Device Count  : {torch.cuda.device_count()}")
        else:
            print("[!] GPU is not available. The system will fall back to CPU.")
    except ImportError:
        print("[!] PyTorch is not installed yet. Cannot check GPU.")
    print("=" * 60 + "\n")

def install_dependencies():
    print("=" * 60)
    print("INSTALLING DEPENDENCIES VIA UV")
    print("=" * 60)
    
    # 1. Install uv package manager if not present
    try:
        import uv
        print("[+] 'uv' is already installed.")
    except ImportError:
        print("[+] Installing 'uv' package manager...")
        run_command("pip install uv")
        
    # 2. Sync dependencies using uv. This respects the pyproject.toml / uv.lock file
    print("[+] Syncing project dependencies with uv...")
    # On Colab, we install packages directly into the active system python environment
    # rather than creating a virtualenv to make it easier to run in notebook cells.
    run_command("uv pip install --system -r pyproject.toml")
    # Also install dev dependencies for testing
    run_command("uv pip install --system pytest httpx jiwer soundfile librosa openai-whisper torch")
    
    print("[+] Installation complete!")
    print("=" * 60 + "\n")

def run_asr_evaluation(model_name="small"):
    print("=" * 60)
    print(f"RUNNING ASR EVALUATION (Model: {model_name})")
    print("=" * 60)
    
    # Configure env variables for evaluation
    os.environ["USE_MOCK_ASR"] = "False"
    os.environ["WHISPER_MODEL_NAME"] = model_name
    
    # Run the evaluate_asr.py script
    exit_code = run_command("python evaluate_asr.py")
    if exit_code == 0:
        print("[+] Evaluation completed successfully! See report at docs/asr_evaluation_report.md")
    else:
        print(f"[-] Evaluation failed with exit code: {exit_code}")
    print("=" * 60 + "\n")

def run_pytest():
    print("=" * 60)
    print("RUNNING AUTOMATED UNIT TESTS (PYTEST)")
    print("=" * 60)
    os.environ["USE_MOCK_ASR"] = "True"  # Use mock ASR for fast tests
    run_command("pytest -v")
    print("=" * 60 + "\n")

def start_server():
    print("=" * 60)
    print("STARTING FASTAPI BACKEND SERVER")
    print("=" * 60)
    print("[*] Note: To expose the server outside of Colab, run Localtunnel in a separate cell:")
    print("    !npm install -g localtunnel")
    print("    !lt --port 8000")
    print("-" * 60)
    os.environ["USE_MOCK_ASR"] = os.environ.get("USE_MOCK_ASR", "False")
    os.environ["WHISPER_MODEL_NAME"] = os.environ.get("WHISPER_MODEL_NAME", "small")
    run_command("python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
    print("=" * 60 + "\n")

def main():
    print("Google Colab Helper Script for Voice Chatbot Agent")
    print("Usage:")
    print("  python colab_run.py --install     # Install all dependencies")
    print("  python colab_run.py --evaluate    # Run Whisper ASR evaluation (defaults to 'small' model)")
    print("  python colab_run.py --eval-base   # Run evaluation with 'base' model")
    print("  python colab_run.py --eval-large  # Run evaluation with 'large-v3' model (requires GPU)")
    print("  python colab_run.py --test        # Run pytest unit tests")
    print("  python colab_run.py --server      # Start FastAPI backend server")
    print("-" * 60)
    
    if len(sys.argv) < 2:
        # Default action: check GPU and install dependencies
        check_gpu()
        install_dependencies()
        return
        
    arg = sys.argv[1]
    if arg == "--install":
        check_gpu()
        install_dependencies()
    elif arg == "--evaluate":
        run_asr_evaluation("small")
    elif arg == "--eval-base":
        run_asr_evaluation("base")
    elif arg == "--eval-large":
        run_asr_evaluation("large-v3")
    elif arg == "--test":
        run_pytest()
    elif arg == "--server":
        start_server()
    else:
        print(f"Unknown argument: {arg}")

if __name__ == "__main__":
    main()
