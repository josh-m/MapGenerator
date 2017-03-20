

import pyglet
from pyglet.window import key, mouse


from copy import deepcopy

from definitions import DiagDir, Terrain, Feature, UnitType, HexDir, SpriteType
from constants import  (WINDOW_HEIGHT, MAP_DISPLAY_WIDTH, MAP_DISPLAY_HEIGHT, UI_PANEL_WIDTH,
                        DRAW_X, DRAW_Y, SCROLL_MARGIN, SCROLL_SPEED, WRAP_X, WRAP_Y, MAP_ROW_COUNT)
from display_panel import DisplayPanel
from map_display import MapDisplay


class GameWindow(pyglet.window.Window):

    def __init__(self, map, *args, **kwargs):
        super(GameWindow, self).__init__(   MAP_DISPLAY_WIDTH+UI_PANEL_WIDTH,
                                            MAP_DISPLAY_HEIGHT, *args, **kwargs)
        self.map = map
        self.turn = 1
        
        self.minimap_enabled = True

        self.__initializeUI()

        self.map_display = MapDisplay(map)
        self.display_panel = DisplayPanel()

        pyglet.clock.schedule_interval(self.update, 1/45.0)

        #tracks the current position of the mouse,
        #updated on_mouse_motion
        self.mouse_pos = None

        self.initMiniMap()
        
    def on_draw(self):
        self.clear()

        self.map_display.batch.draw()

        self.display_panel.draw()
        if self._show_fps:
            self.fps_display.draw()
            
        if self.minimap_enabled:
            self.drawMiniMap()

    def update(self, dt):
        if self.map_display.scroll():
            active_tile = self.map_display.updateActiveTile(self.mouse_pos[0], self.mouse_pos[1])
            self.display_panel.updateTileLabels(active_tile)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.GRAVE:
            self._show_fps = not self._show_fps

    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            if x > MAP_DISPLAY_WIDTH:
                if y < MAP_ROW_COUNT:
                    self.moveCameraFromMinimap((x-MAP_DISPLAY_WIDTH, MAP_ROW_COUNT - y))

        elif button == mouse.RIGHT:
            self.display_panel.updateTileLabels(self.map_display.active_tile)

    def on_mouse_drag(self, x,y, dx,dy, buttons, modifiers):
        self.on_mouse_motion(x,y,dx,dy)

    def on_mouse_motion(self,x,y,dx,dy):
        self.mouse_pos = [x,y]
        self.map_display.updateActiveTile(x,y)
        self.display_panel.updateTileLabels(self.map_display.active_tile)

    def on_mouse_leave(self,x,y):
        self.map_display.stopScroll()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.map_display.changeZoom(0.05)

        if scroll_y < 0:
            self.map_display.changeZoom(-0.05)

    def __initializeUI(self):
        self.fps_display = pyglet.window.FPSDisplay(self)
        self._show_fps = True
        
    def moveCameraFromMinimap(self, pos):
        center_tile = self.map.tileAt(pos)
        self.map_display.initializeCamera(center_tile)
        
    def initMiniMap(self):
        self.minimap_vertex_list = pyglet.graphics.vertex_list(len(self.map.allTiles()), 'v2i', 'c3B')
        
        i=0
        j=0

        for tile in self.map.allTiles():
            self.minimap_vertex_list.vertices[i:i+2] = tile.pos[0] + MAP_DISPLAY_WIDTH, MAP_ROW_COUNT - tile.pos[1]
            
            color = (0,0,0)
            if tile.hasUnit():
                color = (255,0,0)
            elif tile.hasForest():
                color = (30,50,5)
            elif tile.terrain == Terrain.WATER:
                color = (0,0,225)
            elif tile.terrain == Terrain.GRASS:
                color = (0,200,0)
            elif tile.terrain == Terrain.SEMI_DRY_GRASS:
                color = (30, 180, 0)
            elif tile.terrain == Terrain.DRY_GRASS:
                color = (130, 150, 0)
            elif tile.terrain ==  Terrain.HILLS:
                color = (150,200,130)
            elif tile.terrain == Terrain.DRY_HILLS:
                color = (120,120,100)
            elif (
            tile.terrain == Terrain.MOUNTAIN or 
            tile.terrain == Terrain.DRY_MOUNTAIN or
            tile.terrain == Terrain.SNOW_MOUNTAIN):
                color = (56,52,47)
            elif tile.terrain ==  Terrain.DESERT:
                color = (255,200,0)
            elif tile.terrain == Terrain.DESERT_HILLS:
                color = (205,160, 0)
            elif tile.terrain == Terrain.SNOW_TUNDRA:
                color = (255,255,255)
            elif tile.terrain == Terrain.SNOW_HILLS:
                color = (220,220,220)
            elif tile.terrain == Terrain.ICE:
                color = (100,190,215)
                
            self.minimap_vertex_list.colors[j:j+3] = color
                
            i += 2
            j += 3
            
    def drawMiniMap(self):
        self.minimap_vertex_list.draw(pyglet.gl.GL_POINTS)
        
        
        left_x = self.map_display.cam_idx[0] + MAP_DISPLAY_WIDTH
        right_x = left_x + DRAW_X
        top_y = MAP_ROW_COUNT - self.map_display.cam_idx[1]
        btm_y = top_y - DRAW_Y
        
        #draw minimap cam position
        pyglet.gl.glLineWidth(1)
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
            ('v2i', (
                left_x, top_y,
                right_x, top_y,
                
                right_x, top_y,
                right_x, btm_y,
                
                right_x,btm_y,
                left_x,btm_y,
                
                left_x,btm_y,
                left_x,top_y
            )),
            ('c3B', (255,255,0) * 8)
        )
