from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import numpy as np
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    name = request.form.get("name", "unknown")

    filename = f"{name}_{uuid.uuid4().hex}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # SAVE FILE PERMANENTLY
    file.save(filepath)

    # LOAD AUDIO
    y, sr = librosa.load(filepath, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features = np.mean(mfcc, axis=1).tolist()

    return jsonify({
        "features": features,
        "file": filename
    })

if __name__ == "__main__":
    app.run(debug=True)
