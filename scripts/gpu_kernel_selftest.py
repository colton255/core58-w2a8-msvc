import ctypes
import sys
from pathlib import Path

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
UTILS_GPU_DIR = REPO_ROOT / "utils" / "gpu"
if str(UTILS_GPU_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_GPU_DIR))

from pack_weight import convert_weight_int8_to_int2


def bitnet_int8xint2_linear(lib, input0, input1, s, ws, ret):
    stream = torch.cuda.current_stream()
    m = input0.shape[0]
    n = input1.shape[0]
    k = input1.shape[1] * 4

    lib.bitlinear_int8xint2(
        ctypes.c_void_p(input0.data_ptr()),
        ctypes.c_void_p(input1.data_ptr()),
        ctypes.c_void_p(ret.data_ptr()),
        ctypes.c_void_p(s.data_ptr()),
        ctypes.c_void_p(ws.data_ptr()),
        ctypes.c_int(m),
        ctypes.c_int(n),
        ctypes.c_int(k),
        ctypes.c_void_p(stream.cuda_stream),
    )
    return ret


def run_case(lib, n, k, ws_size):
    weight = torch.randint(-1, 2, (n, k), dtype=torch.int8, device="cuda")
    weight_compressed = convert_weight_int8_to_int2(weight).to("cuda")

    input0 = torch.randint(-128, 127, (1, k), dtype=torch.int8, device="cuda")
    input_np = input0.cpu().to(torch.int32).numpy()
    weight_np = weight.cpu().to(torch.int32).T.numpy()
    out_np = torch.tensor(np.matmul(input_np, weight_np), device="cuda", dtype=torch.bfloat16)

    s = torch.ones(1, dtype=torch.bfloat16, device="cuda")
    ws = torch.ones(ws_size, dtype=torch.bfloat16, device="cuda")
    ret = torch.empty((1, n), dtype=torch.bfloat16, device="cuda")
    out = bitnet_int8xint2_linear(lib, input0, weight_compressed, s, ws, ret)
    torch.cuda.synchronize()

    equal = bool(torch.all(out == out_np))
    max_abs = (out.float() - out_np.float()).abs().max().item()
    return equal, max_abs


def main():
    if not torch.cuda.is_available():
        print("CUDA is not available.")
        sys.exit(1)

    torch.cuda.set_device(0)
    dll_path = REPO_ROOT / "src" / "cuda" / "bitnet_kernels" / "libbitnet.dll"
    if not dll_path.exists():
        print(f"Missing kernel DLL: {dll_path}")
        sys.exit(1)

    lib = ctypes.CDLL(str(dll_path), winmode=0)
    cases = [
        (2560, 2560, 1),
        (3840, 2560, 3),
        (13824, 2560, 2),
        (2560, 6912, 1),
    ]

    failures = 0
    for n, k, ws_size in cases:
        equal, max_abs = run_case(lib, n, k, ws_size)
        status = "PASS" if equal else "FAIL"
        print(f"{status} N={n} K={k} max_abs={max_abs:.1f}")
        if not equal:
            failures += 1

    if failures:
        print(f"Kernel self-test failed: {failures} case(s) mismatched.")
        sys.exit(1)

    print("Kernel self-test passed.")


if __name__ == "__main__":
    main()
