import os

def create_folder_structure():
    # Define the folder structure
    folders = [
        "data/input",  # Folder for audio files
        "output/clips",  # Folder for audio clips
        "output/transcripts",  # Folder for transcripts
        "logs",  # Folder for logs
        "config"  # Folder for config
    ]
    
    # Create the folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    # Create the config.yaml file with basic template
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write("""# GPU Configuration
gpu:
  device: "cuda"
  fallback_to_cpu: true

# Model Configuration
model:
  whisper_model: "base"
  spacy_model: "en_core_web_sm"

# Path Configuration
paths:
  input_folder: "data/input"
  clips_base_dir: "output/clips"
  subtitle_base_dir: "output/transcripts"
  checkpoint_file: "logs/checkpoint.json"

# Processing Configuration
audio:
  min_segment_duration: 3.0
  max_segment_duration: 12.0
  segment_buffer: 0.1

# Logging Configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(levelname)s - %(message)s"
  file: "logs/processing.log"
""")
        print(f"Created config.yaml at: {config_path}")

# Run the function to create folder structure
create_folder_structure()
