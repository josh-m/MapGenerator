import pyglet
import random, math
import pickle

from map import Map
from gamewindow import GameWindow



"""
The Game class controls the UI, and acts as a controller
for the game map and window.
"""
class Game():
        
    def __init__(self):
        map = None
        
        try:
            map_file = open("save.map", "rb")
            map = pickle.load(map_file)
        except FileNotFoundError:
            map = Map()
            
        window = GameWindow(map)
