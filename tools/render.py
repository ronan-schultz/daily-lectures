"""Render a lecture script to MP3 with the Kokoro TTS model.

Usage: python3 -I tools/render.py SCRIPT.txt OUT.mp3 [voice] [speed]
Expects the model files in ~/kokoro/ (tools/setup.sh downloads them).
Paragraphs (blank-line separated) are rendered one at a time with a short pause between them.
"""
import os, sys, subprocess, tempfile
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

src, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
lang = "en-gb" if voice.startswith("b") else "en-us"
home = os.path.expanduser("~/kokoro")
k = Kokoro(os.path.join(home, "kokoro.onnx"), os.path.join(home, "voices.bin"))

paras = [p.strip() for p in open(src).read().split("\n\n") if p.strip()]
pieces, sr = [], 24000
for i, p in enumerate(paras):
    samples, sr = k.create(p, voice=voice, speed=speed, lang=lang)
    pieces += [samples, np.zeros(int(sr * 0.6), dtype=samples.dtype)]
    print(f"{i + 1}/{len(paras)}", flush=True)

with tempfile.TemporaryDirectory() as d:
    wav = os.path.join(d, "out.wav")
    sf.write(wav, np.concatenate(pieces), sr)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav,
                    "-codec:a", "libmp3lame", "-b:a", "48k", "-ac", "1", out], check=True)
print("wrote", out)
