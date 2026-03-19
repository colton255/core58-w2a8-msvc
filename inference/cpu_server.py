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

def run_server():
    server_path = resolve_binary("llama-server")
    model_path = resolve_model_path(args.model)
    
    command = [
        f'{server_path}',
        '-m', model_path,
        '-c', str(args.ctx_size),
        '-t', str(args.threads),
        '-n', str(args.n_predict),
        '-ngl', '0',
        '--temp', str(args.temperature),
        '--host', args.host,
        '--port', str(args.port),
    ]

    if args.continuous_batching:
        command.append('-cb')
    
    if args.prompt:
        command.extend(['-p', args.prompt])
    
    # Note: -cnv flag is removed as it's not supported by the server
    
    print(f"Starting server on {args.host}:{args.port}")
    run_command(command)

def signal_handler(sig, frame):
    print("Ctrl+C pressed, shutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description='Run llama.cpp server')
    parser.add_argument("-m", "--model", type=str, help="Path to model file", required=False, default="../models/cpu/Falcon3-10B-Instruct-1.58bit/ggml-model-i2_s.gguf")
    parser.add_argument("-p", "--prompt", type=str, help="System prompt for the model", required=False)
    parser.add_argument("-n", "--n-predict", type=int, help="Number of tokens to predict", required=False, default=4096)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use", required=False, default=2)
    parser.add_argument("-c", "--ctx-size", type=int, help="Size of the context window", required=False, default=2048)
    parser.add_argument("--temperature", type=float, help="Temperature for sampling", required=False, default=0.8)
    parser.add_argument("--host", type=str, help="IP address to listen on", required=False, default="127.0.0.1")
    parser.add_argument("--port", type=int, help="Port to listen on", required=False, default=8080)
    parser.add_argument("--continuous-batching", action="store_true", help="Enable llama-server continuous batching")
    
    args = parser.parse_args()
    run_server()
