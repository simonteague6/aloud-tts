# tts-app

A macOS menu bar text-to-speech tool. Select text anywhere → press **⌃⌥S** → a local Kokoro-82M model (via MLX) speaks it aloud.

- **Fully offline.** Text never leaves your machine. No API keys, no accounts.
- **Fast.** Runs on Apple Silicon's Neural Engine via MLX; first word plays in ~1s after warmup.
- **Lightweight.** One menu bar icon. No background window, no tray clutter.
- **Free & open source.** MIT licensed.

## Requirements

- macOS on **Apple Silicon** (M1/M2/M3/M4) — MLX doesn't support Intel Macs
- **Python 3.12** (not 3.13+)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management

## Install

```bash
git clone https://github.com/simonteague6/tts-app.git
cd tts-app
uv sync
```

First run downloads the Kokoro model (~330 MB) into your Hugging Face cache.

## Run the menu bar app

```bash
uv run tts-app
```

### Grant permissions (one-time)

On first launch, macOS will prompt for two permissions. **Both are required** — the hotkey is silent without them.

1. **Accessibility** — lets the app simulate ⌘C to grab your selection.
2. **Input Monitoring** — lets the app listen for the global hotkey.

System Settings → Privacy & Security → add `tts-app` (or the terminal you launched it from) to both lists. Fully quit and relaunch afterward.

### How to use it

1. Select text in any app — browser, PDF, email, anywhere.
2. Press **⌃⌥S** (Control + Option + S).
3. Listen.

The menu bar icon shows what's happening:

| Icon | State |
|------|-------|
| ⋯ | Loading model (startup only) |
| 🔈 | Idle, ready |
| 📋 | Capturing selection |
| ✨ | Generating audio |
| 🔊 | Speaking |

Press the hotkey again during playback to stop. Press once more to speak a new selection.

## CLI

One-shot synthesis with no menu bar:

```bash
uv run tts-app-cli "Hello world"                     # speak and exit
uv run tts-app-cli - < article.txt                   # read text from stdin
uv run tts-app-cli "save it" --out out.wav --no-play # generate WAV only
```

## Configuration

Edit `src/tts_app/config.py` and relaunch.

| Setting | Default | Notes |
|---------|---------|-------|
| `HOTKEY` | `<ctrl>+<alt>+s` | [pynput hotkey format](https://pynput.readthedocs.io/en/latest/keyboard.html#global-hotkeys) |
| `MODEL` | `prince-canuma/Kokoro-82M` | Any Kokoro checkpoint on Hugging Face |
| `VOICE` | `af_heart` | [Available voices](https://huggingface.co/hexgrad/Kokoro-82M#voicepacks) |
| `SPEED` | `1.0` | Clamp to 0.5–2.0 for natural output |

## Troubleshooting

**The hotkey does nothing.** Input Monitoring isn't granted, or was granted to the wrong binary (common after updating your terminal). Remove and re-add the entry in System Settings, then fully quit and relaunch.

**It triggers but speaks nothing.** Accessibility isn't granted, so the simulated ⌘C reads an empty clipboard. Same fix.

**Menu bar shows ⋯ forever.** Model is still downloading on first run. Watch `~/.cache/huggingface/` for progress.

**`ModuleNotFoundError: misaki`.** Rerun `uv sync` — it's an optional Kokoro dep that must be installed.

## Development

```bash
uv run pytest tests/          # ~2s, fakes the TTS engine
uv run ruff check src/ tests/
```

The codebase is split so the UI layer (`rumps`) and the core (clipboard + TTS + audio) are independent — both the menu bar app and the CLI reuse `core/`.

## Credits

- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) — the TTS model
- [mlx-audio](https://github.com/Blaizzy/mlx-audio) — MLX inference
- [rumps](https://github.com/jaredks/rumps) — Python for macOS menu bar apps

## License

MIT — see [LICENSE](LICENSE).
