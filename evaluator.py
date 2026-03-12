import time
from groq import Groq
from config import GROQ_API_KEY, MODELS
from test_cases import get_all_test_cases, get_categories

client = Groq(api_key=GROQ_API_KEY)

benchmark_history = []


def calculate_cost(model, input_tokens, output_tokens):
    costs = MODELS[model]["cost_per_1k"]
    return round((input_tokens / 1000) * costs["input"] + (output_tokens / 1000) * costs["output"], 6)


def run_single_eval(model, task, input_text, temperature=0.3):
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Answer accurately and concisely."},
                {"role": "user", "content": f"{task}\n\nText: {input_text}"}
            ],
            max_tokens=500,
            temperature=temperature
        )
        latency_ms = (time.time() - start) * 1000
        output = response.choices[0].message.content
        tokens = {
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        }
        cost = calculate_cost(model, tokens["input"], tokens["output"])
        return {
            "success": True,
            "output": output,
            "tokens": tokens,
            "cost_usd": cost,
            "latency_ms": round(latency_ms, 2)
        }
    except Exception as e:
        return {
            "success": False,
            "output": str(e),
            "tokens": {"input": 0, "output": 0, "total": 0},
            "cost_usd": 0,
            "latency_ms": 0
        }


def score_output(output, expected_keywords=None, expected_answer=None):
    score = 0
    details = []
    if not output:
        return 0, ["Empty output"]
    output_lower = output.lower().strip()

    if expected_keywords:
        found = 0
        for keyword in expected_keywords:
            if keyword.lower() in output_lower:
                found += 1
        keyword_score = (found / len(expected_keywords)) * 100
        score += keyword_score * 0.6
        details.append(f"Keywords: {found}/{len(expected_keywords)} ({keyword_score:.0f}%)")

    if expected_answer:
        if expected_answer.lower() in output_lower:
            score += 40
            details.append("Correct answer: YES")
        else:
            details.append(f"Correct answer: NO (expected '{expected_answer}')")

    word_count = len(output.split())
    if 10 <= word_count <= 500:
        score += 10
        details.append(f"Length: Good ({word_count} words)")
    elif word_count < 10:
        details.append(f"Length: Too short ({word_count} words)")
    else:
        score += 5
        details.append(f"Length: Verbose ({word_count} words)")

    if not expected_keywords and not expected_answer:
        score = 70 if word_count > 10 else 30

    return min(round(score, 2), 100), details


def evaluate_model(model, test_cases=None):
    if test_cases is None:
        test_cases = get_all_test_cases()
    results = []
    total_cost = 0
    total_latency = 0
    total_score = 0

    for case in test_cases:
        print(f"  Testing {model} on {case['id']}...")
        result = run_single_eval(model, case["task"], case["input"])
        quality_score, score_details = score_output(
            result["output"],
            case.get("expected_keywords"),
            case.get("expected_answer")
        )
        eval_result = {
            "test_id": case["id"],
            "category": case.get("category", "unknown"),
            "model": model,
            "model_name": MODELS[model]["name"],
            "output": result["output"],
            "quality_score": quality_score,
            "score_details": score_details,
            "tokens": result["tokens"],
            "cost_usd": result["cost_usd"],
            "latency_ms": result["latency_ms"],
            "success": result["success"]
        }
        results.append(eval_result)
        total_cost += result["cost_usd"]
        total_latency += result["latency_ms"]
        total_score += quality_score
        time.sleep(0.5)

    avg_score = total_score / len(test_cases) if test_cases else 0
    avg_latency = total_latency / len(test_cases) if test_cases else 0

    return {
        "model": model,
        "model_name": MODELS[model]["name"],
        "category": MODELS[model]["category"],
        "total_tests": len(test_cases),
        "average_score": round(avg_score, 2),
        "total_cost_usd": round(total_cost, 6),
        "average_latency_ms": round(avg_latency, 2),
        "results": results
    }


def benchmark_all_models(test_cases=None):
    if test_cases is None:
        test_cases = get_all_test_cases()
    print(f"\nBenchmarking {len(MODELS)} models on {len(test_cases)} tests...\n")
    all_results = []

    for model in MODELS:
        print(f"\n[Model] {MODELS[model]['name']}")
        result = evaluate_model(model, test_cases)
        all_results.append(result)
        print(f"  Score: {result['average_score']:.1f}% | Cost: ${result['total_cost_usd']:.6f} | Latency: {result['average_latency_ms']:.0f}ms")

    all_results.sort(key=lambda x: x["average_score"], reverse=True)

    for r in all_results:
        if r["total_cost_usd"] > 0:
            r["score_per_dollar"] = round(r["average_score"] / (r["total_cost_usd"] * 1000), 2)
        else:
            r["score_per_dollar"] = 0

    if len(all_results) >= 2:
        best = all_results[0]
        cheapest = min(all_results, key=lambda x: x["total_cost_usd"])
        if best["total_cost_usd"] > 0:
            cost_savings = round((1 - cheapest["total_cost_usd"] / best["total_cost_usd"]) * 100, 1)
            quality_drop = round(best["average_score"] - cheapest["average_score"], 1)
        else:
            cost_savings = 0
            quality_drop = 0
    else:
        cost_savings = 0
        quality_drop = 0

    summary = {
        "total_models": len(all_results),
        "total_test_cases": len(test_cases),
        "results": all_results,
        "best_quality": all_results[0]["model_name"] if all_results else "",
        "cheapest": min(all_results, key=lambda x: x["total_cost_usd"])["model_name"] if all_results else "",
        "fastest": min(all_results, key=lambda x: x["average_latency_ms"])["model_name"] if all_results else "",
        "cost_savings": f"{cost_savings}%",
        "quality_drop": f"{quality_drop}%"
    }

    benchmark_history.append(summary)
    return summary
