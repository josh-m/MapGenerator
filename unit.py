import resources
from definitions import UnitType

class Unit():
    def __init__(self):
        self.move_speed = 1
        self.moves_left = self.move_speed
        self.health = 1
        
    def restoreMoves(self):
        self.moves_left = self.move_speed
        
class Settler(Unit):
    def __init__(self):
        super(Settler, self).__init__()
        self.unit_type = UnitType.SETTLER
        self.move_speed = 2
        self.moves_left = self.move_speed
        
    def image(self):
        return resources.settler_image