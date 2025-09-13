from flask import Flask, render_template, request, jsonify
from TTS.api import TTS
import pdfplumber
import soundfile as sf
import os

app = Flask(__name__)

# Load TTS model
tts = TTS("tts_models/en/ljspeech/vits")

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = os.path.join("static", "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded!"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text from PDF
    text = ""
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    else:
        return jsonify({"error": "Only PDF supported in this demo."}), 400

    # Trim (demo) — increase if you want longer segments
    text = text[:500].strip()
    if not text:
        return jsonify({"error": "No extractable text found."}), 400

    # Generate audio (numpy array) and sample rate
    wav = tts.tts(text=text, return_type="np")
    sr = tts.synthesizer.output_sample_rate

    output_file = os.path.join(AUDIO_FOLDER, "output.wav")
    sf.write(output_file, wav, sr)

    # ---- Improved timing calculation (char-weighted + punctuation bonus + normalization) ----
    words = text.split()
    if len(words) == 0:
        return jsonify({"error": "No words to synthesize."}), 400

    audio_duration = len(wav) / sr

    # Base durations proportional to character count
    total_chars = sum(len(w) for w in words) or 1
    base_durations = [ (len(w) / total_chars) * audio_duration for w in words ]

    # Add small pauses for punctuation (but we will normalize later)
    punct_bonus = []
    for w, base in zip(words, base_durations):
        bonus = 0.0
        if w.endswith((".", "!", "?")):
            bonus = 0.20
        elif w.endswith(","):
            bonus = 0.10
        punct_bonus.append(base + bonus)

    # Normalize so the sum equals audio_duration exactly
    total_with_bonus = sum(punct_bonus)
    if total_with_bonus <= 0:
        scale = 1.0
    else:
        scale = audio_duration / total_with_bonus

    durations = [d * scale for d in punct_bonus]

    # Build start/end times; ensure last end exactly equals audio_duration (avoid float drift)
    word_timings = []
    t = 0.0
    for i, (w, dur) in enumerate(zip(words, durations)):
        start = t
        end = t + dur
        # If last word, force end to equal audio_duration to guarantee highlight coverage
        if i == len(words) - 1:
            end = audio_duration
        word_timings.append({"word": w, "start": round(start, 6), "end": round(end, 6)})
        t = end

    return jsonify({
        "text": text,
        "audio": "output.wav",
        "timings": word_timings
    })


if __name__ == "__main__":
    app.run(debug=True)
