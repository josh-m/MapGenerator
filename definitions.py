from enum import Enum, IntEnum

class Terrain(Enum):
    BLANK = 0
    WATER = 1
    GRASS = 2

class Feature(Enum):
    FOREST = 1
    TOWN = 2

class UiElement(Enum):
    BORDER = 1
    
class UnitType(Enum):
    NONE = 0
    SETTLER = 1
    CIVILIAN = 2

class Behavior(Enum):
    IDLE = 0
    WANDER = 1
    GATHER = 2

class HexDir(IntEnum):
    FIRST=0
    UL=0
    U=1
    UR=2
    DL=3
    D=4
    DR=5
    LENGTH=6

class Dir(Enum):
    NONE=0
    UP=1
    DOWN=2
    LEFT=3
    RIGHT=4

class DiagDir(Enum):
    NONE=0
    UP=1
    DOWN=2
    LEFT=3
    RIGHT=4
    UR=5
    UL=6
    DR=7
    DL=8