import pyglet
import resources
from constants import  (MAP_DISPLAY_WIDTH, MAP_DISPLAY_HEIGHT, UI_PANEL_WIDTH,
                        DRAW_X, DRAW_Y, SCROLL_MARGIN, SCROLL_SPEED, WRAP_X, WRAP_Y,
                        MAP_ROW_COUNT, MAP_COL_COUNT)
from util import isEven, mapLocToPixelPos
from definitions import DiagDir, Terrain, Feature, UnitType, HexDir, SpriteType
from tilesprite import TileSprite

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
        self.selected_unit_tile = None
        self.unit_sprites = []
        self.to_draw_path = False
        self.path_list = list() #positions of unit move path
        self.move_labels = list()

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

        self.selection_sprite = pyglet.sprite.Sprite(
            img = resources.selection_image,
            batch=self.batch,
            group=self.ui_group
        )
        self.selection_sprite.x = -9999

        pyglet.gl.glLineWidth(2)

    def initializeCamera(self, center_tile=None):
        self.clearAllSprites()
    
        if not center_tile:
            center_tile = self.map.start_tile
    
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
                
        self.move_labels = self.createMoveLabels()

    def changeZoom(self, zoom_mod):
        self.camera_zoom += zoom_mod

        for spr in self.draw_list:
            spr.scale = self.camera_zoom


    def drawPaths(self):
        if len(self.path_list) == 0:
            return

        path_start = self.path_list[0]

        for path_end in self.path_list[1:]:
            start_pix_pos = mapLocToPixelPos(path_start, self.camera_zoom)
            start_pix_pos[0] -= self.cam_pos[0]
            start_pix_pos[1] += self.cam_pos[1]

            end_pix_pos = mapLocToPixelPos(path_end, self.camera_zoom)
            end_pix_pos[0] -= self.cam_pos[0]
            end_pix_pos[1] += self.cam_pos[1]

            pyglet.graphics.draw(
                    2, pyglet.gl.GL_LINES,
                    ('v2f',
                        (start_pix_pos[0] , start_pix_pos[1],
                        end_pix_pos[0], end_pix_pos[1],
                        )))

            path_start = path_end

        if self.move_labels:
            for label in self.move_labels:
                label.draw()

    def createMoveLabels(self):
        if not self.selected_unit_tile:
            return
        units = self.selected_unit_tile.unit_list
        if len(units) == 0:
            return

        group_moves_left = units[0].moves_left
        group_move_speed = units[0].move_speed

        for unit in units[1:]:
            if unit.moves_left < group_moves_left:
                group_moves_left = unit.moves_left
            if unit.move_speed < group_move_speed:
                group_move_speed = unit.move_speed

        start_pos = units[0].map_idx
        group_path = units[0].move_list

        if group_moves_left > 0:
            turn_count = 0
        else:
            turn_count = 1

        label_list = list()

        group_moves = group_move_speed
        for tile_pos in group_path[1:]:


            next_tile = self.map.tileAt(tile_pos)
            tile_cost = next_tile.move_cost
            group_moves -= tile_cost

            if group_moves <= 0:
                group_moves = group_move_speed
                #draw a turn label here
                label_pix_pos = mapLocToPixelPos(tile_pos, self.camera_zoom)
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
            elif tile_pos == group_path[-1]:
                label_pix_pos = mapLocToPixelPos(tile_pos, self.camera_zoom)
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

    def moveUnit(self, unit, start_tile, end_tile):
        start_pos = start_tile.getMapPos()
        next_tile = end_tile

        if start_tile.getMapPos() == end_tile.getMapPos():
            return

        unit_sprite = None
        sprite_found = False
        for spr in self.draw_list:
            if (spr.sprite_type == SpriteType.UNIT
            and spr.map_pos[0] == start_pos[0]
            and spr.map_pos[1] == start_pos[1]):
                spr.moveToMapIdx(next_tile.pos)
                spr.x = next_tile.abs_pixel_pos[0] - self.cam_pos[0]
                spr.y = next_tile.abs_pixel_pos[1] + self.cam_pos[1]
                sprite_found = True
                break


        """
        This is re-adding any unit sprite that had been trimmed from being offscreen
        as soon as it moves.
        TODO: Check if the unit moved onto a tile within current camera view
        """
        if not sprite_found:
            unit_sprite = TileSprite(   map_pos = next_tile.getMapPos(),
                                        sprite_type = SpriteType.UNIT,
                                        img = next_tile.unitImg(),
                                        batch = self.batch,
                                        group = self.unit_group)
            pos = next_tile.getPixelPos(self.camera_zoom)
            unit_sprite.x = pos[0] - self.cam_pos[0]
            unit_sprite.y = pos[1] + self.cam_pos[1]
            if next_tile.unit_list[0].unit_type == UnitType.SETTLER: #TODO: multiple units
                unit_sprite.scale = 0.8

            self.draw_list.append(unit_sprite)
            self.unit_sprites.append(unit_sprite)

        start_tile = self.map.tileAt(start_pos)
        start_tile.unit_list = list()



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



        #adjust sprite positions to match camera
        for sprite in self.draw_list:
            sprite.x = sprite.pix_pos[0] - self.cam_pos[0]
            sprite.y = sprite.pix_pos[1] + self.cam_pos[1]

        self.selection_sprite.x -= dx
        self.selection_sprite.y -= dy

        if self.move_labels:
            for label in self.move_labels:
                label.x -= dx
                label.y -= dy

        return True

    def addDrawRow(self, row_idx):
        map_row = self.map.row( row_idx,
                                start_col=self.cam_idx[0],
                                end_col=self.cam_idx[0]+DRAW_X)

        for tile in map_row:
            self.addTileSprites(tile)

    def addDrawColumn(self, col_idx):
        if verbose:
            print("addDrawColumn(col_idx="+str(col_idx)+")")
            print(" draw_list len: " + str(len(self.draw_list)))
            print(" rows added: " + str(self.cam_idx[1]) + " - " + str(self.cam_idx[1]+DRAW_Y))
        map_col = self.map.column(  col_idx,
                                    start_row=self.cam_idx[1],
                                    end_row=self.cam_idx[1]+DRAW_Y)
        if verbose:
            print(" new col len: " + str(len(map_col)))

        #if column didn't find anything, nothing will be added
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

        if tile.hasUnit():
            unit_sprite = TileSprite(   map_pos = tile.getMapPos(),
                                        sprite_type = SpriteType.UNIT,
                                        img = tile.unitImg(),
                                        batch = self.batch,
                                        group = self.unit_group)
            pos = tile.getPixelPos(self.camera_zoom)
            unit_sprite.x = pos[0] - self.cam_pos[0]
            unit_sprite.y = pos[1] + self.cam_pos[1]
            if tile.unit_list[0].unit_type == UnitType.SETTLER: #TODO: multiple units
                unit_sprite.scale = 0.8

            self.draw_list.append(unit_sprite)
            self.unit_sprites.append(unit_sprite)
            
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
        if verbose:
            print ("removeDrawColumn:(col_idx="+str(col)+")")
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

    #draws a path from the tile in the HexDir dir
    def drawPathInDirection(self, tile, dir):
        if not tile:
            return
        dst_tile_idx = self.map.neighborAt(tile.pos, HexDir.UR)
        dst_pix_pos = self.map.tileAt(dst_tile_idx).getPixelPos(self.camera_zoom)

        src_pix_pos = tile.getPixelPos(self.camera_zoom)
        self.path_start_pos[0] = src_pix_pos[0] - self.cam_pos[0]
        self.path_start_pos[1] = src_pix_pos[1] + self.cam_pos[1]

        self.path_end_pos[0] = dst_pix_pos[0] - self.cam_pos[0]
        self.path_end_pos[1] = dst_pix_pos[1] + self.cam_pos[1]

    #updates display for new turn
    def drawNewTurn(self):
        self.selected_unit_tile = None
        self.path_list = list()
        self.move_labels = list()
        self.selection_sprite.x = 99999
        self.selection_sprite.y = 99999

    def updateActiveTile(self, mx,my):
        self.scroll_dir = determine_scroll_dir(mx,my)
        self.active_tile = self.determineClosestTile(mx,my)
        return self.active_tile

    def stopScroll(self):
        self.scroll_dir = DiagDir.NONE

    def pathFromSelectedToActiveTile(self):
        if not self.selected_unit_tile:
            return

        self.path_list = self.map.determineShortestLandPath(self.selected_unit_tile, self.active_tile)
        if len(self.path_list) >0:
            for unit in self.selected_unit_tile.unit_list:
                unit.setMovePath(self.path_list)
            self.move_labels = self.createMoveLabels()

    def dragPathFromSelectedToActiveTile(self):
        #Check if moused over (active) tile is different than the
        #previous end of path
        if self.selected_unit_tile:
            if len(self.path_list) == 0 or self.active_tile.pos != self.path_list[-1]:
                self.pathFromSelectedToActiveTile()

    def deselectUnitTile(self):
        self.selected_unit_tile = None
        self.selection_sprite.x = -9999
        del self.path_list[:]

    #either select unit or immediately move existing selected
    def selectUnitOrDestination(self, x,y):
        clicked_tile = self.determineClosestTile(x,y)
        if len(clicked_tile.unit_list) > 0:
            #select the unit
            self.selected_unit_tile = clicked_tile
            self.selection_sprite.x = clicked_tile.abs_pixel_pos[0] - self.cam_pos[0]
            self.selection_sprite.y = clicked_tile.abs_pixel_pos[1] + self.cam_pos[1]

            unit = self.selected_unit_tile.unit_list[0]
            if len(unit.move_list) > 0:
                #draw the existing move list
                self.path_list = unit.move_list
                self.move_labels = self.createMoveLabels()


        elif self.selected_unit_tile and len(self.path_list) > 1:
        #Move selected unit immediately
            tiles = self.map.moveUnit(self.selected_unit_tile.unit_list[0])
            self.moveUnit(self.selected_unit_tile.unit_list[0], tiles[0], tiles[1])


            dst_tile = tiles[1]
            if dst_tile.getMapPos() != self.selected_unit_tile.getMapPos():
            #The unit actually moved
                self.selected_unit_tile = dst_tile
                self.selection_sprite.x = dst_tile.abs_pixel_pos[0] - self.cam_pos[0]
                self.selection_sprite.y = dst_tile.abs_pixel_pos[1] + self.cam_pos[1]

                i=0
                for idx in self.path_list:
                    if idx == dst_tile.getMapPos():
                        break
                    i+=1

                self.path_list = self.path_list[i:]
                self.move_labels = self.move_labels[1:]
                
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