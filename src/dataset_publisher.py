import pandas as pd
import os
from datetime import datetime

class DatasetPublisher:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

    def prepare_parquet(self):
        rankings_path = os.path.join(self.data_dir, "model_rankings.csv")
        if not os.path.exists(rankings_path):
            print("No rankings found to publish.")
            return None
        
        df = pd.read_csv(rankings_path)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"model_intel_{timestamp}.parquet"
        publish_path = os.path.join(self.data_dir, filename)
        
        df.to_parquet(publish_path, index=False)
        print(f"Parquet dataset prepared: {publish_path}")
        return publish_path

    def publish_to_hf(self, file_path: str, repo_id: str):
        """
        Uploads the dataset to Hugging Face Datasets.
        Requires HUGGINGFACE_TOKEN as an environment variable.
        """
        token = os.getenv("HUGGINGFACE_TOKEN")
        if not token:
            print("HUGGINGFACE_TOKEN not found. Skipping upload.")
            return False
            
        try:
            from huggingface_hub import HfApi
            api = HfApi()
            print(f"Uploading {file_path} to HF repo {repo_id}...")
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=os.path.basename(file_path),
                repo_id=repo_id,
                repo_type="dataset",
                token=token
            )
            print("Upload successful!")
            return True
        except Exception as e:
            print(f"HF Upload failed: {e}")
            return False

if __name__ == "__main__":
    publisher = DatasetPublisher()
    path = publisher.prepare_parquet()
    if path:
        # Default repo if not specified via env
        repo = os.getenv("HF_REPO_ID", "your-username/model-radar-intelligence")
        publisher.publish_to_hf(path, repo_id=repo)
