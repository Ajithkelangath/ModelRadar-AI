import pandas as pd
import json
import os
from datetime import datetime

class DaaSGenerator:
    def __init__(self, rankings_path: str = "data/model_rankings.csv", output_path: str = "data/live_intel.json"):
        self.rankings_path = rankings_path
        self.output_path = output_path

    def generate_feed(self):
        if not os.path.exists(self.rankings_path):
            print(f"Error: {self.rankings_path} not found.")
            return False
            
        df = pd.read_csv(self.rankings_path)
        
        # Structure the data for a professional API feed
        intel_feed = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_models_scanned": len(df),
                "license": "ModelRadar Commercial-DaaS-v1"
            },
            "top_value_models": df.head(10).to_dict('records'),
            "arbitrage_alerts": {
                "high_performance": df[(df['avg_perf'] > 0.8) & (df['avg_cost'] < 0.5)].to_dict('records'),
                "high_speed": df[(df['avg_speed'] > 100) & (df['avg_cost'] < 0.1)].to_dict('records')
            }
        }
        
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w') as f:
            json.dump(intel_feed, f, indent=4)
            
        print(f"DaaS Feed generated at {self.output_path}")
        return True

if __name__ == "__main__":
    generator = DaaSGenerator()
    generator.generate_feed()
