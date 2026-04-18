import logging
import queue

import rumps

from tts_app.core import hotkey
from tts_app.core.speaker import Speaker, State
from tts_app.menubar.icons import DEFAULT_ICON, ICON_FOR_STATE

log = logging.getLogger(__name__)


class MenuBarApp(rumps.App):
    def __init__(self) -> None:
        super().__init__(name="tts-app", title=DEFAULT_ICON, quit_button=None)
        self.menu = ["Speak selection", "Stop", None, "Unload model", None, "Quit"]

        self._ui_queue: queue.Queue[State] = queue.Queue()
        self.speaker = Speaker(on_state_change=self._ui_queue.put)
        self._ui_drain = rumps.Timer(self._drain_ui_queue, 0.05)
        self._ui_drain.start()

        self.speaker.start()
        self._hotkey_listener = hotkey.start(self.speaker.trigger)

    def _drain_ui_queue(self, _sender) -> None:
        try:
            while True:
                state = self._ui_queue.get_nowait()
                self.title = ICON_FOR_STATE.get(state, DEFAULT_ICON)
        except queue.Empty:
            pass

    @rumps.clicked("Speak selection")
    def _on_speak(self, _sender) -> None:
        self.speaker.trigger()

    @rumps.clicked("Stop")
    def _on_stop(self, _sender) -> None:
        self.speaker.interrupt()

    @rumps.clicked("Unload model")
    def _on_unload(self, _sender) -> None:
        self.speaker.unload_model()
        rumps.notification("tts-app", "", "Model unloaded — next hotkey will reload it.")

    @rumps.clicked("Quit")
    def _on_quit(self, _sender) -> None:
        try:
            self._hotkey_listener.stop()
        except Exception:
            log.exception("hotkey listener stop failed")
        self.speaker.shutdown()
        rumps.quit_application()


def run() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
    MenuBarApp().run()
