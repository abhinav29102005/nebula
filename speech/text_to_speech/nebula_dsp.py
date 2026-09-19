"""
speech/text_to_speech/nebula_dsp.py – Marvel's Nebula Voice DSP Filter
======================================================================
Recreates the cybernetic vocal processing for Karen Gillan's Nebula:
1. Slight pitch modulation for synthetic tightness
2. Standard pacing
3. Crisp high-frequency shelf for robotic clarity
4. Short metallic comb filtering (cyborg chassis reflection)
5. Warm analog tape soft-saturation (tanh) and peak-safe normalization
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy import signal

@dataclass
class NebulaAudioChunk:
    audio_float_array: np.ndarray
    sample_rate: int
    sample_channels: int = 1


def apply_nebula_voice_effect(
    audio: np.ndarray,
    sample_rate: int = 22050,
    pitch_factor: float = 1.05,
    comb_feedback: float = 0.45,
    comb_delay_ms: float = 2.5,
    high_shelf_gain: float = 0.35,
    saturation_drive: float = 1.15,
) -> np.ndarray:
    """
    Transform a raw voice audio signal into the unmistakable cyborg Nebula voice from Marvel.
    """
    if len(audio) == 0:
        return audio

    x = audio.astype(np.float32)

    # 1. Pitch Shift Up slightly for a tighter synthetic feel
    target_length = max(1, int(len(x) / pitch_factor))
    x_pitched = signal.resample(x, target_length)

    # 2. High-frequency Shelf (Crisp robotic clarity)
    nyquist = sample_rate / 2.0
    cutoff = min(3000.0 / nyquist, 0.95)
    sos_high = signal.iirfilter(2, cutoff, btype='highpass', output='sos')
    high_component = signal.sosfilt(sos_high, x_pitched) * high_shelf_gain

    # 3. Metallic Comb Filter (Cyborg chassis acoustic resonance)
    delay_samples = max(1, int((comb_delay_ms / 1000.0) * sample_rate))
    b = np.zeros(1, dtype=np.float32)
    b[0] = 1.0
    a = np.zeros(delay_samples + 1, dtype=np.float32)
    a[0] = 1.0
    a[-1] = -comb_feedback
    comb = signal.lfilter(b, a, x_pitched).astype(np.float32)

    # 4. Composite Mix: dry body + metallic reflection + crisp highs
    mixed = (x_pitched * 0.65) + (comb * 0.35) + high_component

    # 5. Warm Analog Tape Saturation (non-linear soft clipping via tanh)
    saturated = np.tanh(mixed * saturation_drive)

    # Peak normalization to prevent digital distortion
    peak = np.max(np.abs(saturated))
    if peak > 1e-4:
        saturated = saturated * (0.92 / peak)

    return saturated.astype(np.float32)
