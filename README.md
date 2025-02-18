# Audio Processor Project

This project processes audio files (MP3 format) to perform transcription, text segmentation, sentence alignment with timestamps, and clip generation. It leverages Whisper for transcription and SpaCy for text processing. The workflow is managed using **LangGraph** for sequential processing of tasks, and **checkpointing** is implemented to allow resuming the process if interrupted.

## Features

- **Transcription**: Converts MP3 audio to text using Whisper.
- **Segmentation**: Splits the transcribed text into segments.
- **Alignment**: Aligns the transcribed text with word-level timestamps.
- **Clip Generation**: Generates audio clips based on aligned segments and timestamps.
- **Checkpointing**: Resumes processing from where it was last stopped in case of interruptions.
- **Folder Organization**: Automatically creates output folders for clips and transcripts per file.

## Requirements

- Python 3.8 or later
- Dependencies listed in `requirements.txt`

### Dependencies

- **Whisper** for transcription.
- **SpaCy** for text segmentation and alignment.
- **LangGraph** for managing workflows.
- **FFmpeg** for audio clip generation.
- **logging** for detailed logging during processing.

### Install Dependencies

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/audio-processor.git
   cd audio-processor
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### `config.yaml`

The project uses a `config.yaml` file for configuration. Here, you can specify paths for input files, output directories, model settings, and more.

Sample configuration:

```yaml
# GPU Configuration
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
```

---

## Getting Started

### Download SpaCy Model

To use SpaCy for text segmentation and alignment, you need to download the **`en_core_web_sm`** model. This is mentioned in the `config.yaml` under `spacy_model`.

Run the following command to download the model:

```bash
python -m spacy download en_core_web_sm
```

---

## Usage

1. Place your audio files (in MP3 format) in the `data/input/` folder.
2. Run the main script to process the audio files:

   ```bash
   python main.py
   ```

   The program will:
   - Transcribe the audio file into text.
   - Segment the transcribed text into smaller parts.
   - Align the sentences with their timestamps.
   - Generate audio clips based on the aligned text and timestamps.

3. The processed clips will be saved in the `output/clips/` directory, and the transcripts will be saved in `output/transcripts/`. Each file will have its own folder within these directories, named after the file.

4. Logs and checkpoints are saved in the `logs/` directory. The checkpoint system ensures that the process can be resumed from where it was left off if interrupted.

---

## Folder Structure

```
audio_processor/
├── config/
│   └── config.yaml
├── data/
│   └── input/         # Input MP3 files for processing
├── logs/
│   └── checkpoint.json   # Checkpoints for resuming the process
├── output/
│   ├── clips/         # Generated audio clips

│   └── transcripts/   # Transcribed text files
├── src/
│   ├── transcribe.py   # Code for transcription
│   ├── segment.py      # Code for text segmentation
│   ├── align.py        # Code for sentence alignment
│   └── generate.py     # Code for generating clips
├── main.py             # Main script to process audio files
├── checkpoint_manager.py # Manages checkpoints (used to resume processing)
└── .gitignore          # To exclude unnecessary files from version control
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
