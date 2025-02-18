def align_sentences_with_timestamps(state):
    print(f"\n=== Starting align_sentences_with_timestamps for {state['audio_path']} ===")
    sentence_timestamps = []
    current_words = []
    current_start = None

    for segment in state["word_timestamps"]:
        if current_start is None:
            current_start = segment["start"]
        current_text = " ".join(current_words + [segment["text"]]).strip()
        for sentence in state["sentences"]:
            clean_sentence = sentence.strip()
            clean_current = current_text.strip()
            if clean_sentence in clean_current:
                sentence_timestamps.append({
                    "sentence": clean_sentence,
                    "start": current_start,
                    "end": segment["end"]
                })
                current_words = []
                current_start = None
                break
        else:
            current_words.append(segment["text"])

    state["sentence_timestamps"] = sentence_timestamps
    print(f"Aligned sentence timestamps: {sentence_timestamps}")
    return state
