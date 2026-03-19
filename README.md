# core58-w2a8-msvc

A minimal Windows-native inference framework for 1.58-bit ternary LLMs (BitNet).

The implementation focuses on a dense `W2A8` (Weight 2-bit, Activation 8-bit) execution path that bypasses PyTorch's native `BF16` bottlenecks on Windows. The CPU route is automated around `llama.cpp`/GGUF, while the GPU route stays as a separate Windows-native experimental path built around PyTorch, CUDA graphs, and a custom DLL.

## Features
- **Automated CPU Build Pipeline:** The `setup_env.py` script manages HuggingFace weights, generates the selected CPU kernels, and compiles the `llama-cli`, `llama-server`, and quantization binaries via CMake.
- **Universal CUDA Support (Fatbin):** The GPU kernel natively targets Ampere (`sm_80`, `sm_86`), Lovelace (`sm_89`), and Hopper (`sm_90`) simultaneously without requiring manual reconfiguration.
- **PyTorch CUDAGraphs + FFI Integration:** Python execution relies on PyTorch `CUDAGraphs` to statically allocate memory arrays in VRAM, routing execution directly into the unrolled C++ NVCC kernel via `ctypes` FFI to minimize kernel-launch overhead.

## Installation

Ensure you have Python 3.8+, Git, and Visual Studio C++ build tools installed with the LLVM/Clang toolchain enabled. For GPU builds, install the CUDA toolkit so `nvcc` is available on `PATH`.
This repository does not ship model weights or prepared GPU checkpoints.

```bash
git clone https://github.com/syn-999/core58-w2a8-msvc.git
cd core58-w2a8-msvc
git submodule update --init --recursive

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Setup & Compilation

The environment script automates the CPU download, conversion, and native compilation process.
The CPU path is the primary automated flow. The GPU path remains a separate Windows-native experimental route on purpose and is not folded into `setup_env.py`.

**For CPU Inference (default `i2_s` GGUF):**
```bash
python setup_env.py --hf-repo tiiuae/Falcon3-10B-Instruct-1.58bit
```

**For CPU Inference (`tl2` on x86_64):**
```bash
python setup_env.py --hf-repo tiiuae/Falcon3-10B-Instruct-1.58bit --quant-type tl2
```

**For GPU Inference (CUDA):**
The GPU runtime does not ship checkpoints or compiled CUDA binaries. Prepare a checkpoint directory that contains `model_state_fp16.pt` and `model_state_int2.pt`, then build `src/cuda/bitnet_kernels/libbitnet.dll` locally with `src/cuda/bitnet_kernels/compile.bat`.
The examples below assume you place those artifacts under `models/gpu/bitnet-b1.58-2B-4T-bf16`.

## Inference

**CPU Execution:**
Routes directly via the C++ `llama-cli.exe` engine.
```bash
cd inference
python cpu_inference.py -m ../models/cpu/Falcon3-10B-Instruct-1.58bit/ggml-model-i2_s.gguf -p "A complete structural breakdown of a cell is" -n 200
```

**GPU Execution:**
Routes via the native PyTorch/NVCC wrapper.
```bash
cd inference
python gpu_generate.py ../models/gpu/bitnet-b1.58-2B-4T-bf16 --interactive
```

**Preparing a New GPU Checkpoint:**
```bash
python utils/gpu/convert_safetensors.py --safetensors_file models/gpu/bitnet-b1.58-2B-4T-bf16/model.safetensors --output models/gpu/bitnet-b1.58-2B-4T-bf16/model_state.pt --model_name 2B
python utils/gpu/convert_checkpoint.py --input models/gpu/bitnet-b1.58-2B-4T-bf16/model_state.pt
cd src/cuda/bitnet_kernels
.\compile.bat
```

## Smoke Test

For a quick Windows release check:

```powershell
.\scripts\smoke_test.ps1
```

To also verify the local CUDA helper build:

```powershell
.\scripts\smoke_test.ps1 -CheckGpu
```
