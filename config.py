import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

MODELS = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B",
        "cost_per_1k": {"input": 0.00059, "output": 0.00079},
        "category": "large"
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B",
        "cost_per_1k": {"input": 0.00005, "output": 0.00008},
        "category": "small"
    },
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "name": "Llama 4 Scout 17B",
        "cost_per_1k": {"input": 0.00020, "output": 0.00060},
        "category": "medium"
    },
    "qwen/qwen3-32b": {
        "name": "Qwen 3 32B",
        "cost_per_1k": {"input": 0.00020, "output": 0.00040},
        "category": "medium"
    }
}
