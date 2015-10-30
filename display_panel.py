import pyglet.graphics
from constants import MAP_DISPLAY_WIDTH, WINDOW_HEIGHT, UI_PANEL_WIDTH
from definitions import Terrain, Feature, UnitType

class DisplayPanel():
    def __init__(self):
        self.turn_label = UiLabel('Turn: 1', 0)
        self.terrain_label = UiLabel('Terrain: None', 1)
        self.feature_label = UiLabel('Feature: None', 2)
        self.unit_label = UiLabel('Unit: None', 3)
        
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
    
    def updateTileLabels(self, tile):
        if (not tile):
            self.terrain_label.text = 'Terrain: None'
            self.feature_label.text = 'Feature: None'
            self.unit_label.text = 'Unit: None'
            return
        
        self.updateTerrainLabel(tile.terrain)
        self.updateFeatureLabel(tile.feature)
        self.updateUnitLabel(tile.unit)
        
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
        if unit == None:
            self.unit_label.text = 'Unit: None'
        elif unit == UnitType.SETTLER:
            self.unit_label.text = 'Unit: Settler'
        else:
            self.unit_label.text = 'Unit: Unknown'
    
    def updateTurnLabel(self, turn):
        self.turn_label.text = "Turn: " + str(turn)
        
class UiLabel(pyglet.text.Label):
    def __init__(self, text, order):
        super(UiLabel, self).__init__(  text, font_name='Arial',
                                        font_size=16, x=MAP_DISPLAY_WIDTH+10,
                                        y=WINDOW_HEIGHT-(order*25),
                                        anchor_x='left', anchor_y='top',
                                        color = (0,0,0,255))