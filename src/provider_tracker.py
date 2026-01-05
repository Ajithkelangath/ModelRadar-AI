import yaml
import requests
import os
from typing import List, Dict
import pandas as pd

class ProviderScout:
    def __init__(self, config_path: str = "config/providers.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.providers = self.config.get('providers', [])

    def fetch_openai_compatible_models(self, provider: Dict) -> List[Dict]:
        """Fetch models from OpenAI-compatible /models endpoint."""
        api_base = provider.get('api_base')
        api_key = os.getenv(f"{provider['name'].upper()}_API_KEY", "EMPTY")
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(f"{api_base.rstrip('/')}/models", headers=headers, timeout=10)
            if response.status_code == 200:
                models_data = response.json()
                # Unified format for internal database
                extracted = []
                for m in models_data.get('data', []):
                    # Basic extraction, pricing often requires separate scraping or hardcoding
                    extracted.append({
                        "provider": provider['name'],
                        "model_id": m['id'],
                        "created": m.get('created'),
                        "owned_by": m.get('owned_by')
                    })
                return extracted
        except Exception as e:
            print(f"Error fetching from {provider['name']}: {e}")
        return []

    def get_pricing_estimate(self, model_id: str, provider_name: str) -> Dict:
        """
        Hardcoded pricing for MVP. In Phase 2.1, this would scrape provider status pages.
        Returns price per 1M tokens in USD.
        """
        pricing_data = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "llama-3.1-70b-versatile": {"input": 0.59, "output": 0.79},
            "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
            "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
            "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
        }
        return pricing_data.get(model_id, {"input": 1.0, "output": 1.0})

    def run_scan(self):
        all_models = []
        for provider in self.providers:
            print(f"Scanning {provider['name']}...")
            # For MVP, we use the suggested models if API call fails or for non-compatible ones
            models = self.fetch_openai_compatible_models(provider)
            if not models:
                for m_id in provider.get('models_suggested', []):
                    models.append({
                        "provider": provider['name'],
                        "model_id": m_id
                    })
            
            for m in models:
                pricing = self.get_pricing_estimate(m['model_id'], provider['name'])
                m.update(pricing)
            
            all_models.extend(models)
        
        df = pd.DataFrame(all_models)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/provider_catalog.csv", index=False)
        print(f"Catalog saved with {len(df)} models.")
        return df

if __name__ == "__main__":
    scout = ProviderScout()
    scout.run_scan()
