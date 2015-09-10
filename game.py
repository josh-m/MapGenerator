import pyglet
import random, math

from map import Map
from gamewindow import GameWindow

class Game():

    def __init__(self):
        map = Map()
        window = GameWindow(map)