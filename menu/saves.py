from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from os import listdir
from os.path import isfile

class SaveDataButton(Button):
    def __init__(self, **kwargs):
        super(SaveDataButton, self).__init__(**kwargs)
        self.bind(on_press = selectMapFile)
        
class SavesData(GridLayout):
    def __init__(self, **kwargs):
        super(SavesData, self).__init__(**kwargs)
        
        files = listdir('saves')
        files = [f for f in files if len(f) > 4 and f[-4:] == '.map']
        
        for filename in files:
            elem= SaveDataButton(
                text = filename
            )
            
            self.add_widget(elem)
        
class SavesScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(SavesScrollView, self).__init__(**kwargs)
        
def selectMapFile(save_button):
    #menu_screen is the 2nd highest level widget
    menu_screen = [w for w in save_button.walk_reverse()][-2]
   
    menu_screen.loadMap(save_button.text)