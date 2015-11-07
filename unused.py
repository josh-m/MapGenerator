"""
functions that are currently unused, but may be useful in the future
"""

def isOffscreen(sprite):
    if whereOffscreen(sprite.x, sprite.y) != DiagDir.NONE:
        return True
    else:
        return False

def whereOffscreen(sprite_x, sprite_y):
    off_dir = DiagDir.NONE
    OFF_MARGIN = 36

    if sprite_x < -OFF_MARGIN:
        if sprite_y < -OFF_MARGIN:
            off_dir = DiagDir.DL
        elif sprite_y > WINDOW_HEIGHT + OFF_MARGIN:
            off_dir = DiagDir.UL
        else:
            off_dir = DiagDir.LEFT
    elif sprite_x > MAP_DISPLAY_WIDTH + OFF_MARGIN:
        if sprite_y < -OFF_MARGIN:
            off_dir = DiagDir.DR
        elif sprite_y > WINDOW_HEIGHT + OFF_MARGIN:
            off_dir = DiagDir.UR
        else:
            off_dir = DiagDir.RIGHT
    elif sprite_y < -OFF_MARGIN:
        off_dir = DiagDir.DOWN
    elif sprite_y > WINDOW_HEIGHT + OFF_MARGIN:
        off_dir = DiagDir.UP

    return off_dir
    
    """
    Incomplete functions that were being developed to aid heuristic based pathfinding
    """
    
    #Returns a path of HexDir that constitutes a land path 
    def constructLandPath(self, curr, end):
        path = list()
        curr_tile = curr
        end_idx = end.pos
        
        while curr_tile != end:
            curr_idx = curr_tile.pos

            neighbors = self.neighborsOf(curr_tile)
            neighbors = [tile for tile in neighbors if tile.isEnterableByLandUnit()]
            print(str(len(neighbors)))
            
            next_move = self.nextBestMove(curr_tile, end, neighbors)
            
            if next_move:
                print("constructLandPath: next_move found!") 
                path.append(next_move)
                curr_tile = self.neighborAt(curr_tile.pos, next_move)
            else:
                #path not found
                return
        
        return
    
    #Returns the best found HexDir to reach the goal that
    #is a possible move given the current tile's neighbors
    def nextBestMove(self, curr, end, neighbors):
        gen_direction = self.directionTo(curr, end)
        
        direction_queue = Queue()
        self.constructDirectionQueue(curr, end, direction_queue)
        if direction_queue.empty():
            print("nextBestMove: queue populated!")
        else:
            print("nextBestMove: queue empty! :(")
        
        found = False
        
        while not direction_queue.empty():
            direction = direction_queue.get()
            if self.neighborAt(curr.pos, direction) in neighbors:
                return direction
        
        return None
    
    #Returns a queue of HexDir that constitutes a descending
    #list of desired directions to move in to reach the end tile.
    def constructDirectionQueue(self, curr, end, direction_queue):
        desired_direction = self.directionTo(curr, end)
        
        if desired_direction == HexDir.U:
            direction_queue.put(HexDir.U)
            direction_queue.put(HexDir.UL)
            direction_queue.put(HexDir.UR)
            direction_queue.put(HexDir.DL)
            direction_queue.put(HexDir.DR)
            direction_queue.put(HexDir.D)
        elif desired_direction == HexDir.D:
            direction_queue.put(HexDir.D)
            direction_queue.put(HexDir.DL)
            direction_queue.put(HexDir.DR)
            direction_queue.put(HexDir.UL)
            direction_queue.put(HexDir.UR)
            direction_queue.put(HexDir.U)
        elif desired_direction == HexDir.UL:
            direction_queue.put(HexDir.UL)
            direction_queue.put(HexDir.U)
            direction_queue.put(HexDir.UR)
            direction_queue.put(HexDir.DL)
            direction_queue.put(HexDir.DR)
        elif desired_direction == HexDir.DL:
            direction_queue.put(HexDir.DL)
            direction_queue.put(HexDir.D)
            direction_queue.put(HexDir.UL)
            direction_queue.put(HexDir.U)
            direction_queue.put(HexDir.DR)
            direction_queue.put(HexDir.UR)
        elif desired_direction == HexDir.UR:
            direction_queue.put(HexDir.UR)
            direction_queue.put(HexDir.U)
            direction_queue.put(HexDir.DR)
            direction_queue.put(HexDir.UL)
            direction_queue.put(HexDir.DR)
            direction_queue.put(HexDir.DL)        
        elif desired_direction == HexDir.DR:
            direction_queue.put(HexDir.DR)
            direction_queue.put(HexDir.D)
            direction_queue.put(HexDir.UR)
            direction_queue.put(HexDir.DL)
            direction_queue.put(HexDir.UR)
            direction_queue.put(HexDir.UL)        

        if not direction_queue.empty():
            print("ConstructDirQueue: queue populated!")
        else:
            print("ConstructDirQueue: queue empty!")
            
        return
        
    #Returns the HexDir that describes the general direction from start to end
    def directionTo(self, start, end):
        start_x = start.pos[0]
        start_y = start.pos[1]
        end_x = start.pos[0]
        end_y = start.pos[1]
        dir = None
        
        if start_x == end_x:
            if start_y < end_y:
                return HexDir.U
            else:
                return HexDir.D
        
        if start_x < end_x:
            if isEven(start_x):
                if end_y <= start_y:
                    return HexDir.UR
                else:
                    return HexDir.DR
            else:
                if end_y < start_y:
                    return HexDir.UR
                else:
                    return HexDir.DR
        else:
            if isEven(start_x):
                if end_y <= start_y:
                    return HexDir.UL
                else:
                    return HexDir.DL
            else:
                if end_y < start_y:
                    return HexDir.UL
                else:
                    return HexDir.DL 
