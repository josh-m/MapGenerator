import pyglet
import random, math

from map import Map
from gamewindow import GameWindow

"""
The Game class controls the UI, and acts as a controller
for the game map and window.
"""
class Game():
        
    def __init__(self):
        map = Map()
        window = GameWindow(map)