from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from evaluator import evaluate_model, benchmark_all_models, run_single_eval, score_output, benchmark_history
from test_cases import get_all_test_cases, get_categories, TEST_CASES
from config import MODELS


app = FastAPI(
    title="AI Eval Kit - LLM Quality Evaluator",
    description="Benchmark AI models across quality, latency, and cost. Built by Kethavath Santhosh",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EvalRequest(BaseModel):
    model: str = "llama-3.3-70b-versatile"
    task: str = "Summarize this text"
    input_text: str = "AI is transforming the world"


@app.get("/")
def home():
    return {
        "name": "AI Eval Kit - LLM Quality Evaluator",
        "version": "1.0.0",
        "models": list(MODELS.keys()),
        "test_categories": get_categories(),
        "total_test_cases": len(get_all_test_cases())
    }


@app.post("/api/v1/eval")
def evaluate_single(request: EvalRequest):
    result = run_single_eval(request.model, request.task, request.input_text)
    score, details = score_output(result["output"])
    result["quality_score"] = score
    result["score_details"] = details
    result["model_name"] = MODELS.get(request.model, {}).get("name", request.model)
    return result


@app.get("/api/v1/benchmark")
def run_benchmark(category: Optional[str] = None):
    if category and category in TEST_CASES:
        test_cases = [dict(c, category=category) for c in TEST_CASES[category]]
    else:
        test_cases = get_all_test_cases()
    return benchmark_all_models(test_cases)


@app.get("/api/v1/models")
def list_models():
    return MODELS


@app.get("/api/v1/tests")
def list_tests():
    return {"categories": get_categories(), "total": len(get_all_test_cases()), "tests": TEST_CASES}


@app.get("/api/v1/history")
def get_history():
    return {"total": len(benchmark_history), "benchmarks": benchmark_history}
