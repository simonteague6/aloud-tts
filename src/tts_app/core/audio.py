import shutil
import subprocess
import threading
import time
from pathlib import Path


class AudioPlayer:
    def __init__(self) -> None:
        if shutil.which("afplay") is None:
            raise RuntimeError("afplay not found on PATH (requires macOS)")
        self._proc: subprocess.Popen | None = None

    def play(self, path: Path) -> None:
        self.stop()
        self._proc = subprocess.Popen(["afplay", str(path)])

    def stop(self) -> None:
        proc = self._proc
        if proc is None or proc.poll() is not None:
            return
        proc.terminate()
        try:
            proc.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=0.5)

    def is_playing(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def wait(self, stop_event: threading.Event | None = None) -> None:
        proc = self._proc
        if proc is None:
            return
        while proc.poll() is None:
            if stop_event is not None and stop_event.is_set():
                self.stop()
                return
            time.sleep(0.05)
