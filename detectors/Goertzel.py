from math import pi as π, cos, sin, pow, sqrt
from collections.abc import Iterator
from itertools import islice, count
from random import randrange

# https://en.wikipedia.org/wiki/Goertzel_algorithm
class GoertzelDetector:
    _sin_ω : float
    _cos_ω : float
    _C : float
    _Q1 : float = 0.0
    _Q2 : float = 0.0

    def __init__(self, 
                 f_sampling: float,
                 f_target: float,
                 samples_per_window: int) -> None:
        n : float = float(samples_per_window)
        k : int = int(n * f_target / f_sampling + 0.93)
        ω : float = 2.0 * π * k / n
        self._sin_ω = sin(ω)
        self._cos_ω = cos(ω)
        self._C = 2.0 * self._cos_ω

    def process_sample(self, s: int) -> None:
        self._Q1, self._Q2 = (self._C * self._Q1 - self._Q2 + float(s),
                              self._Q1)

    def detect(self) -> float:
        def complex_results() -> tuple[float, float]:
            return (self._Q1 - self._Q2 * self._cos_ω,
                    self._Q2 * self._sin_ω)

        def reset() -> None:
            self._Q1, self._Q2 = (0.0, 0.0)
        
        Q_R, Q_I = complex_results()
        result : float = sqrt(pow(Q_R, 2)+pow(Q_I, 2))
        reset()
        return result

if __name__ == "__main__":
    def tone_generator(f_sampling: float, f_tone: float, amplitude: int) -> Iterator[int]:
        return map(lambda i:int(amplitude * sin(2 * π * f_tone * i / f_sampling)), count())

    def random_generator(amplitude: int) -> Iterator[int]:
        while True:
            yield randrange(-amplitude, amplitude)
    
    f_sampling: float = 5.0e3
    samples_per_window: int = 1000

    dtmf_frequencies = (697.0, 770.0, 852.0, 941.0, 1209.0, 1336.0, 1477.0)
    dtmf_detectors = tuple(GoertzelDetector(f_sampling, f_target, samples_per_window)
        for f_target in dtmf_frequencies)

    for ts in islice(
            zip(tone_generator(f_sampling, 852.0, 100), 
                tone_generator(f_sampling, 852.0+30.0, 50), 
                tone_generator(f_sampling, 1477.0, 100),
                random_generator(100)),
            samples_per_window):
        x : int = sum(ts)
        for detector in dtmf_detectors:
            detector.process_sample(x)
    
    dtmf_powers = tuple(detector.detect() for detector in dtmf_detectors)
    for f_target, p in zip(dtmf_frequencies, dtmf_powers):
        print(f'{int(f_target)}: {int(100*p/sum(dtmf_powers))}%')