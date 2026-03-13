# AI Eval Kit

LLM Quality Evaluation Framework - Benchmark and compare AI models.

## Live Demo

Try it now: https://ai-eval-kit-ksom5tmhijaoewgrudtvvc.streamlit.app/

## Key Metrics

| Metric | Value |
|--------|-------|
| Models Benchmarked | 4 (Llama 3.3 70B, Llama 3.1 8B, Qwen 3 32B, Llama 4 Scout) |
| Test Cases | 13 across 4 categories |
| Categories Tested | Summarization, Classification, Extraction, Reasoning |
| Cost Savings Found | 93.1% by using cheapest model |
| Quality Drop | Only 3.8% compared to best model |

## Key Insight

93.1% cost savings possible by using the cheapest model with only 3.8% quality drop compared to the best model.

## Architecture

Test Cases --> Evaluator Engine --> Multiple LLM Models --> Score Calculator --> Results Dashboard

## How It Works

1. Define test cases across 4 categories
2. Run each test case against all 4 models
3. Measure quality score, latency, and cost
4. Calculate value score (quality per dollar)
5. Display comparison charts and insights

## Features

- Multi-Model Benchmarking: Compare 4 models simultaneously
- Quality Scoring: Evaluate output accuracy
- Latency Tracking: Measure response times
- Cost Analysis: Calculate cost per request
- Value Score: Quality-to-cost ratio
- Interactive Dashboard: Visual comparison charts

## Model Comparison Results

| Model | Quality Score | Avg Latency | Total Cost | Value Score |
|-------|--------------|-------------|------------|-------------|
| Qwen 3 32B | 57.7% | 833ms | $0.001491 | 38.69 |
| Llama 3.3 70B | 53.9% | 564ms | $0.001145 | 47.03 |
| Llama 3.1 8B | 53.9% | 494ms | $0.000103 | 522.82 |
| Llama 4 Scout 17B | 53.1% | 463ms | $0.000526 | 100.91 |

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastAPI | API Framework |
| Groq | LLM Provider |
| Streamlit | Dashboard |
| Pandas | Data Analysis |

## Quick Start

1. Clone: git clone https://github.com/santhosh123-vs/ai-eval-kit
2. Install: pip install -r requirements.txt
3. Add .env with GROQ_API_KEY
4. Run API: python main.py
5. Run Dashboard: streamlit run dashboard.py

## Author

Kethavath Santhosh - github.com/santhosh123-vs
