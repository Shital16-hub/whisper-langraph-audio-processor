import ffmpeg
import os

def generate_clips(state):
    print(f"\n=== Starting generate_clips for {state['audio_path']} ===")
    clips = []
    transcripts = []

    os.makedirs(state["clips_dir"], exist_ok=True)
    os.makedirs(state["transcribe_dir"], exist_ok=True)

    segments = state["sentence_timestamps"]
    grouped_segments = []
    i = 0

    while i < len(segments):
        current_segment = segments[i]
        segment_duration = current_segment["end"] - current_segment["start"]
        if 3.0 <= segment_duration <= 12.0:
            grouped_segments.append([current_segment])
            i += 1
            continue

        current_group = [current_segment]
        current_duration = segment_duration
        while current_duration < 3.0 and i + 1 < len(segments):
            next_segment = segments[i + 1]
            next_duration = next_segment["end"] - next_segment["start"]
            if current_duration + next_duration <= 12.0:
                current_group.append(next_segment)
                current_duration += next_duration
                i += 1
            else:
                break

        if current_duration < 3.0 and len(grouped_segments) > 0:
            prev_group = grouped_segments[-1]
            prev_duration = prev_group[-1]["end"] - prev_group[0]["start"]
            if len(prev_group) == 1 and (prev_duration + current_duration <= 12.0):
                prev_group.extend(current_group)
            else:
                grouped_segments.append(current_group)
        else:
            grouped_segments.append(current_group)

        i += 1

    for group_idx, group in enumerate(grouped_segments, 1):
        file_number = str(group_idx).zfill(6)
        start_time = group[0]["start"]
        end_time = group[-1]["end"] + 0.1
        duration = end_time - start_time

        clip_path = os.path.join(state["clips_dir"], f"audio_{file_number}.wav")
        transcript_path = os.path.join(state["transcribe_dir"], f"text_{file_number}.txt")

        ffmpeg.input(state["audio_path"], ss=start_time, t=duration).output(clip_path, **{'c': 'copy'}).overwrite_output().run()
        with open(transcript_path, "w", encoding='utf-8') as f:
            sentences = [segment['sentence'] for segment in group]
            f.write(" ".join(sentences))

        clips.append(clip_path)
        transcripts.append(transcript_path)
        print(f"Generated clip {file_number}: {clip_path} (duration: {duration:.2f}s)")

    state["clips"] = clips
    state["transcripts"] = transcripts
    return state
