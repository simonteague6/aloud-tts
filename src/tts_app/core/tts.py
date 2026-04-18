import threading
from pathlib import Path

import numpy as np
import soundfile as sf

from tts_app import config


class GenerationCancelled(Exception):
    pass


class TTSEngine:
    def __init__(self) -> None:
        self._model = None

    def load(self) -> None:
        if self._model is not None:
            return
        from mlx_audio.tts import load

        self._model = load(config.MODEL)

    def unload(self) -> None:
        self._model = None

    def is_loaded(self) -> bool:
        return self._model is not None

    def generate(
        self,
        text: str,
        out: Path,
        cancel: threading.Event | None = None,
    ) -> Path:
        if self._model is None:
            self.load()

        segments = []
        for result in self._model.generate(
            text,
            voice=config.VOICE,
            speed=config.SPEED,
            lang_code=config.LANG_CODE,
        ):
            if cancel is not None and cancel.is_set():
                raise GenerationCancelled
            segments.append(np.array(result.audio))

        audio = np.concatenate(segments)
        tmp = out.with_suffix(out.suffix + ".tmp")
        sf.write(str(tmp), audio, samplerate=config.SAMPLE_RATE, format="WAV")
        tmp.replace(out)
        return out

    def warmup(self) -> None:
        self.generate(".", config.WAV_PATH.with_name("tts_app_warmup.wav"))
