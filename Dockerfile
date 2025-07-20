# Base44 Pyannote Diarization Worker – רק inference
FROM python:3.9-slim

# 1. Set workdir
WORKDIR /app

# 2. Install ffmpeg for pydub
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 3. Copy & install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy only the diarization script
COPY diarize.py .

# 5. Entry point: read path/to/audio.wav from argv, emit JSON to stdout
ENTRYPOINT ["python", "diarize.py"]
