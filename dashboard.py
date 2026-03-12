import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AI Eval Kit",
    page_icon="\U0001f9ea",
    layout="wide"
)

API_URL = "https://ai-eval-kit.onrender.com"

st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0;}
    .sub-header {font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem;}
    .winner-box {background: linear-gradient(135deg, #FFD700, #FFA500); padding: 1rem; border-radius: 1rem; text-align: center; color: white; font-weight: 700;}
</style>
""", unsafe_allow_html=True)


def get_models():
    try:
        return requests.get(f"{API_URL}/api/v1/models", timeout=10).json()
    except:
        return None

def get_tests():
    try:
        return requests.get(f"{API_URL}/api/v1/tests", timeout=10).json()
    except:
        return None

def run_benchmark(category=None):
    try:
        url = f"{API_URL}/api/v1/benchmark"
        if category:
            url += f"?category={category}"
        return requests.get(url, timeout=300).json()
    except Exception as e:
        return {"error": str(e)}

def run_single_eval(model, task, input_text):
    try:
        return requests.post(f"{API_URL}/api/v1/eval", json={
            "model": model,
            "task": task,
            "input_text": input_text
        }, timeout=60).json()
    except Exception as e:
        return {"error": str(e)}


with st.sidebar:
    st.markdown("## \U0001f9ea AI Eval Kit")
    st.markdown("LLM Quality Evaluator")
    st.markdown("---")
    page = st.radio("Navigate", [
        "\U0001f3c6 Benchmark",
        "\U0001f9ea Single Test",
        "\U0001f4ca Results",
        "\U0001f916 Models Info"
    ])
    st.markdown("---")
    st.markdown("**Built by Kethavath Santhosh**")
    st.markdown("[GitHub](https://github.com/santhosh123-vs)")


if page == "\U0001f3c6 Benchmark":
    st.markdown('<p class="main-header">\U0001f3c6 LLM Benchmark</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compare AI models on quality, speed, and cost</p>', unsafe_allow_html=True)

    tests = get_tests()
    categories = ["all"] + (tests.get("categories", []) if tests else [])
    
    selected_cat = st.selectbox("Test Category", categories)
    
    st.info(f"This will test all models on {'all' if selected_cat == 'all' else selected_cat} test cases. Takes 2-3 minutes.")
    
    if st.button("\U0001f680 Run Benchmark", type="primary", use_container_width=True):
        with st.spinner("Benchmarking all models... This takes 2-3 minutes..."):
            cat = None if selected_cat == "all" else selected_cat
            results = run_benchmark(cat)
        
        if "error" in results:
            st.error(f"Error: {results['error']}")
            st.stop()
        
        st.session_state["benchmark_results"] = results
    
    if "benchmark_results" in st.session_state:
        results = st.session_state["benchmark_results"]
        
        st.markdown("---")
        st.markdown("## \U0001f3c6 Results")
        
        # Key findings
        k1, k2, k3 = st.columns(3)
        with k1:
            st.success(f"**Best Quality**\n\n{results.get('best_quality', '')}")
        with k2:
            st.info(f"**Cheapest**\n\n{results.get('cheapest', '')}")
        with k3:
            st.warning(f"**Fastest**\n\n{results.get('fastest', '')}")
        
        st.markdown("---")
        
        # Key insight
        st.markdown("### \U0001f4a1 Key Insight")
        st.markdown(f"""
        > **{results.get('cost_savings', '0%')} cost savings** possible by using the cheapest model, 
        > with only **{results.get('quality_drop', '0%')} quality drop** compared to the best model.
        """)
        
        st.markdown("---")
        
        # Model comparison table
        model_results = results.get("results", [])
        if model_results:
            st.markdown("### \U0001f4ca Model Comparison")
            
            comparison_data = []
            for r in model_results:
                comparison_data.append({
                    "Model": r.get("model_name", ""),
                    "Category": r.get("category", ""),
                    "Quality Score": f"{r.get('average_score', 0):.1f}%",
                    "Total Cost": f"${r.get('total_cost_usd', 0):.6f}",
                    "Avg Latency": f"{r.get('average_latency_ms', 0):.0f}ms",
                    "Tests Passed": r.get("total_tests", 0),
                    "Value Score": r.get("score_per_dollar", 0)
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            
            # Charts
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("### Quality Score by Model")
                chart_data = pd.DataFrame({
                    "Model": [r["model_name"] for r in model_results],
                    "Score": [r["average_score"] for r in model_results]
                }).set_index("Model")
                st.bar_chart(chart_data)
            
            with c2:
                st.markdown("### Cost by Model")
                chart_data = pd.DataFrame({
                    "Model": [r["model_name"] for r in model_results],
                    "Cost ($)": [r["total_cost_usd"] for r in model_results]
                }).set_index("Model")
                st.bar_chart(chart_data)
            
            c3, c4 = st.columns(2)
            
            with c3:
                st.markdown("### Latency by Model")
                chart_data = pd.DataFrame({
                    "Model": [r["model_name"] for r in model_results],
                    "Latency (ms)": [r["average_latency_ms"] for r in model_results]
                }).set_index("Model")
                st.bar_chart(chart_data)
            
            with c4:
                st.markdown("### Value (Quality per Dollar)")
                chart_data = pd.DataFrame({
                    "Model": [r["model_name"] for r in model_results],
                    "Value": [r.get("score_per_dollar", 0) for r in model_results]
                }).set_index("Model")
                st.bar_chart(chart_data)
            
            st.markdown("---")
            
            # Detailed results per model
            st.markdown("### \U0001f50d Detailed Results Per Model")
            for r in model_results:
                with st.expander(f"{r['model_name']} — Score: {r['average_score']:.1f}% | Cost: ${r['total_cost_usd']:.6f}"):
                    for test in r.get("results", []):
                        status = "\u2705" if test.get("quality_score", 0) > 30 else "\u274c"
                        st.markdown(f"{status} **{test['test_id']}** ({test['category']}) — Score: {test['quality_score']}%")
                        st.markdown(f"  Output: {test['output'][:200]}...")
                        st.markdown(f"  Details: {', '.join(test.get('score_details', []))}")
                        st.markdown("---")
            
            # Download
            st.markdown("### Download Results")
            st.download_button(
                "\U0001f4be Download Full Results (JSON)",
                data=json.dumps(results, indent=2),
                file_name=f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


elif page == "\U0001f9ea Single Test":
    st.markdown('<p class="main-header">\U0001f9ea Single Model Test</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Test one model with custom input</p>', unsafe_allow_html=True)
    
    models = get_models()
    if not models:
        st.error("Cannot connect to server.")
        st.stop()
    
    model = st.selectbox("Select Model", list(models.keys()), format_func=lambda x: models[x]["name"])
    task = st.text_input("Task", value="Summarize this text in 2-3 sentences")
    input_text = st.text_area("Input Text", value="Artificial intelligence is transforming industries worldwide. From healthcare to finance, AI models are being used to automate tasks, make predictions, and drive innovation.", height=150)
    
    if st.button("\U0001f9ea Run Test", type="primary", use_container_width=True):
        with st.spinner("Testing..."):
            result = run_single_eval(model, task, input_text)
        
        if "error" in result:
            st.error(result["error"])
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Quality Score", f"{result.get('quality_score', 0)}%")
            with col2:
                st.metric("Cost", f"${result.get('cost_usd', 0):.6f}")
            with col3:
                st.metric("Latency", f"{result.get('latency_ms', 0):.0f}ms")
            
            st.markdown("### Output")
            st.markdown(result.get("output", ""))
            
            st.markdown("### Score Details")
            for detail in result.get("score_details", []):
                st.markdown(f"- {detail}")
            
            tokens = result.get("tokens", {})
            t1, t2, t3 = st.columns(3)
            with t1:
                st.metric("Input Tokens", tokens.get("input", 0))
            with t2:
                st.metric("Output Tokens", tokens.get("output", 0))
            with t3:
                st.metric("Total Tokens", tokens.get("total", 0))


elif page == "\U0001f4ca Results":
    st.markdown('<p class="main-header">\U0001f4ca Benchmark History</p>', unsafe_allow_html=True)
    
    if "benchmark_results" in st.session_state:
        results = st.session_state["benchmark_results"]
        
        st.markdown(f"**Models Tested:** {results.get('total_models', 0)}")
        st.markdown(f"**Test Cases:** {results.get('total_test_cases', 0)}")
        st.markdown(f"**Best Quality:** {results.get('best_quality', '')}")
        st.markdown(f"**Cheapest:** {results.get('cheapest', '')}")
        st.markdown(f"**Fastest:** {results.get('fastest', '')}")
        st.markdown(f"**Cost Savings:** {results.get('cost_savings', '')}")
        st.markdown(f"**Quality Drop:** {results.get('quality_drop', '')}")
    else:
        st.info("No benchmark results yet. Run a benchmark first!")


elif page == "\U0001f916 Models Info":
    st.markdown('<p class="main-header">\U0001f916 Available Models</p>', unsafe_allow_html=True)
    
    models = get_models()
    if models:
        model_data = []
        for model_id, info in models.items():
            model_data.append({
                "Model ID": model_id,
                "Name": info["name"],
                "Category": info["category"],
                "Input Cost ($/1K)": info["cost_per_1k"]["input"],
                "Output Cost ($/1K)": info["cost_per_1k"]["output"]
            })
        
        st.dataframe(pd.DataFrame(model_data), use_container_width=True)
        
        st.markdown("---")
        st.markdown("### Cost Comparison")
        cost_df = pd.DataFrame({
            "Model": [m["Name"] for m in model_data],
            "Input Cost": [m["Input Cost ($/1K)"] for m in model_data],
            "Output Cost": [m["Output Cost ($/1K)"] for m in model_data]
        }).set_index("Model")
        st.bar_chart(cost_df)
    else:
        st.error("Cannot connect to server.")


st.markdown("---")
st.markdown("<div style=\"text-align:center;color:#888;\">AI Eval Kit v1.0 | LLM Quality Evaluator | Built by Kethavath Santhosh</div>", unsafe_allow_html=True)
