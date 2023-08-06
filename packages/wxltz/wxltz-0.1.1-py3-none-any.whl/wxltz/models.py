from typing import NamedTuple

HSV = NamedTuple("HSV", [("hue", float), ("sat", float), ("vib", float)])


class Proportion(float):
    def __new__(cls, val: float):
        assert 0 <= val <= 1
        return super().__new__(cls, val)
