from threading import Thread
import pickle

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.app import App

import pyglet

from map.game import Game
from map.map import Map

class MenuScreen(Screen):
    map_preview = ObjectProperty(None)
    gen_map_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
        self.active_map = None
        
    def loadMap(self, text):
    
        img_fname = 'saves/' + text[:-4] + '.png' 
        
        self.map_preview.source = img_fname
       
        try:
            map_file = open("saves/" + text, "rb")
            self.active_map = pickle.load(map_file)
        except FileNotFoundError:
            print('FileNotFoundError')
        
    def enterMap(self):
        if not self.active_map:
            return
            
        if not self.active_map.visuals_generated:
            self.active_map.generateVisuals()
        game = Game(self.active_map)
        
        window = self.parent.parent
        window.minimize()
        pyglet.app.run()   

    def generateMap(self):
        self.gen_map_btn.text = 'Generating New Map...'
        self.gen_map_btn.disabled = True
        
        Thread(target = self.updateMap, daemon = True).start()
    
    def mapGen(self):
        self.active_map = Map()
        
        self.active_map.saveMinimapPng()
        self.active_map.saveMapData()

    def updateMap(self):
    
        t = Thread(target = self.mapGen)
        t.start()
        t.join()
        
        self.updatePreview()
        
        self.gen_map_btn.text = 'Generate Map'
        self.gen_map_btn.disabled = False
    
    @mainthread
    def updatePreview(self):
        img_fname = 'saves/temp.png'        
        self.map_preview.source = img_fname
        self.map_preview.reload()
        
    def enableFileButtons(self, exc_btn=None):
        pass
        
