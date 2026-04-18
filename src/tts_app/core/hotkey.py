from collections.abc import Callable

from pynput import keyboard

from tts_app.config import HOTKEY

# pynput 1.8.1 on macOS calls on_press(key) without `injected` in the
# media-key branch of _darwin.py:_handle_message, but GlobalHotKeys._on_press
# requires `injected`. Make it default to False so media keys don't raise.
_orig_on_press = keyboard.GlobalHotKeys._on_press
_orig_on_release = keyboard.GlobalHotKeys._on_release
keyboard.GlobalHotKeys._on_press = lambda self, key, injected=False: _orig_on_press(self, key, injected)
keyboard.GlobalHotKeys._on_release = lambda self, key, injected=False: _orig_on_release(self, key, injected)


def start(callback: Callable[[], None], hotkey: str = HOTKEY) -> keyboard.GlobalHotKeys:
    listener = keyboard.GlobalHotKeys({hotkey: callback})
    listener.start()
    return listener
