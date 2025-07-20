# handler.py
import os, sys, json
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/diarize", methods=["POST"])
def diarize_endpoint():
    data = request.get_json()
    gcs_uri = data.get("gcs_uri")
    if not gcs_uri:
        return jsonify({"error": "Missing gcs_uri"}), 400

    # כאן ירדידו את הקובץ ל־/tmp/input.wav
    local_path = "/tmp/input.wav"
    # לדוגמה using wget; אפשר גם curl
    ret = subprocess.run([
        "wget", "-q", "-O", local_path, gcs_uri
    ])
    if ret.returncode != 0:
        return jsonify({"error": "Failed to download audio"}), 500

    # עכשיו קוראים ל־diarize.py על הקובץ שהורד
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
    # Run on 0.0.0.0 כדי שה־healthcheck יעבוד
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
