import time

import pyperclip
from pynput import keyboard

_kb = keyboard.Controller()

# Time to wait for macOS clipboard to update after simulating Cmd+C.
# 0.15s is a conservative bump from the 0.1s used in the prototype — covers
# focus jitter when the hotkey is pressed from another app.
_COPY_SETTLE_SECONDS = 0.15


def get_selected_text() -> str | None:
    old = pyperclip.paste()
    with _kb.pressed(keyboard.Key.cmd):
        _kb.tap("c")
    time.sleep(_COPY_SETTLE_SECONDS)
    new = pyperclip.paste()
    pyperclip.copy(old)
    if new == old:
        return None
    return new
