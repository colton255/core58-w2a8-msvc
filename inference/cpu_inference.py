import os
import sys
import signal
import platform
import argparse
import subprocess
from pathlib import Path

def run_command(command, shell=False):
    """Run a system command and ensure it succeeds."""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent

def resolve_binary(name: str) -> str:
    candidates = []
    build_dir = REPO_ROOT / "build" / "bin"
    if platform.system() == "Windows":
        candidates.extend([
            build_dir / "Release" / f"{name}.exe",
            build_dir / f"{name}.exe",
        ])
    else:
        candidates.append(build_dir / name)

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    print(
        f"Unable to find {name}. Build artifacts are missing under {build_dir}. "
        f"Rebuild with `powershell -ExecutionPolicy Bypass -File .\\scripts\\smoke_test.ps1 -BuildDir build -KeepBuildDir` from the repo root."
    )
    sys.exit(1)

def resolve_model_path(model_arg: str) -> str:
    requested = Path(model_arg)
    candidates = []

    if requested.exists():
        return str(requested)

    rel_candidate = (THIS_DIR / requested).resolve()
    if rel_candidate.exists():
        return str(rel_candidate)

    if requested.name:
        matches = list((REPO_ROOT / "models" / "cpu").rglob(requested.name))
        if len(matches) == 1:
            return str(matches[0])
        candidates.extend(matches)

    print(f"Unable to find model: {model_arg}")
    if candidates:
        print("Matching candidates:")
        for candidate in candidates:
            print(f"  {candidate}")
    sys.exit(1)

def run_inference():
    main_path = resolve_binary("llama-cli")
    model_path = resolve_model_path(args.model)
    command = [
        f'{main_path}',
        '-m', model_path,
        '-n', str(args.n_predict),
        '-t', str(args.threads),
        '-p', args.prompt,
        '-ngl', '0',
        '-c', str(args.ctx_size),
        '--temp', str(args.temperature),
        "-b", "1",
    ]
    if args.conversation:
        command.append("-cnv")
    run_command(command)

def signal_handler(sig, frame):
    print("Ctrl+C pressed, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # Usage: python run_inference.py -p "Microsoft Corporation is an American multinational corporation and technology company headquartered in Redmond, Washington."
    parser = argparse.ArgumentParser(description='Run inference')
    parser.add_argument("-m", "--model", type=str, help="Path to model file", required=False, default="../models/cpu/Falcon3-10B-Instruct-1.58bit/ggml-model-i2_s.gguf")
    parser.add_argument("-n", "--n-predict", type=int, help="Number of tokens to predict when generating text", required=False, default=128)
    parser.add_argument("-p", "--prompt", type=str, help="Prompt to generate text from", required=True)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use", required=False, default=2)
    parser.add_argument("-c", "--ctx-size", type=int, help="Size of the prompt context", required=False, default=2048)
    parser.add_argument("-temp", "--temperature", type=float, help="Temperature, a hyperparameter that controls the randomness of the generated text", required=False, default=0.8)
    parser.add_argument("-cnv", "--conversation", action='store_true', help="Whether to enable chat mode or not (for instruct models.)")

    args = parser.parse_args()
    run_inference()
