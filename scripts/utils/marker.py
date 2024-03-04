from enum import Enum
from .constants import *

class MarkerType(Enum):
    OBJECT = OBJECT_COLOR
    UNCERTAIN = UNCERTAIN_COLOR
    BACKGROUND = BACKGROUND_COLOR

class Marker():
    def __init__(self, x, y, type, size = 5.0):
        self.x = x
        self.y = y
        self.type = type
        self.color = type.value
        self.size = size

    def __str__(self):
        str_marker = f"({self.x}, {self.y}, {self.type}), {self.color}, {self.size} "
        return str_marker