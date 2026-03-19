import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def parse_nvcc_release(output: str) -> str | None:
    match = re.search(r"release\s+(\d+\.\d+)", output)
    return match.group(1) if match else None


def safe_run(command: list[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(command, check=True, capture_output=True, text=True)
        return True, proc.stdout or proc.stderr
    except Exception as exc:
        return False, str(exc)


def get_xformers_status() -> dict:
    status = {
        "installed": False,
        "version": None,
        "cpp_extensions_loaded": False,
        "error": None,
    }
    try:
        import xformers  # type: ignore

        status["installed"] = True
        status["version"] = getattr(xformers, "__version__", "unknown")
        try:
            from xformers import _cpp_lib  # type: ignore

            exc = getattr(_cpp_lib, "_cpp_library_load_exception", None)
            status["cpp_extensions_loaded"] = exc is None
            status["error"] = None if exc is None else str(exc)
        except Exception as exc:
            status["error"] = repr(exc)
    except Exception as exc:
        status["error"] = repr(exc)
    return status


def main() -> int:
    try:
        import torch
        import torch.utils.cpp_extension as cpp_extension
    except Exception as exc:
        print(json.dumps({"error": f"torch import failed: {exc}"}, indent=2))
        return 1

    nvcc_path = shutil.which("nvcc")
    nvcc_output = None
    nvcc_release = None
    if nvcc_path:
        ok, output = safe_run([nvcc_path, "--version"])
        nvcc_output = output.strip()
        if ok:
            nvcc_release = parse_nvcc_release(output)

    torch_cuda = torch.version.cuda
    cuda_home = str(cpp_extension.CUDA_HOME) if cpp_extension.CUDA_HOME else None
    xformers = get_xformers_status()

    toolkit_matches_torch = None
    if torch_cuda and nvcc_release:
        toolkit_matches_torch = torch_cuda.startswith(nvcc_release)

    status = {
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "torch_cuda": torch_cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_capability": list(torch.cuda.get_device_capability(0)) if torch.cuda.is_available() else None,
        "cuda_home": cuda_home,
        "nvcc_path": nvcc_path,
        "nvcc_release": nvcc_release,
        "toolkit_matches_torch": toolkit_matches_torch,
        "xformers": xformers,
    }

    print(json.dumps(status, indent=2))

    if not torch.cuda.is_available():
        return 1
    if torch_cuda and nvcc_release and not toolkit_matches_torch:
        return 2
    if not xformers["cpp_extensions_loaded"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
