import spacy

def segment_text(state):
    print(f"\n=== Starting segment_text for {state['audio_path']} ===")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(state["transcribed_text"])
    state["sentences"] = [sent.text for sent in doc.sents]
    print(f"Segmented sentences: {state['sentences']}")
    return state
