import json
import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/processing.log"),
            logging.StreamHandler()
        ]
    )

def save_checkpoint(state, checkpoint_file="logs/checkpoint.json"):
    with open(checkpoint_file, "w") as f:
        json.dump(state, f)

def load_checkpoint(checkpoint_file="logs/checkpoint.json"):
    try:
        with open(checkpoint_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
