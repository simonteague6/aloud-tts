from unittest.mock import patch

from tts_app.core import hotkey


def test_start_registers_callback_with_default_hotkey():
    callback = lambda: None
    with patch.object(hotkey.keyboard, "GlobalHotKeys") as gh_mock:
        listener = hotkey.start(callback)

    gh_mock.assert_called_once_with({"<ctrl>+<alt>+s": callback})
    assert listener is gh_mock.return_value
    listener.start.assert_called_once()


def test_start_accepts_custom_hotkey():
    callback = lambda: None
    with patch.object(hotkey.keyboard, "GlobalHotKeys") as gh_mock:
        hotkey.start(callback, hotkey="<cmd>+<shift>+t")

    gh_mock.assert_called_once_with({"<cmd>+<shift>+t": callback})
