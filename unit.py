import resources
from definitions import UnitType
from copy import deepcopy

class Unit():
    def __init__(self, pos):
        self.move_speed = 1
        self.moves_left = self.move_speed
        self.health = 1
        self.move_list = list()
        
        self.map_idx = pos
        
        self.is_moving = False
        
    def restoreMoves(self):
        self.moves_left = self.move_speed
        
    def setMovePath(self, path_list):
        self.move_list = deepcopy(path_list)
    
    def setMapIdx(self, idx):
        self.map_idx = idx
        
class Settler(Unit):
    def __init__(self, *args, **kwargs):
        super(Settler, self).__init__(*args, **kwargs)
        self.unit_type = UnitType.SETTLER
        self.move_speed = 2
        self.moves_left = self.move_speed
        
    def image(self):
        return resources.settler_image
        
class Wolf(Unit):
    def __init__(self, *args, **kwargs):
        super(Settler, self).__init__(*args, **kwargs)
        self.unit_type = UnitType.WOLF
        self.move_speed = 1
        self.moves_left = self.move_speed
        
    def image(self):
        return resources.wolf_image