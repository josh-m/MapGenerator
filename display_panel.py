import pyglet.graphics
from constants import MAP_DISPLAY_WIDTH, WINDOW_HEIGHT, UI_PANEL_WIDTH
from definitions import Terrain, Feature, UnitType

class DisplayPanel():
    def __init__(self):
        self.turn_label = UiLabel('Turn: 1', 0)
        self.terrain_label = UiLabel('Terrain: None', 1)
        self.feature_label = UiLabel('Feature: None', 2)
        self.unit_label = UiLabel('Unit: None', 3)
        self.index_label = UiLabel('Index: None', 4)
        self.move_cost_label = UiLabel('Move Cost: None', 5)
        
    def draw(self):
        pyglet.graphics.draw(
                4, pyglet.gl.GL_QUADS,
                ('v2f',
                    (MAP_DISPLAY_WIDTH,WINDOW_HEIGHT,
                    MAP_DISPLAY_WIDTH,0,
                    MAP_DISPLAY_WIDTH+UI_PANEL_WIDTH,0,
                    MAP_DISPLAY_WIDTH+UI_PANEL_WIDTH,WINDOW_HEIGHT
                    )))
        self.turn_label.draw()
        self.terrain_label.draw()
        self.feature_label.draw()
        self.unit_label.draw()
        self.index_label.draw()
        self.move_cost_label.draw()
    
    def updateTileLabels(self, tile):
        if (not tile):
            self.terrain_label.text = 'Terrain: None'
            self.feature_label.text = 'Feature: None'
            self.unit_label.text = 'Unit: None'
            self.index_label.text = 'Index: None'
            self.move_cost_label.text = 'Move Cost: None'
            return
        
        self.updateTerrainLabel(tile.terrain)
        self.updateFeatureLabel(tile.feature)
        if len(tile.unit_list) > 0:
            self.updateUnitLabel(tile.unit_list[0]) #TODO: multiple units
        else:
            self.updateUnitLabel(None)
        self.updateIndexLabel(tile.pos)
        self.updateMoveCostLabel(tile.move_cost)
            
    def updateTerrainLabel(self, terrain):
        if terrain == Terrain.WATER:
            self.terrain_label.text = 'Terrain: Ocean'
        elif terrain == Terrain.GRASS:
            self.terrain_label.text = 'Terrain: Grassland'
        else:
            self.terrain_label.text = 'Terrain: Unknown'
    
    def updateFeatureLabel(self, feature):
        if feature == None:
            self.feature_label.text = 'Feature: None'
        elif feature == Feature.FOREST:
            self.feature_label.text = 'Feature: Forest'
        elif feature == Feature.TOWN:
            self.feature_label.text = 'Feature: Town'
        else:
            self.feature_label.text = 'Feature: Unknown'
            
    def updateUnitLabel(self, unit):
        if unit:
            unit_type = unit.unit_type
        else:
            unit_type = UnitType.NONE
            
        if unit_type == UnitType.NONE:
            self.unit_label.text = 'Unit: None'
        elif unit_type == UnitType.SETTLER:
            self.unit_label.text = 'Unit: Settler'
        else:
            self.unit_label.text = 'Unit: Unknown'
    
    def updateTurnLabel(self, turn):
        self.turn_label.text = "Turn: " + str(turn)
        
    def updateIndexLabel(self, pos):
        self.index_label.text = ("Index: ["
                                + str(pos[0])
                                + ", "
                                + str(pos[1])
                                + "]")
                                
    def updateMoveCostLabel(self, move_cost):
        self.move_cost_label.text = ("Move Cost: "+str(move_cost))
        
class UiLabel(pyglet.text.Label):
    def __init__(self, text, order):
        super(UiLabel, self).__init__(  text, font_name='Arial',
                                        font_size=16, x=MAP_DISPLAY_WIDTH+10,
                                        y=WINDOW_HEIGHT-(order*25),
                                        anchor_x='left', anchor_y='top',
                                        color = (0,0,0,255))