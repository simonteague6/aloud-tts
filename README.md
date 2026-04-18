# tts-app

macOS menu bar text-to-speech. Select text anywhere → press **Ctrl+Alt+S** → local Kokoro-82M (MLX) speaks it aloud. Fully offline.

## Install

```
uv sync
```

Requires macOS + Apple Silicon, Python 3.12.

## Menu bar app

```
uv run tts-app
```

First launch: macOS will prompt for **Accessibility** (for the simulated Cmd+C) and **Input Monitoring** (for the global hotkey). Grant both in System Settings → Privacy & Security, then relaunch.

Icon shows the current state: ⋯ loading, 🔈 idle, 📋 capturing, ✨ generating, 🔊 speaking.

Pressing the hotkey during playback stops it. Press again to speak a new selection.

## CLI

```
uv run tts-app-cli "Hello world"
uv run tts-app-cli - < some_file.txt
uv run tts-app-cli "save but don't play" --out /tmp/out.wav --no-play
```

## Tests

```
uv run pytest tests/
```
