# 🧪 AI Eval Kit

**LLM Quality Evaluation Framework** - Benchmark and compare AI models on quality, latency, and cost.

## 🎯 Features

- Multi-Model Benchmarking - Compare 4+ LLM models simultaneously
- Quality Scoring - Evaluate summarization, classification, extraction, reasoning
- Latency Tracking - Measure response times per model
- Cost Analysis - Calculate cost per request and total costs
- Value Score - Quality-to-cost ratio for optimal model selection
- Interactive Dashboard - Visual charts and comparison tables
- REST API - Programmatic access to all evaluation features

## 🚀 Quick Start

1. Clone the repo
2. Create virtual environment: python -m venv venv
3. Activate: source venv/bin/activate
4. Install: pip install -r requirements.txt
5. Add .env file with GROQ_API_KEY
6. Run API: uvicorn main:app --port 8002
7. Run Dashboard: streamlit run dashboard.py

## 📡 API Endpoints

- GET / - Health check
- GET /models - List available models
- POST /evaluate - Run single model evaluation
- POST /benchmark - Benchmark all models

## 🛠 Tech Stack

Python, FastAPI, Streamlit, Groq API

## 👨‍💻 Author

Kethavath Santhosh - github.com/santhosh123-vs
