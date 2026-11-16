#!/bin/sh
# One-time per session: install the TTS runtime and download the Kokoro model (hosted on GitHub releases).
set -e
pip install --break-system-packages -q kokoro-onnx soundfile 2>/dev/null
mkdir -p ~/kokoro
base=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s ~/kokoro/kokoro.onnx ] || curl -sSL -o ~/kokoro/kokoro.onnx $base/kokoro-v1.0.int8.onnx
[ -s ~/kokoro/voices.bin ] || curl -sSL -o ~/kokoro/voices.bin $base/voices-v1.0.bin
which ffmpeg >/dev/null
echo "setup ok"
