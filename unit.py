
class Unit():
	def __init__(self):
		self.move_speed = 1
		self.health = 1
        
class Settler(Unit):
    def __init__(self):
        super(Unit, self).__init__()