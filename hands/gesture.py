import enum
from dataclasses import dataclass


class GestureName(enum.Enum):
    NoGesture = 0
    Double = 1
    Triple = 2


@dataclass
class Gesture:
    name: GestureName
    index_finger: tuple[int, int]
