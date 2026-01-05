# 🚀 ModelRadar AI: Value & Arbitrage Intelligence

**Stop overpaying for LLMs.** ModelRadar is an autonomous intelligence platform that scans 100+ providers to find the highest-performing models at the lowest possible price.

## 💰 How this "Makes Money" (ROI)
ModelRadar identifies **Value Arbitrage** opportunities where a model performs at ~90% of a top-tier model (like GPT-4o) but costs only ~1% of the price. 
*   **Example**: Switching from GPT-4o to DeepSeek-V3 or a highly-optimized Llama-3 local instance can save thousands of dollars in monthly token costs.
*   **Arbitrage War Room**: The built-in dashboard identifies these "Value Kings" and "Speed Demons" in real-time.

## 🔌 Data-as-a-Service (DaaS)
ModelRadar is more than a dashboard; it's a professional model intelligence feed.
*   **Live JSON Feed**: Access real-time arbitrage and ranking data via our public endpoint.
*   **Developer API**: Integrate "Value King" logic directly into your applications to automate cost-saving.
*   **Commercial License**: Professional feeds with high-frequency updates available for enterprise customers.

## 🌍 Public Deployment
The dashboard is optimized for Streamlit Cloud and Railway.
*   **Live URL**: [Deploying to Streamlit Cloud...]
*   **GitHub Actions**: Runs every 24 hours to refresh the DaaS feed and dataset history.

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
