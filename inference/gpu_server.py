import os
import sys
import time
import uuid
from pathlib import Path
from typing import List, Optional

try:
    import torch
except ImportError:
    print("Missing dependency 'torch'. Activate your repo GPU venv or run `pip install -r requirements.txt` before using gpu_server.py.")
    sys.exit(1)

try:
    import uvicorn
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:
    print("Missing GPU server dependencies. Activate your repo GPU venv or run `pip install -r requirements.txt` before using gpu_server.py.")
    sys.exit(1)

try:
    from gpu_generate import FastGen, GenArgs
    from tokenizer import ChatFormat
except ImportError:
    from .gpu_generate import FastGen, GenArgs
    from .tokenizer import ChatFormat

app = FastAPI()

# Global config
THIS_DIR = Path(__file__).resolve().parent
DEFAULT_CKPT_DIR = THIS_DIR.parent / "models" / "gpu" / "bitnet-b1.58-2B-4T-bf16"
CKPT_DIR = os.getenv("BITNET_CKPT_DIR", str(DEFAULT_CKPT_DIR if DEFAULT_CKPT_DIR.exists() else (THIS_DIR / "checkpoints")))
DEVICE = os.getenv("BITNET_DEVICE", "cuda:0")
DECODE_BACKEND = os.getenv("BITNET_DECODE_BACKEND", "int2")

g = None

@app.on_event("startup")
def load_model():
    global g
    print(f"Loading model on {DEVICE} from {CKPT_DIR} using {DECODE_BACKEND} decode")
    torch.cuda.set_device(DEVICE)
    g = FastGen.build(CKPT_DIR, GenArgs(), DEVICE, decode_backend=DECODE_BACKEND)
    # Wrap tokenizer in ChatFormat for chat/completions
    g.tokenizer = ChatFormat(g.tokenizer)
    print("Model loaded and ready for inference.")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "bitnet"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    max_tokens: Optional[int] = 512
    stream: Optional[bool] = False

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    global g
    
    # We only process batch size 1 natively for now based on generator constraints
    dialog = [{"role": m.role, "content": m.content} for m in req.messages]
    
    # Tokenize prompt using the ChatFormat structure
    tokens = [g.tokenizer.encode_dialog_prompt(dialog=dialog, completion=True)]
    
    # Run the BitNet generator
    stats, out_tokens = g.generate_all(
        tokens,
        use_cuda_graphs="NO_CUDA_GRAPHS" not in os.environ,
        use_sampling=(req.temperature > 0.0)
    )
    
    # Decode the result (batch index 0)
    answer = g.tokenizer.decode(out_tokens[0])
    
    # Build OpenAI compatible response
    resp = {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(tokens[0]),
            "completion_tokens": len(out_tokens[0]),
            "total_tokens": len(tokens[0]) + len(out_tokens[0])
        }
    }
    return resp

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
