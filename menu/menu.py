from threading import Thread

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import mainthread


from map.map import Map

class MenuScreen(Screen):
    map_preview = ObjectProperty(None)
    gen_map_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
        self.active_map_file = None
        
    def loadMap(self, text):
        print('menuscreen.loadMap!')
        
        img_fname = text + '.png' 
        
        self.map_preview.source = img_fname

    def generateMap(self):
        self.gen_map_btn.text = 'Generating New Map...'
        self.gen_map_btn.disabled = True
        
        Thread(target = self.updateMap, daemon = True).start()
    
    def mapGen(self):
        map = Map()
        
        map.saveMinimapPng()

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
        
