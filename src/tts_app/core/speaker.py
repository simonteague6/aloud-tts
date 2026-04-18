import logging
import queue
import threading
from collections.abc import Callable
from enum import Enum
from typing import Optional

from tts_app import config
from tts_app.core.audio import AudioPlayer
from tts_app.core.clipboard import get_selected_text
from tts_app.core.tts import GenerationCancelled, TTSEngine

log = logging.getLogger(__name__)


class State(Enum):
    LOADING = "loading"
    IDLE = "idle"
    CAPTURING = "capturing"
    GENERATING = "generating"
    SPEAKING = "speaking"
    INTERRUPTING = "interrupting"


StateCallback = Callable[[State], None]


class Speaker:
    def __init__(
        self,
        on_state_change: StateCallback,
        engine: Optional[TTSEngine] = None,
        audio: Optional[AudioPlayer] = None,
        capture_text: Callable[[], Optional[str]] = get_selected_text,
    ) -> None:
        self._on_state_change = on_state_change
        self._engine = engine or TTSEngine()
        self._audio = audio or AudioPlayer()
        self._capture_text = capture_text

        self._state = State.LOADING
        self._lock = threading.Lock()
        self._queue: queue.Queue[None] = queue.Queue(maxsize=1)
        self._stop_event = threading.Event()
        self._shutdown_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    @property
    def state(self) -> State:
        return self._state

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, daemon=True, name="speaker")
        self._thread.start()

    def trigger(self) -> None:
        with self._lock:
            if self._state == State.IDLE:
                try:
                    self._queue.put_nowait(None)
                except queue.Full:
                    pass
            elif self._state in (State.CAPTURING, State.GENERATING, State.SPEAKING):
                self._interrupt_locked()
            # LOADING / INTERRUPTING: ignore

    def interrupt(self) -> None:
        with self._lock:
            self._interrupt_locked()

    def _interrupt_locked(self) -> None:
        self._stop_event.set()
        self._audio.stop()
        self._set_state(State.INTERRUPTING)

    def shutdown(self) -> None:
        self._shutdown_event.set()
        self._stop_event.set()
        self._audio.stop()
        try:
            self._queue.put_nowait(None)
        except queue.Full:
            pass
        if self._thread is not None:
            self._thread.join(timeout=2.0)

    def unload_model(self) -> None:
        self._engine.unload()

    def _set_state(self, new_state: State) -> None:
        self._state = new_state
        try:
            self._on_state_change(new_state)
        except Exception:
            log.exception("state callback raised")

    def _run(self) -> None:
        self._set_state(State.LOADING)
        try:
            self._engine.load()
            self._engine.warmup()
        except Exception:
            log.exception("model load/warmup failed")
        self._set_state(State.IDLE)

        while not self._shutdown_event.is_set():
            self._queue.get()
            if self._shutdown_event.is_set():
                break
            self._stop_event.clear()
            self._handle_request()

    def _handle_request(self) -> None:
        try:
            self._set_state(State.CAPTURING)
            text = self._capture_text()
            if text is None or self._stop_event.is_set():
                return

            self._set_state(State.GENERATING)
            self._engine.generate(text, config.WAV_PATH, cancel=self._stop_event)
            if self._stop_event.is_set():
                return

            self._set_state(State.SPEAKING)
            self._audio.play(config.WAV_PATH)
            self._audio.wait(self._stop_event)
        except GenerationCancelled:
            pass
        except Exception:
            log.exception("request failed")
        finally:
            self._set_state(State.IDLE)
