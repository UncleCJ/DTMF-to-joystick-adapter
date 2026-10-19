from typing import Iterator
from collections.abc import Sequence
from math import pi as π, sin
from itertools import islice, count
from random import randrange

from Goertzel import GoertzelDetector

# https://en.wikipedia.org/wiki/DTMF_signaling
class DTMFDetector:
    _row_detectors: tuple[GoertzelDetector, ...]
    _column_detectors: tuple[GoertzelDetector, ...]

    def __init__(self, 
                 f_sampling: float,
                 samples_per_window: int) -> None:
        def create_detectors(fs : Sequence[float]) -> tuple[GoertzelDetector, ...]:
            return tuple(
                GoertzelDetector(f_sampling, f_target, samples_per_window)
                for f_target in fs)

        f_rows = (697.0, 770.0, 852.0, 941.0)
        f_columns = (1209.0, 1336.0, 1477.0)
        self._row_detectors = create_detectors(f_rows)
        self._column_detectors = create_detectors(f_columns)
    
    def process_sample(self, s: int) -> None:
        for detector in self._row_detectors + self._column_detectors:
            detector.process_sample(s)

    def detect(self) -> str:
        def detect_list(detectors : Sequence[GoertzelDetector]) -> tuple[float, ...]:
            return tuple(detector.detect() for detector in detectors)
            
        def calculate_density(powers : Sequence[float], p_total : float) -> tuple[int, ...]:
            return tuple(int(100*p/p_total) for p in powers)

        def detectable_frequency(ρs : Sequence[int], τ : int = 15) -> int:
            above_τ : Sequence[bool] = tuple(ρ >= τ for ρ in ρs)
            detectable_fs : Sequence[int] = tuple(
                i for i, e
                in enumerate(above_τ) 
                if e == True)
            if len(detectable_fs) != 1:
                raise ValueError(f'No single detectable frequency above threshold {τ} for powers {ρs}')
            return detectable_fs[0]
        
        def coord_to_key(i_row : int, i_col : int) -> str:
            return (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9"), ("*", "0", "#"))[i_row][i_col]

        p_rows : Sequence[float] = detect_list(self._row_detectors)
        p_columns : Sequence[float] = detect_list(self._column_detectors)
        # print(p_rows + p_columns)
        p_total : float = sum(p_rows + p_columns)
        ρ_rows : Sequence[int] = calculate_density(p_rows, p_total)
        ρ_columns : Sequence[int] = calculate_density(p_columns, p_total)
        # print(ρ_rows + ρ_columns)
        return coord_to_key(
            detectable_frequency(ρ_rows),
            detectable_frequency(ρ_columns))


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