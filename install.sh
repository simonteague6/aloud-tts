#!/usr/bin/env bash
set -euo pipefail

# --- platform check ---
if [[ "$(uname -s)" != "Darwin" || "$(uname -m)" != "arm64" ]]; then
  echo "Error: aloud-tts requires macOS on Apple Silicon (arm64)." >&2
  exit 1
fi

macos_version=$(sw_vers -productVersion)
macos_major=$(echo "$macos_version" | cut -d. -f1)
if [[ "$macos_major" -lt 14 ]]; then
  echo "Error: aloud-tts requires macOS 14 (Sonoma) or later. You have $macos_version." >&2
  exit 1
fi

# --- ensure uv ---
if ! command -v uv &>/dev/null; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# --- install aloud-tts ---
echo "Installing aloud-tts..."
uv tool install --python 3.12 aloud-tts

# --- done ---
echo ""
echo "aloud-tts installed. Launch it with: aloud-tts"
echo ""
echo "Before the hotkey works, grant two permissions in System Settings:"
echo "  1. Privacy & Security → Accessibility → add your terminal"
echo "  2. Privacy & Security → Input Monitoring → add your terminal"
echo ""
echo "Opening Privacy & Security now..."
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility" 2>/dev/null || true
