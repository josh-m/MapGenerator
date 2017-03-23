#!python3
import pyglet
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from menu.menu import MenuScreen
from map.game import Game

class MapApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen())
        return self.sm
        
def main():
    MapApp().run()
    
def runPygletMap():
    game = Game()
    pyglet.app.run()
    
if __name__ == '__main__':
    main()