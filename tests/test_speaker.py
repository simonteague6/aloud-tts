import threading
import time
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock

import pytest

from tts_app.core.speaker import Speaker, State
from tts_app.core.tts import GenerationCancelled


class FakeEngine:
    def __init__(self, generate_delay: float = 0.0) -> None:
        self.generate_delay = generate_delay
        self.load_called = False
        self.warmup_called = False

    def load(self) -> None:
        self.load_called = True

    def warmup(self) -> None:
        self.warmup_called = True

    def unload(self) -> None:
        pass

    def generate(self, text: str, out: Path, cancel: Optional[threading.Event] = None):
        deadline = time.time() + self.generate_delay
        while time.time() < deadline:
            if cancel is not None and cancel.is_set():
                raise GenerationCancelled
            time.sleep(0.01)
        return out


class FakeAudio:
    def __init__(self, play_delay: float = 0.0) -> None:
        self.play_delay = play_delay
        self._playing = False
        self._play_deadline = 0.0
        self._stop_called = False

    def play(self, path: Path) -> None:
        self._playing = True
        self._play_deadline = time.time() + self.play_delay

    def stop(self) -> None:
        self._stop_called = True
        self._playing = False

    def is_playing(self) -> bool:
        return self._playing and time.time() < self._play_deadline

    def wait(self, stop_event: Optional[threading.Event] = None) -> None:
        while self.is_playing():
            if stop_event is not None and stop_event.is_set():
                self.stop()
                return
            time.sleep(0.01)
        self._playing = False


@pytest.fixture
def states():
    return []


@pytest.fixture
def speaker(states):
    engine = FakeEngine(generate_delay=0.1)
    audio = FakeAudio(play_delay=0.2)
    s = Speaker(
        on_state_change=states.append,
        engine=engine,
        audio=audio,
        capture_text=lambda: "hello world",
    )
    s.start()
    _wait_for_state(s, State.IDLE, timeout=1.0)
    yield s
    s.shutdown()


def _wait_for_state(s: Speaker, target: State, timeout: float = 1.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if s.state == target:
            return
        time.sleep(0.005)
    raise AssertionError(f"state did not reach {target}, stuck at {s.state}")


def _wait_for_n_states(states: list, n: int, timeout: float = 2.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if len(states) >= n:
            return
        time.sleep(0.005)
    raise AssertionError(f"only got {len(states)} states: {states}, wanted {n}")


def test_starts_in_loading_then_idle(states, speaker):
    assert State.LOADING in states
    assert State.IDLE in states
    assert speaker.state == State.IDLE


def test_trigger_idle_cycles_through_states(states, speaker):
    states.clear()
    speaker.trigger()
    _wait_for_n_states(states, 4, timeout=2.0)

    assert states[0] == State.CAPTURING
    assert State.GENERATING in states
    assert State.SPEAKING in states
    assert states[-1] == State.IDLE


def test_trigger_while_speaking_interrupts(states, speaker):
    speaker.trigger()
    _wait_for_state(speaker, State.SPEAKING, timeout=2.0)

    speaker.trigger()  # should interrupt
    _wait_for_state(speaker, State.IDLE, timeout=1.0)

    assert State.INTERRUPTING in states


def test_trigger_with_no_selection_returns_to_idle(states):
    engine = FakeEngine()
    audio = FakeAudio()
    s = Speaker(
        on_state_change=states.append,
        engine=engine,
        audio=audio,
        capture_text=lambda: None,
    )
    s.start()
    _wait_for_state(s, State.IDLE, timeout=1.0)

    states.clear()
    s.trigger()
    _wait_for_n_states(states, 2, timeout=1.0)

    assert states[0] == State.CAPTURING
    assert states[-1] == State.IDLE
    assert State.GENERATING not in states
    s.shutdown()


def test_shutdown_exits_worker_cleanly(states):
    engine = FakeEngine()
    audio = FakeAudio()
    s = Speaker(
        on_state_change=states.append,
        engine=engine,
        audio=audio,
        capture_text=lambda: "hi",
    )
    s.start()
    _wait_for_state(s, State.IDLE, timeout=1.0)
    s.shutdown()

    assert s._thread is not None
    assert not s._thread.is_alive()


def test_load_and_warmup_called_on_start(states):
    engine = FakeEngine()
    audio = FakeAudio()
    s = Speaker(
        on_state_change=states.append,
        engine=engine,
        audio=audio,
        capture_text=lambda: None,
    )
    s.start()
    _wait_for_state(s, State.IDLE, timeout=1.0)
    assert engine.load_called
    assert engine.warmup_called
    s.shutdown()
