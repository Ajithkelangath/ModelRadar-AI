import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ModelRadar AI War Room", layout="wide")

st.title("🚀 ModelRadar AI: Live LLM Intelligence")
st.markdown("Automated benchmarks, pricing tracking, and arbitrage alerts.")

# Sidebar for controls
st.sidebar.header("Controls")
if st.sidebar.button("Run Daily Scan (Manual)"):
    st.sidebar.info("Triggering LangGraph pipeline...")
    # Trigger orchestrator here

# Load Data
def load_data():
    rankings_path = "data/model_rankings.csv"
    if os.path.exists(rankings_path):
        return pd.read_csv(rankings_path)
    return None

df = load_data()

if df is not None:
    st.header("🏆 Live Leaderboard (Value for Money)")
    
    # Hero metrics
    col1, col2, col3 = st.columns(3)
    best_value = df.iloc[0]
    col1.metric("Best Value Model", best_value['model_id'], f"Score: {best_value['value_score']:.2f}")
    
    fastest = df.sort_values(by='avg_speed', ascending=False).iloc[0]
    col2.metric("Speed King", fastest['model_id'], f"{fastest['avg_speed']:.0f} t/s")
    
    cheapest = df.sort_values(by='avg_cost').iloc[0]
    col3.metric("Cost Champion", cheapest['model_id'], f"${cheapest['avg_cost']:.4f}/M")

    # Interactive Table
    st.dataframe(df[['model_id', 'provider', 'avg_perf', 'avg_cost', 'value_score', 'avg_speed']], 
                 use_container_width=True)

    # Arbitrage Section
    st.header("💰 Arbitrage War Room")
    colA, colB = st.columns(2)
    
    # Logic to get arbitrage from engine (simulated if no live engine)
    from src.intelligence_engine import IntelligenceEngine
    engine = IntelligenceEngine()
    deals = engine.detect_arbitrage()
    
    with colA:
        st.subheader("💎 Value Kings")
        st.markdown("*High performance, ultra-low cost.*")
        if deals['value_kings']:
            for deal in deals['value_kings']:
                st.success(f"🔥 **{deal['model_id']}** ({deal['provider']})\n\n"
                           f"Perf: {deal['avg_perf']:.2f} | Cost: ${deal['avg_cost']:.4f}/M")
        else:
            st.info("Searching for top-tier value...")

    with colB:
        st.subheader("⚡ Speed Demons")
        st.markdown("*Extreme throughput for scale.*")
        if deals['speed_demons']:
            for deal in deals['speed_demons']:
                st.warning(f"🚀 **{deal['model_id']}** ({deal['provider']})\n\n"
                           f"Speed: {deal['avg_speed']:.0f} t/s | Cost: ${deal['avg_cost']:.4f}/M")
        else:
            st.info("Monitoring network latency...")

    # ROI Calculator
    st.divider()
    st.subheader("🧮 Potential Monthly Savings")
    monthly_tokens = st.slider("Monthly Token Volume (Millions)", 1, 1000, 10)
    
    # Compare vs GPT-4o standard ($5/M avg)
    standard_cost = monthly_tokens * 5.0
    best_value_cost = monthly_tokens * df['avg_cost'].min()
    savings = standard_cost - best_value_cost
    
    st.metric("Estimated Savings vs. Market Leader", f"${savings:,.2f}", f"{(savings/standard_cost)*100:.1f}% Reduction")

else:
    st.warning("No data found. Please run the pipeline first.")
    st.image("https://via.placeholder.com/800x400?text=ModelRadar+Scanning+for+Profit...", use_column_width=True)
