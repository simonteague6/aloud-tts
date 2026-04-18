from collections.abc import Callable

from pynput import keyboard

from tts_app.config import HOTKEY


def start(callback: Callable[[], None], hotkey: str = HOTKEY) -> keyboard.GlobalHotKeys:
    listener = keyboard.GlobalHotKeys({hotkey: callback})
    listener.start()
    return listener
