import pyglet
import resources
from map.constants import  (MAP_DISPLAY_WIDTH, MAP_DISPLAY_HEIGHT, UI_PANEL_WIDTH,
                        DRAW_X, DRAW_Y, SCROLL_MARGIN, SCROLL_SPEED, WRAP_X, WRAP_Y,
                        MAP_ROW_COUNT, MAP_COL_COUNT)
from map.util import isEven, mapLocToPixelPos
from map.definitions import DiagDir, Terrain, Feature, UnitType, HexDir, SpriteType
from map.tilesprite import TileSprite

import math

#amount of pixels
TILE_THRESHOLD_X = 54
TILE_THRESHOLD_Y = 72
MAX_CAM_POS_X = TILE_THRESHOLD_X*MAP_COL_COUNT - MAP_DISPLAY_WIDTH + TILE_THRESHOLD_X/2
MAX_CAM_POS_Y = TILE_THRESHOLD_Y*MAP_ROW_COUNT - MAP_DISPLAY_HEIGHT + TILE_THRESHOLD_Y/2

verbose = False

class MapDisplay():
    def __init__(self, map):
        self.map = map
        self.active_tile = None

        self.__initializeGraphics()
        self.initializeCamera()

    def __initializeGraphics(self):
        self.batch = pyglet.graphics.Batch()
        self.terrain_group = pyglet.graphics.OrderedGroup(0)
        self.border_group = pyglet.graphics.OrderedGroup(1)
        self.feature_group = pyglet.graphics.OrderedGroup(2)
        self.big_terrain_group = pyglet.graphics.OrderedGroup(3)
        self.unit_group = pyglet.graphics.OrderedGroup(4)
        self.ui_group = pyglet.graphics.OrderedGroup(5)

        self.draw_list = list() #TODO: remove once Tiles are responsible for their own sprites

    def initializeCamera(self, center_tile=None):
        self.clearAllSprites()
    
        if not center_tile:
            center_tile = self.map.tileAt(
                (int(MAP_COL_COUNT/2), int(MAP_ROW_COUNT/2))
            )
    
        self.camera_zoom = 1.0
        self.cam_pos = [0,0]
        self.centerCameraOnTile(center_tile)
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

    def changeZoom(self, zoom_mod):
        self.camera_zoom += zoom_mod

        for spr in self.draw_list:
            spr.scale = self.camera_zoom

    def scroll(self):
        """scroll: scrolls the camera. returns bool whether a scroll occured"""
        if verbose:
            print("cam_pos {}, {}".format(self.cam_pos[0], self.cam_pos[1]))
            print("cam_idx {}, {}".format(self.cam_idx[0], self.cam_idx[1]))
            print("cam_d {}, {}".format(self.cam_dx, self.cam_dy))

        if self.scroll_dir == DiagDir.NONE:
            return False

        dir = self.scroll_dir
        #shift camera position
        dx=0
        dy=0

        if dir==DiagDir.LEFT or dir==DiagDir.UL or dir==DiagDir.DL:
            if WRAP_X or not WRAP_X and not self.cam_pos[0] < 0:
                dx = -SCROLL_SPEED
        elif dir==DiagDir.RIGHT or dir==DiagDir.UR or dir==DiagDir.DR:
            if WRAP_X or not WRAP_X and not self.cam_pos[0] > MAX_CAM_POS_X:
                dx = SCROLL_SPEED

        if dir==DiagDir.UP or dir==DiagDir.UL or dir==DiagDir.UR:
            if WRAP_Y or not WRAP_Y and not self.cam_pos[1] < 0:
                dy = SCROLL_SPEED
        elif dir==DiagDir.DOWN or dir==DiagDir.DR or dir==DiagDir.DL:
            if WRAP_Y or not WRAP_Y and not self.cam_pos[1] > MAX_CAM_POS_Y:
                dy = -SCROLL_SPEED

        self.cam_pos[0] += dx
        self.cam_pos[1] -= dy
        self.cam_dx -= dx
        self.cam_dy -= dy


        #adjust columns and/or rows to be drawn,
        #while updating the camera offsets
        if self.cam_dx > TILE_THRESHOLD_X:
            #shift left
            self.cam_dx -= TILE_THRESHOLD_X

            self.removeDrawColumn(self.cam_idx[0]+DRAW_X-1)

            self.cam_idx[0]-=1
            self.addDrawColumn(self.cam_idx[0])

        elif self.cam_dx < -TILE_THRESHOLD_X:
            #shift right
            self.cam_dx += TILE_THRESHOLD_X

            self.removeDrawColumn(self.cam_idx[0])
            self.cam_idx[0]+=1

            self.addDrawColumn(self.cam_idx[0]+DRAW_X-1)

        if self.cam_dy > TILE_THRESHOLD_Y:
            #shift down
            self.cam_dy -= TILE_THRESHOLD_Y

            self.removeDrawRow(self.cam_idx[1])
            self.cam_idx[1]+=1

            self.addDrawRow(self.cam_idx[1]+DRAW_Y-1)

        elif self.cam_dy < -TILE_THRESHOLD_Y:
            #shift up
            self.cam_dy += TILE_THRESHOLD_Y
            self.removeDrawRow(self.cam_idx[1]+DRAW_Y-1)
            self.cam_idx[1]-=1
            self.addDrawRow(self.cam_idx[1])

        #adjust sprite positions to match camera
        for sprite in self.draw_list:
            sprite.x = sprite.pix_pos[0] - self.cam_pos[0]
            sprite.y = sprite.pix_pos[1] + self.cam_pos[1]

        return True

    def addDrawRow(self, row_idx):
        map_row = self.map.row( row_idx,
                                start_col=self.cam_idx[0],
                                end_col=self.cam_idx[0]+DRAW_X)

        for tile in map_row:
            self.addTileSprites(tile)

    def addDrawColumn(self, col_idx):
        map_col = self.map.column(  col_idx,
                                    start_row=self.cam_idx[1],
                                    end_row=self.cam_idx[1]+DRAW_Y)

        for tile in map_col:
            self.addTileSprites(tile)

    def addTileSprites(self, tile):
        if tile.terrain != None:
            if tile.isMountain():
                batch_group = self.big_terrain_group
            else:
                batch_group = self.terrain_group

            terr_sprite = TileSprite(   map_pos = tile.getMapPos(),
                                        sprite_type = SpriteType.TERRAIN,
                                        img = tile.terrainImg(),
                                        batch = self.batch,
                                        group = batch_group)
            pos = tile.getPixelPos(self.camera_zoom)
            terr_sprite.x = (pos[0] - self.cam_pos[0])
            terr_sprite.y = (pos[1] + self.cam_pos[1])
            self.draw_list.append(terr_sprite)

        if tile.feature != None:
            ftr_sprite = TileSprite(map_pos = tile.getMapPos(),
                                    sprite_type = SpriteType.FEATURE,
                                    img = tile.featureImg(),
                                    batch = self.batch,
                                    group = self.feature_group)
            pos = tile.getPixelPos(self.camera_zoom)
            ftr_sprite.x = pos[0] - self.cam_pos[0]
            ftr_sprite.y = pos[1] + self.cam_pos[1]
            if tile.feature == Feature.FOREST:
                ftr_sprite.scale = 0.8
            self.draw_list.append(ftr_sprite)

        for border in tile.border_sprites:
            border_sprite = TileSprite(map_pos = tile.getMapPos(),
                                    sprite_type = SpriteType.TERRAIN,
                                    img = border,
                                    batch = self.batch,
                                    group = self.border_group)
            border_sprite.x = (pos[0] - self.cam_pos[0])
            border_sprite.y = (pos[1] + self.cam_pos[1])
            self.draw_list.append(border_sprite)


    def removeDrawRow(self, row):
        #Remove sprites from right
        to_remove = list(filter(
                lambda x: isInRow(x, row), self.draw_list))
        self.__removeSprites(to_remove)

    def removeDrawColumn(self, col):
        to_remove = list(filter(
                lambda x: isInColumn(x, col), self.draw_list))
        self.__removeSprites(to_remove)

    def __removeSprites(self, sprites):
        for _sprite in sprites:
            if _sprite is not None:
                _sprite.delete() #immediately removes sprite from video memory
            if _sprite in self.draw_list:
                self.draw_list.remove(_sprite)
            if _sprite.sprite_type == SpriteType.UNIT:
                if _sprite in self.unit_sprites:
                    self.unit_sprites.remove(_sprite)

    def clearAllSprites(self):
        for sprite in self.draw_list:
            sprite.delete()
        
        self.draw_list = []

    def centerCameraOnSprite(self, sprite):
        pos = [0,0]
        pos = mapLocToPixelPos(sprite.map_pos, self.camera_zoom)

        pos[0] -= MAP_DISPLAY_WIDTH/2
        pos[1] = -pos[1]
        #adjust for odd columns
        if not isEven(sprite.map_pos[0]):
            pos[1] += 36
        pos[1] += MAP_DISPLAY_HEIGHT/2

        self.cam_pos = pos
        
        #Determine index of top right tile based on initial camera
        self.cam_idx = pixelPosToMapLoc(self.cam_pos)

        #Adjust the camera to keep map edges offscreen
        if self.cam_idx[0] > 1:
            self.cam_idx[0] -= 2
        if self.cam_idx[1] > 0:
            self.cam_idx[1] -=1

    def centerCameraOnTile(self, tile):
        pos = [0,0]
        pos = tile.getPixelPos(self.camera_zoom)

        pos[0] -= MAP_DISPLAY_WIDTH/2
        pos[1] = -pos[1]
        #adjust for odd columns
        if not isEven(tile.pos[0]):
            pos[1] += 36
        pos[1] += MAP_DISPLAY_HEIGHT/2

        self.cam_pos = pos
        
        #Determine index of top right tile based on initial camera
        self.cam_idx = pixelPosToMapLoc(self.cam_pos)

        #Adjust the camera to keep map edges offscreen
        if self.cam_idx[0] > 1:
            self.cam_idx[0] -= 2
        if self.cam_idx[1] > 0:
            self.cam_idx[1] -=1

    def determineClosestTile(self, mouse_x, mouse_y):
        min_distance = 9999999
        distance = 0.0
        min_sprite = None

        for sprite in self.draw_list:
            distance = math.sqrt( (sprite.x - mouse_x)**2 + (sprite.y - mouse_y)**2)
            if distance < min_distance:
                min_distance = distance
                min_sprite = sprite

        return self.map.tileAt(min_sprite.map_pos)

    def updateActiveTile(self, mx,my):
        self.scroll_dir = determine_scroll_dir(mx,my)
        self.active_tile = self.determineClosestTile(mx,my)
        return self.active_tile

    def stopScroll(self):
        self.scroll_dir = DiagDir.NONE
         
    def mapPosToScreenPos(self, map_pos):
        tile = self.map.tileAt(map_pos)
        pix_pos = tile.getPixelPos()
        
        #camera adjust
        pix_pos[0] -= self.cam_pos[0]
        pix_pos[1] += self.cam_pos[1]
        
        return pix_pos

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

def determine_scroll_dir(mouse_x, mouse_y):
    scroll_dir = DiagDir.NONE

    if mouse_x > MAP_DISPLAY_WIDTH:
        return scroll_dir

    if mouse_x < SCROLL_MARGIN:
        if mouse_y < SCROLL_MARGIN:
            scroll_dir = DiagDir.DL
        elif mouse_y > MAP_DISPLAY_HEIGHT - SCROLL_MARGIN:
            scroll_dir = DiagDir.UL
        else:
            scroll_dir = DiagDir.LEFT
    elif mouse_x > MAP_DISPLAY_WIDTH - SCROLL_MARGIN:
        if mouse_y < SCROLL_MARGIN:
            scroll_dir = DiagDir.DR
        elif mouse_y > MAP_DISPLAY_HEIGHT - SCROLL_MARGIN:
            scroll_dir = DiagDir.UR
        else:
            scroll_dir = DiagDir.RIGHT
    elif mouse_y < SCROLL_MARGIN:
        scroll_dir = DiagDir.DOWN
    elif mouse_y > MAP_DISPLAY_HEIGHT - SCROLL_MARGIN:
        scroll_dir = DiagDir.UP

    return scroll_dir

def isInRow(t_sprite, row):
    if t_sprite.map_pos[1] == (row % MAP_ROW_COUNT):
        return True
    else:
        return False

def isInColumn(t_sprite, column):
    if t_sprite.map_pos[0] == (column % MAP_COL_COUNT):
        return True
    else:
        return False