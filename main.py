import logging
import os
import yaml
from langgraph.graph import StateGraph
from typing import Dict, Any
from src.transcribe import transcribe_audio
from src.segment import segment_text
from src.align import align_sentences_with_timestamps
from src.generate import generate_clips
from checkpoint_manager import CheckpointManager

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Load configuration from YAML file
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extract paths from the configuration
input_folder = config['paths']['input_folder']
clips_base_dir = config['paths']['clips_base_dir']
subtitle_base_dir = config['paths']['subtitle_base_dir']

# Initialize checkpoint manager
checkpoint_manager = CheckpointManager(config['paths']['checkpoint_file'])

# Build workflow graph
def build_and_run_workflow():
    workflow = StateGraph()
    
    workflow.add_node("transcribe_audio", transcribe_audio)
    workflow.add_node("segment_text", segment_text)
    workflow.add_node("align_sentences_with_timestamps", align_sentences_with_timestamps)
    workflow.add_node("generate_clips", generate_clips)

    workflow.add_edge("transcribe_audio", "segment_text")
    workflow.add_edge("segment_text", "align_sentences_with_timestamps")
    workflow.add_edge("align_sentences_with_timestamps", "generate_clips")
    
    workflow.set_entry_point("transcribe_audio")
    workflow.set_finish_point("generate_clips")
    
    return workflow.compile()

# Process a single audio file with checkpoints
def process_audio_file(audio_file):
    logger.info(f"Starting to process {audio_file}...")

    # Construct the full audio file path
    audio_path = os.path.join(input_folder, audio_file)
    
    # Define the state dictionary
    audio_name = audio_file.split('.')[0]
    state = {
        'audio_path': audio_path,  # Path of the audio file
        'transcribed_text': None,
        'sentences': None,
        'word_timestamps': None,
        'sentence_timestamps': None,
        'clips_dir': os.path.join(clips_base_dir, audio_name),  # Create separate folder for each file
        'transcribe_dir': os.path.join(subtitle_base_dir, audio_name)  # Create separate folder for each file
    }

    # Ensure that the directories exist
    if not os.path.exists(state['clips_dir']):
        os.makedirs(state['clips_dir'])
    if not os.path.exists(state['transcribe_dir']):
        os.makedirs(state['transcribe_dir'])

    # Load checkpoint for this file
    completed_steps = checkpoint_manager.get_checkpoint(audio_file)

    # Log the completed steps
    logger.info(f"Completed steps for {audio_file}: {completed_steps}")

    # Transcription step
    if 'transcription' not in completed_steps:
        logger.info(f"Transcribing {audio_file}...")
        transcribe_audio(state)
        checkpoint_manager.update_checkpoint(audio_file, 'transcription')

    # Segmentation step
    if 'segmentation' not in completed_steps:
        logger.info(f"Segmenting {audio_file}...")
        segment_text(state)
        checkpoint_manager.update_checkpoint(audio_file, 'segmentation')

    # Sentence alignment step
    if 'alignment' not in completed_steps:
        logger.info(f"Aligning sentences for {audio_file}...")
        align_sentences_with_timestamps(state)
        checkpoint_manager.update_checkpoint(audio_file, 'alignment')

    # Clip generation step
    if 'clip_generation' not in completed_steps:
        logger.info(f"Generating clips for {audio_file}...")
        generate_clips(state)
        checkpoint_manager.update_checkpoint(audio_file, 'clip_generation')

# Main loop to process all files
for audio_file in os.listdir(input_folder):
    if audio_file.endswith('.mp3'):
        process_audio_file(audio_file)
