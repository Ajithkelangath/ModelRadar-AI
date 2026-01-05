import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# Import our agents
from provider_tracker import ProviderScout
from auto_benchmarker import AutoBenchmarker
from intelligence_engine import IntelligenceEngine

class AgentState(TypedDict):
    step: str
    catalog_ready: bool
    benchmarks_ready: bool
    rankings_ready: bool

def run_scout(state: AgentState):
    print("--- 1. RUNNING SCOUT ---")
    scout = ProviderScout()
    scout.run_scan()
    return {"step": "benchmark", "catalog_ready": True}

def run_benchmark(state: AgentState):
    print("--- 2. RUNNING BENCHMARKER ---")
    benchmarker = AutoBenchmarker()
    # If API keys are present, do real benchmarking
    has_keys = any(os.getenv(f"{p['provider'].upper().replace(' ', '_')}_API_KEY") for p in benchmarker.catalog.to_dict('records'))
    benchmarker.benchmark_all(real=has_keys)
    return {"step": "rank", "benchmarks_ready": True}

def run_engine(state: AgentState):
    print("--- 3. RUNNING INTELLIGENCE ENGINE ---")
    engine = IntelligenceEngine()
    engine.calculate_rankings()
    return {"step": "complete", "rankings_ready": True}

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("scout", run_scout)
workflow.add_node("benchmark", run_benchmark)
workflow.add_node("engine", run_engine)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "benchmark")
workflow.add_edge("benchmark", "engine")
workflow.add_edge("engine", END)

app = workflow.compile()

if __name__ == "__main__":
    print("Starting ModelRadar Pipeline...")
    inputs = {"step": "start", "catalog_ready": False, "benchmarks_ready": False, "rankings_ready": False}
    for output in app.stream(inputs):
        print(output)
