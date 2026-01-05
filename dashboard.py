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
    st.header("💰 Arbitrage Alerts")
    deals = df[(df['avg_perf'] > 0.75) & (df['avg_cost'] < 0.5)]
    if not deals.empty:
        for idx, row in deals.iterrows():
            st.success(f"🔥 **{row['model_id']} ({row['provider']})**: High performance at ultra-low cost (${row['avg_cost']}/M)!")
    else:
        st.info("No major arbitrage opportunities detected today.")

else:
    st.warning("No data found. Please run the pipeline first.")
    st.image("https://via.placeholder.com/800x400?text=ModelRadar+Awaiting+Data", use_column_width=True)
