from pathlib import Path

import numpy as np
import pytest
import soundfile as sf


@pytest.fixture
def short_wav(tmp_path: Path) -> Path:
    path = tmp_path / "short.wav"
    sf.write(str(path), np.zeros(12000, dtype=np.float32), samplerate=24000, format="WAV")
    return path


@pytest.fixture
def long_wav(tmp_path: Path) -> Path:
    path = tmp_path / "long.wav"
    sf.write(str(path), np.zeros(24000 * 3, dtype=np.float32), samplerate=24000, format="WAV")
    return path
