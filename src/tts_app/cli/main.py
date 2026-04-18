import argparse
import sys
from pathlib import Path

from tts_app import config
from tts_app.core.audio import AudioPlayer
from tts_app.core.tts import TTSEngine


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tts-app-cli",
        description="Speak text out loud using local MLX Audio (Kokoro).",
    )
    parser.add_argument("text", help="Text to speak. Use '-' to read from stdin.")
    parser.add_argument("--out", type=Path, default=config.WAV_PATH, help="WAV output path.")
    parser.add_argument("--no-play", action="store_true", help="Generate WAV, don't play it.")
    args = parser.parse_args()

    text = sys.stdin.read() if args.text == "-" else args.text
    if not text.strip():
        parser.error("empty text")

    engine = TTSEngine()
    engine.load()
    engine.generate(text, args.out)
    print(args.out)

    if not args.no_play:
        player = AudioPlayer()
        player.play(args.out)
        player.wait()
