import pandas as pd
import os
from typing import Dict

class IntelligenceEngine:
    def __init__(self, catalog_path: str = "data/provider_catalog.csv", benchmark_path: str = "data/benchmark_results.csv"):
        self.catalog_path = catalog_path
        self.benchmark_path = benchmark_path

    def calculate_rankings(self):
        if not os.path.exists(self.catalog_path) or not os.path.exists(self.benchmark_path):
            print("Missing data files for ranking.")
            return None
        
        catalog = pd.read_csv(self.catalog_path)
        benchmarks = pd.read_csv(self.benchmark_path)
        
        # Merge catalog (pricing) with benchmarks (performance)
        df = pd.merge(benchmarks, catalog[['model_id', 'provider', 'input', 'output']], on=['model_id', 'provider'])
        
        # Value Score = (Avg Performance Score) / (Cost per 1M tokens)
        # Normalize performance: (Coding + Math + Reasoning) / 3
        performance_cols = [c for c in df.columns if "_score" in c]
        df['avg_perf'] = df[performance_cols].mean(axis=1)
        
        # Avg cost = (input + output) / 2
        df['avg_cost'] = (df['input'] + df['output']) / 2
        
        # Value score: High is better. (Perf / Cost)
        # Avoid division by zero
        df['value_score'] = df['avg_perf'] / (df['avg_cost'] + 0.0001)
        
        # Rank by Value Score
        df = df.sort_values(by='value_score', ascending=False)
        
        df.to_csv("data/model_rankings.csv", index=False)
        print("Intelligence Engine: Rankings recalculated.")
        return df

    def detect_arbitrage(self):
        """Find models that perform like top-tier but cost significantly less."""
        if not os.path.exists("data/model_rankings.csv"):
            self.calculate_rankings()
            
        df = pd.read_csv("data/model_rankings.csv")
        
        # 1. High Performance Arbitrage: Perf > 0.8, Cost < $0.50
        # These are models that can replace GPT-4/Pro for most tasks at 1/10th the cost.
        high_perf_deals = df[(df['avg_perf'] > 0.8) & (df['avg_cost'] < 0.5)]
        
        # 2. Speed Arbitrage: Speed > 100 t/s, Cost < $0.10
        # These are "Free" level speeds for production workloads.
        speed_deals = df[(df['avg_speed'] > 100) & (df['avg_cost'] < 0.1)]
        
        return {
            "value_kings": high_perf_deals.to_dict('records'),
            "speed_demons": speed_deals.to_dict('records')
        }

if __name__ == "__main__":
    engine = IntelligenceEngine()
    engine.calculate_rankings()
    deals = engine.detect_arbitrage()
    print(f"Top Arbitrage Opportunity: {deals.iloc[0]['model_id']} from {deals.iloc[0]['provider']}")
