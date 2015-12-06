
import pyglet
from pyglet.window import key, mouse


from copy import deepcopy

from definitions import DiagDir, Terrain, Feature, UnitType, HexDir, SpriteType
from constants import  (MAP_DISPLAY_WIDTH, WINDOW_HEIGHT, UI_PANEL_WIDTH,
                        DRAW_X, DRAW_Y, SCROLL_MARGIN, SCROLL_SPEED)
from display_panel import DisplayPanel
from map_display import MapDisplay



class GameWindow(pyglet.window.Window):

    def __init__(self, map, *args, **kwargs):
        super(GameWindow, self).__init__(   MAP_DISPLAY_WIDTH+UI_PANEL_WIDTH,
                                            WINDOW_HEIGHT, *args, **kwargs)
        self.map = map
        self.turn = 1

        #self.__initializeGraphics()
        #self.__initializeCamera()
        self.__initializeUI()
        
        self.map_display = MapDisplay(map)
        self.display_panel = DisplayPanel()
       
        pyglet.clock.schedule_interval(self.update, 1/45.0)

    def on_draw(self):
        self.clear()
        
        self.map_display.batch.draw()
        self.map_display.drawPaths()
        
        self.display_panel.draw()
        if self._show_fps:
            self.fps_display.draw()
        
    def update(self, dt):
        self.map_display.scroll()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.GRAVE:
            self._show_fps = not self._show_fps
        elif symbol == key.SPACE:
            self.turn += 1
            self.display_panel.updateTurnLabel(self.turn)
            
            all_units = self.map.allUnits()
            for unit in all_units:
                unit.restoreMoves()
                self.map_display.moveUnit(unit)
            
            self.map_display.drawNewTurn()

            
    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            self.map_display.pathFromSelectedToActiveTile()
                    
        elif button == mouse.RIGHT:
            self.map_display.deselectUnitTile()
            self.display_panel.updateTileLabels(self.map_display.active_tile)
    
    def on_mouse_drag(self, x,y, dx,dy, buttons, modifiers):
        self.on_mouse_motion(x,y,dx,dy)
    
        if buttons & mouse.LEFT:
            self.map_display.dragPathFromSelectedToActiveTile()
    
    def on_mouse_release(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            self.map_display.selectUnitOrDestination(x,y)
                
    def on_mouse_motion(self,x,y,dx,dy):
        self.map_display.updateActiveTile(x,y)

        self.display_panel.updateTileLabels(self.map_display.active_tile)
            
    def on_mouse_leave(self,x,y):
        self.map_display.stopScroll()
    
    def __initializeUI(self):
        self.fps_display = pyglet.window.FPSDisplay(self)
        self._show_fps = True
             





 