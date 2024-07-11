from dataclasses import dataclass


@dataclass
class Gesture:
    name: str
    index_finger: tuple[int, int]
