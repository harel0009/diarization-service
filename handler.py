#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Healthcheck עבור RunPod (GET ל־/run)
@app.route("/run", methods=["GET"])
def healthcheck_run():
    return "OK", 200

# Endpoint לדיאריזציה (POST ל־/run/diarize)
@app.route("/run/diarize", methods=["POST"])
def diarize_endpoint():
    data = request.get_json(force=True)
    gcs_uri = data.get("gcs_uri")
    if not gcs_uri:
        return jsonify({"error": "Missing gcs_uri"}), 400

    # הורדת הקובץ ל־/tmp/input.wav
    local_path = "/tmp/input.wav"
    ret = subprocess.run(
        ["wget", "-q", "-O", local_path, gcs_uri]
    )
    if ret.returncode != 0:
        return jsonify({"error": "Failed to download audio"}), 500

    # הרצת הסקריפט diarize.py על הקובץ
    try:
        output = subprocess.check_output(
            ["python", "diarize.py", local_path],
            stderr=subprocess.STDOUT
        )
        segments = json.loads(output)
        return jsonify(segments)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 500

if __name__ == "__main__":
    # רוץ על כל הכתובות כדי שה־healthcheck יעבוד
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
