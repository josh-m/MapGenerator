
import pyglet
from pyglet.window import key, mouse

import math
from copy import deepcopy

from definitions import DiagDir, Terrain, Feature, UnitType, HexDir
from constants import  (MAP_DISPLAY_WIDTH, WINDOW_HEIGHT, UI_PANEL_WIDTH,
                        DRAW_X, DRAW_Y, SCROLL_MARGIN, SCROLL_SPEED)
from util import isEven, mapLocToPixelPos
import resources
from tilesprite import TileSprite
from display_panel import DisplayPanel

#amount of pixels
TILE_THRESHOLD_X = 54
TILE_THRESHOLD_Y = 72

class GameWindow(pyglet.window.Window):

    def __init__(self, map, *args, **kwargs):
        super(GameWindow, self).__init__(   MAP_DISPLAY_WIDTH+UI_PANEL_WIDTH,
                                            WINDOW_HEIGHT, *args, **kwargs)
        self.map = map
        self.turn = 1
        self.active_tile = None
        self.selected_unit_tile = None
        
        self.to_draw_path = False
        self.path_list = list() #positions of unit move path
        self.move_labels = list()
        
        self.__initializeGraphics()
        self.__initializeCamera()
        self.__initializeUI()
        self.display_panel = DisplayPanel()
     
        pyglet.clock.schedule_interval(self.update, 1/45.0)

    def on_draw(self):
        self.clear()
        self.batch.draw()
        if self._show_fps:
            self.fps_display.draw()
        self.__drawPaths()
        self.display_panel.draw()

    def update(self, dt):
        if self.scroll_dir != DiagDir.NONE:
            self.scroll(self.scroll_dir)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.GRAVE:
            self._show_fps = not self._show_fps
        elif symbol == key.SPACE:
            self.turn += 1
            self.display_panel.updateTurnLabel(self.turn)

    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            if self.selected_unit_tile:
                if self.active_tile.isEnterableByLandUnit():
                    self.path_list = self.map.determineShortestLandPath(self.selected_unit_tile, self.active_tile)
                    if len(self.path_list) >0:
                        self.move_labels = self.createMoveLabels()
                    
        elif button == mouse.RIGHT:
            self.selected_unit_tile = None
            self.selection_sprite.x = -9999
            del self.path_list[:]
            self.display_panel.updateTileLabels(self.active_tile)
    
    def on_mouse_drag(self, x,y, dx,dy, buttons, modifiers):
        self.on_mouse_motion(x,y,dx,dy)
    
        if buttons & mouse.LEFT:
            #Check if moused over (active) tile is different than the
            #previous end of path
            if self.selected_unit_tile:
                if len(self.path_list) == 0 or self.active_tile.pos != self.path_list[-1]:
                    self.path_list = self.map.determineShortestLandPath(self.selected_unit_tile, self.active_tile)
                    if len(self.path_list) > 0:
                        self.move_labels = self.createMoveLabels()
    
    def on_mouse_release(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            clicked_tile = self.determineClosestTile(x,y)
            if len(clicked_tile.unit_list) > 0:
                self.selected_unit_tile = clicked_tile
                self.selection_sprite.x = clicked_tile.abs_pixel_pos[0] - self.cam_pos[0]
                self.selection_sprite.y = clicked_tile.abs_pixel_pos[1] + self.cam_pos[1]
        
            elif self.selected_unit_tile and len(self.path_list) > 0:
                #move unit one turn
                pass
            
        
    def on_mouse_motion(self,x,y,dx,dy):
        self.scroll_dir = determine_scroll_dir(x,y)

        self.active_tile = self.determineClosestTile(x,y)
        self.display_panel.updateTileLabels(self.active_tile)
            
    def on_mouse_leave(self,x,y):
        self.scroll_dir = DiagDir.NONE

    def scroll(self, dir):
        #shift camera position
        dx=0
        dy=0

        if dir==DiagDir.LEFT or dir==DiagDir.UL or dir==DiagDir.DL:
            dx = -SCROLL_SPEED
        elif dir==DiagDir.RIGHT or dir==DiagDir.UR or dir==DiagDir.DR:
            dx = SCROLL_SPEED

        if dir==DiagDir.UP or dir==DiagDir.UL or dir==DiagDir.UR:
            dy = SCROLL_SPEED
        elif dir==DiagDir.DOWN or dir==DiagDir.DR or dir==DiagDir.DL:
            dy = -SCROLL_SPEED

        self.cam_pos[0] += dx
        self.cam_pos[1] -= dy
        self.cam_dx -= dx
        self.cam_dy -= dy

        #adjust sprite positions to match camera
        for sprite in self.draw_list:
            sprite.x = sprite.pix_pos[0] - self.cam_pos[0]
            sprite.y = sprite.pix_pos[1] + self.cam_pos[1]
        
        self.selection_sprite.x -= dx
        self.selection_sprite.y -= dy
        
        for label in self.move_labels:
            label.x -= dx
            label.y -= dy
        
        #adjust columns and/or rows to be drawn,
        #while updating the camera offsets
        if self.cam_dx > TILE_THRESHOLD_X:
            #print("shift left")
            self.cam_dx -= TILE_THRESHOLD_X

            self.removeDrawColumn(self.cam_idx[0]+DRAW_X-1)

            self.cam_idx[0]-=1
            self.addDrawColumn(self.cam_idx[0])

        elif self.cam_dx < -TILE_THRESHOLD_X:
            #print("shift right")
            self.cam_dx += TILE_THRESHOLD_X

            self.removeDrawColumn(self.cam_idx[0])
            self.cam_idx[0]+=1

            self.addDrawColumn(self.cam_idx[0]+DRAW_X-1)

        if self.cam_dy > TILE_THRESHOLD_Y:
            #print ("shift down")
            self.cam_dy -= TILE_THRESHOLD_Y

            self.removeDrawRow(self.cam_idx[1])
            self.cam_idx[1]+=1

            self.addDrawRow(self.cam_idx[1]+DRAW_Y-1)

        elif self.cam_dy < -TILE_THRESHOLD_Y:
            #print("shift up")
            self.cam_dy += TILE_THRESHOLD_Y
            self.removeDrawRow(self.cam_idx[1]+DRAW_Y-1)
            self.cam_idx[1]-=1
            self.addDrawRow(self.cam_idx[1])

    def addDrawRow(self, row_idx):
        map_row = self.map.row( row_idx,
                                start_col=self.cam_idx[0],
                                end_col=self.cam_idx[0]+DRAW_X)
        assert(len(map_row) >= DRAW_X)

        for tile in map_row:
            self.addTileSprites(tile)
    
    def addDrawColumn(self, col_idx):
        map_col = self.map.column(  col_idx,
                                    start_row=self.cam_idx[1],
                                    end_row=self.cam_idx[1]+DRAW_Y)
        assert(len(map_col) >= DRAW_Y)

        for tile in map_col:
            self.addTileSprites(tile)
    
    def addTileSprites(self, tile):
        if tile.terrain != None:
            terr_sprite = TileSprite(   map_pos = tile.getMapPos(),
                                        img = tile.terrainImg(),
                                        batch = self.batch,
                                        group = self.terrain_group)
            pos = tile.getAbsolutePixelPos()
            terr_sprite.x = (pos[0] - self.cam_pos[0])
            terr_sprite.y = (pos[1] + self.cam_pos[1])

            self.draw_list.append(terr_sprite)

        if tile.feature != None:
            ftr_sprite = TileSprite( map_pos = tile.getMapPos(),
                                    img = tile.featureImg(),
                                    batch = self.batch,
                                    group = self.feature_group)
            pos = tile.getAbsolutePixelPos()
            ftr_sprite.x = pos[0] - self.cam_pos[0]
            ftr_sprite.y = pos[1] + self.cam_pos[1]
            if tile.feature == Feature.FOREST:
                ftr_sprite.scale = 0.8
            self.draw_list.append(ftr_sprite)
            
        if len(tile.unit_list) > 0:
            unit_sprite = TileSprite( map_pos = tile.getMapPos(),
                                    img = tile.unitImg(),
                                    batch = self.batch,
                                    group = self.unit_group)
            pos = tile.getAbsolutePixelPos()
            unit_sprite.x = pos[0] - self.cam_pos[0]
            unit_sprite.y = pos[1] + self.cam_pos[1]
            if tile.unit_list[0].unit_type == UnitType.SETTLER: #TODO: multiple units
                unit_sprite.scale = 0.8
            self.draw_list.append(unit_sprite)
                
    def removeDrawRow(self, row):
        #Remove sprites from right
        to_remove = list(filter(
                lambda x: isInRow(x, row), self.draw_list))

        for sprite in to_remove:
            self.draw_list.remove(sprite)
            sprite.delete() #immediately removes sprite from video memory

    def removeDrawColumn(self, col):
        to_remove = list(filter(
                lambda x: isInColumn(x, col), self.draw_list))

        for sprite in to_remove:
            self.draw_list.remove(sprite)
            sprite.delete() #immediately removes sprite from video memory
        
    def centerCameraOnSprite(self, sprite):
        pos = [0,0]
        pos = mapLocToPixelPos(sprite.map_pos)

        pos[0] -= MAP_DISPLAY_WIDTH/2
        pos[1] = -pos[1]
        #adjust for odd columns
        if not isEven(sprite.map_pos[0]):
            pos[1] += 36
        pos[1] += WINDOW_HEIGHT/2

        self.cam_pos = pos

    def centerCameraOnTile(self, tile):
        pos = [0,0]
        pos = tile.getAbsolutePixelPos()

        pos[0] -= MAP_DISPLAY_WIDTH/2
        pos[1] = -pos[1]
        #adjust for odd columns
        if not isEven(tile.pos[0]):
            pos[1] += 36
        pos[1] += WINDOW_HEIGHT/2

        self.cam_pos = pos
    
    def determineClosestTile(self, mouse_x, mouse_y):
        min_distance = 9999999
        min_pos = [0,0]
        distance = 0.0
        min_sprite = None

        for sprite in self.draw_list:
            distance = math.sqrt( (sprite.x - mouse_x)**2 + (sprite.y - mouse_y)**2)
            if distance < min_distance:
                min_distance = distance
                min_pos = [sprite.x, sprite.y]
                min_sprite = sprite
                
        return self.map.tileAt(min_sprite.map_pos)
    
    #draws a path from the tile in the HexDir dir
    def drawPathInDirection(self, tile, dir):
        if not tile:   
            return
        dst_tile_idx = self.map.neighborAt(tile.pos, HexDir.UR)
        dst_pix_pos = self.map.tileAt(dst_tile_idx).getAbsolutePixelPos()

        src_pix_pos = tile.getAbsolutePixelPos()
        self.path_start_pos[0] = src_pix_pos[0] - self.cam_pos[0]
        self.path_start_pos[1] = src_pix_pos[1] + self.cam_pos[1]
        
        self.path_end_pos[0] = dst_pix_pos[0] - self.cam_pos[0]
        self.path_end_pos[1] = dst_pix_pos[1] + self.cam_pos[1]
        
    def __initializeGraphics(self):
        self.batch = pyglet.graphics.Batch()
        self.terrain_group = pyglet.graphics.OrderedGroup(0)
        self.feature_group = pyglet.graphics.OrderedGroup(1)
        self.unit_group = pyglet.graphics.OrderedGroup(2)
        self.ui_group = pyglet.graphics.OrderedGroup(3)

        self.draw_list = list() #TODO: remove once Tiles are responsible for their own sprites
        
        self.selection_sprite = pyglet.sprite.Sprite(
            img = resources.selection_image,
            batch=self.batch,
            group=self.ui_group
        )
        self.selection_sprite.x = -9999
        
    def __initializeCamera(self):
        self.cam_pos = [0,0]
        self.centerCameraOnTile(self.map.start_tile)
        self.cam_dx = 0
        self.cam_dy = 0
        self.scroll_dir = DiagDir.NONE
        
        #Determine index of top right tile based on initial camera
        self.cam_idx = pixelPosToMapLoc(self.cam_pos)
        
        #Adjust the camera to keep map edges offscreen
        if self.cam_idx[0] > 1:
            self.cam_idx[0] -= 2
        if self.cam_idx[1] > 0:
            self.cam_idx[1] -=1
            
        #Add sprites within camera to the draw batch
        for i in range(self.cam_idx[0], min(self.cam_idx[0]+DRAW_X, len(self.map.columns))):
            self.addDrawColumn(i)
    
    def __initializeUI(self):
        self.fps_display = pyglet.window.FPSDisplay(self)
        self._show_fps = True
            
    def __drawPaths(self):
        if len(self.path_list) == 0:
            return
            
        path_start = self.path_list[0]

        for path_end in self.path_list[1:]:
            start_pix_pos = mapLocToPixelPos(path_start)
            start_pix_pos[0] -= self.cam_pos[0]
            start_pix_pos[1] += self.cam_pos[1]
            
            end_pix_pos = mapLocToPixelPos(path_end)
            end_pix_pos[0] -= self.cam_pos[0]
            end_pix_pos[1] += self.cam_pos[1]
            
            pyglet.graphics.draw(
                    2, pyglet.gl.GL_LINES,
                    ('v2f',
                        (start_pix_pos[0] , start_pix_pos[1],
                        end_pix_pos[0], end_pix_pos[1],
                        )))
            
            path_start = path_end
            
        for label in self.move_labels:
            label.draw()
                        
    def createMoveLabels(self):
        unit_moves = 2 #TODO: placeholder, replace with unit's speed
        start_pos = self.path_list[0]
        turn_count = 1
        label_list = list()
        
        for tile_pos in self.path_list[1:]:
            next_tile = self.map.tileAt(tile_pos)
            tile_cost = next_tile.move_cost
            unit_moves -= tile_cost
            
            if unit_moves <= 0:
                unit_moves = 2
                #draw a turn label here
                label_pix_pos = mapLocToPixelPos(tile_pos)
                label_x = label_pix_pos[0] - self.cam_pos[0]
                label_y = label_pix_pos[1] + self.cam_pos[1]
                label = pyglet.text.Label(
                    str(turn_count), font_name='Arial',
                    font_size=16, x=label_x,
                    y=label_y,
                    anchor_x='center', anchor_y='center',
                    color = (255,255,0,255)
                )
                label_list.append(label)
                turn_count += 1
            elif tile_pos == self.path_list[-1]:
                label_pix_pos = mapLocToPixelPos(tile_pos)
                label_x = label_pix_pos[0] - self.cam_pos[0]
                label_y = label_pix_pos[1] + self.cam_pos[1]
                label = pyglet.text.Label(
                    str(turn_count), font_name='Arial',
                    font_size=16, x=label_x,
                    y=label_y,
                    anchor_x='center', anchor_y='center',
                    color = (255,255,0,255)
                )
                label_list.append(label)
                break
                    
        return label_list
                     
def isInRow(t_sprite, row):
    if t_sprite.map_pos[1] == row:
        return True
    else:
        return False

def isInColumn(t_sprite, column):
    if t_sprite.map_pos[0] == column:
        return True
    else:
        return False

def determine_scroll_dir(mouse_x, mouse_y):
    scroll_dir = DiagDir.NONE
    
    if mouse_x > MAP_DISPLAY_WIDTH:
        return scroll_dir

    if mouse_x < SCROLL_MARGIN:
        if mouse_y < SCROLL_MARGIN:
            scroll_dir = DiagDir.DL
        elif mouse_y > WINDOW_HEIGHT - SCROLL_MARGIN:
            scroll_dir = DiagDir.UL
        else:
            scroll_dir = DiagDir.LEFT
    elif mouse_x > MAP_DISPLAY_WIDTH - SCROLL_MARGIN:
        if mouse_y < SCROLL_MARGIN:
            scroll_dir = DiagDir.DR
        elif mouse_y > WINDOW_HEIGHT - SCROLL_MARGIN:
            scroll_dir = DiagDir.UR
        else:
            scroll_dir = DiagDir.RIGHT
    elif mouse_y < SCROLL_MARGIN:
        scroll_dir = DiagDir.DOWN
    elif mouse_y > WINDOW_HEIGHT - SCROLL_MARGIN:
        scroll_dir = DiagDir.UP

    return scroll_dir

def pixelPosToMapLoc(pix_pos):
    x_offset = 54
    y_offset = 72
    y_margin = y_offset/2

    col_idx = (pix_pos[0] - 36) / x_offset

    row_idx = pix_pos[1]
    if isEven(col_idx):
        row_idx -= y_margin

    row_idx = row_idx / y_offset

    return [int(col_idx), int(row_idx)]
 