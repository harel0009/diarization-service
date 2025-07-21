#!/usr/bin/env python3
import os
import sys
import json
from pyannote.audio import Pipeline
from pydub import AudioSegment

if len(sys.argv) != 2:
    print("Usage: python diarize.py path/to/audio.wav")
    sys.exit(1)

audio_path = sys.argv[1]

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("Missing HF_TOKEN environment variable")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=hf_token
)

diarization = pipeline(audio_path)

segments = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    segments.append({
        "start": round(turn.start, 3),
        "end":   round(turn.end,   3),
        "speaker": speaker
    })

# מדפיס JSON למערכת הקריאה (stdout)
print(json.dumps(segments, ensure_ascii=False))
