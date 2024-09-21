import os
import torch

MODEL_DIR = "models"
MODEL_TYPE = "vit_h"

def download_model(model_type=MODEL_TYPE):
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, f"sam_{model_type}.pth")
    if not os.path.exists(model_path):
        url = f"https://dl.fbaipublicfiles.com/segment_anything/sam_{model_type}.pth"
        torch.hub.download_url_to_file(url, model_path)
    return model_path

if __name__ == "__main__":
    download_model()