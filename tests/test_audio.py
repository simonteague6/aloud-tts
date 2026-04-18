import threading
import time
from pathlib import Path

from tts_app.core.audio import AudioPlayer


def test_play_then_stop_terminates_quickly(long_wav: Path):
    player = AudioPlayer()
    player.play(long_wav)
    assert player.is_playing()

    t0 = time.time()
    player.stop()
    elapsed = time.time() - t0

    assert not player.is_playing()
    assert elapsed < 0.6  # stop() must terminate well within 500ms timeout


def test_wait_returns_after_playback_finishes(short_wav: Path):
    player = AudioPlayer()
    player.play(short_wav)
    player.wait()
    assert not player.is_playing()


def test_wait_honors_stop_event(long_wav: Path):
    player = AudioPlayer()
    player.play(long_wav)

    stop_event = threading.Event()
    threading.Timer(0.1, stop_event.set).start()

    t0 = time.time()
    player.wait(stop_event)
    elapsed = time.time() - t0

    assert not player.is_playing()
    assert elapsed < 0.5


def test_play_replaces_current_playback(long_wav: Path, short_wav: Path):
    player = AudioPlayer()
    player.play(long_wav)
    first_proc = player._proc
    player.play(short_wav)
    assert player._proc is not first_proc
    player.stop()


def test_stop_is_noop_when_idle():
    player = AudioPlayer()
    player.stop()  # should not raise
    assert not player.is_playing()
