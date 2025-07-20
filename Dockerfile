FROM python:3.9-slim

WORKDIR /app

# 1) FFmpeg ו‑wget
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg wget && \
    rm -rf /var/lib/apt/lists/*

# 2) העתק והתקן תלויות Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) העתק כל הקוד
COPY . .

# 4) הפעל את ה‑handler.py כשרת Flask
ENTRYPOINT ["python", "handler.py"]
