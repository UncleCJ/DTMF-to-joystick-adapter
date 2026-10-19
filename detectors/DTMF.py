from typing import Iterator, Final
from collections.abc import Sequence
from math import pi as π, sin
from itertools import islice, count
from random import randrange

from Goertzel import GoertzelDetector

# https://en.wikipedia.org/wiki/DTMF_signaling
class DTMFDetector:
    _ROW_FREQUENCIES : Final[tuple[float, ...]] = (697.0, 770.0, 852.0, 941.0)
    _COLUMN_FREQUENCIES : Final[tuple[float, ...]] = (1209.0, 1336.0, 1477.0)
    _BASIC_KEY_MATRIX : Final[tuple[tuple[str, ...], ...]] = (
        ("1", "2", "3"), 
        ("4", "5", "6"), 
        ("7", "8", "9"), 
        ("*", "0", "#"))
    
    _detectors : tuple[GoertzelDetector, ...]

    def __init__(self, 
                 f_sampling: float = 5.0e3,
                 samples_per_window: int = 1000) -> None:
        self._detectors = tuple(
            GoertzelDetector(f_sampling, f_target, samples_per_window)
            for f_target in self._ROW_FREQUENCIES + self._COLUMN_FREQUENCIES)
    
    def process_sample(self, s: int) -> None:
        for detector in self._detectors:
            detector.process_sample(s)

    def detect(self) -> str:
        def detectable_frequency(tone_group_densities : Sequence[int], percentage_threshold : int = 15) -> int:
            detectable_fs : Sequence[int] = tuple(
                tone_index
                for tone_index, is_above_threshold
                in enumerate(
                    tone_density >= percentage_threshold
                    for tone_density in tone_group_densities)
                if is_above_threshold == True)
            if len(detectable_fs) != 1:
                raise ValueError(f'No single detectable frequency above threshold {percentage_threshold} for powers {tone_group_densities}')
            return detectable_fs[0]
        
        def coord_to_key(row_tone_index : int, column_tone_index : int) -> str:
            return self._BASIC_KEY_MATRIX[row_tone_index][column_tone_index]

        tone_powers : Sequence[float] = tuple(detector.detect() for detector in self._detectors)
        total_power : float = sum(tone_powers)
        tone_densities : Sequence[int] = tuple(
            int(100*tone_power/total_power)
            for tone_power in tone_powers)
        return coord_to_key(
            detectable_frequency(tone_densities[:len(self._ROW_FREQUENCIES)]),
            detectable_frequency(tone_densities[len(self._ROW_FREQUENCIES):]))


if __name__ == "__main__":
    def tone_generator(f_sampling: float, f_tone: float, amplitude: int) -> Iterator[int]:
        return map(lambda i:int(amplitude * sin(2 * π * f_tone * i / f_sampling)), count())

    def random_generator(amplitude: int) -> Iterator[int]:
        while True:
            yield randrange(-amplitude, amplitude)
    
    f_sampling: float = 5.0e3
    samples_per_window: int = 1000

    dtmf_detector = DTMFDetector(f_sampling, samples_per_window)

    for ts in islice(
            zip(tone_generator(f_sampling, 697.0, 100), 
                tone_generator(f_sampling, 852.0+30.0, 50), 
                tone_generator(f_sampling, 1477.0, 100),
                random_generator(100)),
            samples_per_window):
        x : int = sum(ts)
        dtmf_detector.process_sample(x)
    
    print(dtmf_detector.detect())