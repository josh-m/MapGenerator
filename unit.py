import resources
from definitions import UnitType

class Unit():
    def __init__(self):
        self.move_speed = 1
        self.current_moves = self.move_speed
        self.health = 1
        
class Settler(Unit):
    def __init__(self):
        super(Unit, self).__init__()
        self.unit_type = UnitType.SETTLER
        
    def image(self):
        return resources.settler_image