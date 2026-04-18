from unittest.mock import MagicMock, patch

from tts_app.core import clipboard


def test_returns_new_text_when_selection_differs():
    with (
        patch.object(clipboard, "pyperclip") as pyperclip_mock,
        patch.object(clipboard, "_kb") as kb_mock,
        patch.object(clipboard.time, "sleep"),
    ):
        pyperclip_mock.paste.side_effect = ["old content", "selected text"]
        kb_mock.pressed.return_value = MagicMock()

        assert clipboard.get_selected_text() == "selected text"
        pyperclip_mock.copy.assert_called_once_with("old content")


def test_returns_none_when_clipboard_unchanged():
    with (
        patch.object(clipboard, "pyperclip") as pyperclip_mock,
        patch.object(clipboard, "_kb") as kb_mock,
        patch.object(clipboard.time, "sleep"),
    ):
        pyperclip_mock.paste.side_effect = ["same", "same"]
        kb_mock.pressed.return_value = MagicMock()

        assert clipboard.get_selected_text() is None
        pyperclip_mock.copy.assert_called_once_with("same")


def test_restores_original_clipboard_even_on_new_selection():
    with (
        patch.object(clipboard, "pyperclip") as pyperclip_mock,
        patch.object(clipboard, "_kb") as kb_mock,
        patch.object(clipboard.time, "sleep"),
    ):
        pyperclip_mock.paste.side_effect = ["original", "new"]
        kb_mock.pressed.return_value = MagicMock()

        clipboard.get_selected_text()
        pyperclip_mock.copy.assert_called_once_with("original")
