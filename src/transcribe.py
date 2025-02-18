import whisper

def transcribe_audio(state):
    print(f"\n=== Starting transcribe_audio for {state['audio_path']} ===")
    model = whisper.load_model("base")
    result = model.transcribe(state["audio_path"], word_timestamps=True)
    state["transcribed_text"] = result["text"]
    state["word_timestamps"] = result["segments"]
    print(f"Transcribed text: {state['transcribed_text']}")
    return state
