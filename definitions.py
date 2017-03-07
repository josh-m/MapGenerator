from enum import Enum, IntEnum

class Terrain(Enum):
    BLANK = 0
    WATER = 1
    ICE = 2
    GRASS = 10
    SEMI_DRY_GRASS = 11
    DRY_GRASS = 12
    DESERT = 13
    SNOW_TUNDRA = 14
    HILLS = 20
    SNOW_HILLS = 21
    DRY_HILLS = 22
    DESERT_HILLS = 23
    MOUNTAIN = 30
    DRY_MOUNTAIN = 31
    SNOW_MOUNTAIN = 32



class Feature(Enum):
    FOREST = 1
    PINE = 2
    RAINFOREST = 3
    JUNGLE = 4
    SAVANNA = 5
    PALM = 6
    TOWN = 20

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
    
class SpriteType(Enum):
    TERRAIN = 1
    FEATURE = 2
    UNIT = 3

class HexDir(IntEnum):
    FIRST = 0
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