# 🚀 ModelRadar AI: Value & Arbitrage Intelligence

**Stop overpaying for LLMs.** ModelRadar is an autonomous intelligence platform that scans 100+ providers to find the highest-performing models at the lowest possible price.

## 💰 How this "Makes Money" (ROI)
ModelRadar identifies **Value Arbitrage** opportunities where a model performs at ~90% of a top-tier model (like GPT-4o) but costs only ~1% of the price. 
*   **Example**: Switching from GPT-4o to DeepSeek-V3 or a highly-optimized Llama-3 local instance can save thousands of dollars in monthly token costs.
*   **Arbitrage War Room**: The built-in dashboard identifies these "Value Kings" and "Speed Demons" in real-time.

## 🛠️ Components
1.  **Provider Scout**: Scans 100+ API endpoints and local Ollama instances for model metadata and pricing.
2.  **Auto Benchmarker**: Runs low-latency performance tests (Coding, Math, Reasoning) to verify model quality.
3.  **Intelligence Engine**: Calculates a `Value Score` (Performance / Cost) and detects arbitrage.
4.  **Dataset Publisher**: Bundles the intelligence into Parquet files for historical analysis or public sharing on Hugging Face.

## 🚀 Getting Started
1.  **Clone & Install**:
    ```bash
    git clone https://github.com/Ajithkelangath/ModelRadar-AI.git
    cd ModelRadar-AI
    pip install -r requirements.txt
    ```
2.  **Configure API Keys**:
    Set your `GROQ_API_KEY`, `OPENAI_API_KEY`, and `HUGGINGFACE_TOKEN` in your environment.
3.  **Run the Pipeline**:
    ```bash
    python src/langgraph_orchestrator.py
    ```
4.  **Launch Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```

## 📊 Live Monitoring
The platform runs daily via GitHub Actions, pushing the latest intelligence to the `data/` directory and your Hugging Face space.

---
Built with ❤️ for LLM efficiency and profit.
