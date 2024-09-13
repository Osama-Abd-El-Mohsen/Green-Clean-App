from kivy.factory import Factory as F
from utils import load_kv_path
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivymd.utils.set_bars_colors import set_bars_colors
from main import AndroidBluetoothClass

load_kv_path("screens/main_screen.kv")

class MainScreen(F.Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.has_loaded = False  
        self.stored_data = JsonStore('data.json')
        self.load_from_JSON()

    def load_from_JSON(self):
        self.first_open_state = self.stored_data.get('state')['first']

    def on_pre_enter(self, *args):
        parent_manager = self.parent
        if not self.has_loaded:
            if 'Loading Screen' not in self.parent.screen_names:
                self.parent.add_widget(self.get_screen_object_from_screen_name('Loading Screen'))
            self.set_bars_colors_screen_2()
            parent_manager.current = 'Loading Screen'

            if 'Devices Screen' not in self.parent.screen_names:
                self.parent.add_widget(self.get_screen_object_from_screen_name('Devices Screen'))

            Clock.schedule_once(lambda dt: self.load_content(dt, parent_manager), 1)
        else:
            self.set_bars_colors_screen_1()
            parent_manager.current = 'Main Screen'


    def on_enter(self,*args):
        if 'Help Screen_1' not in self.parent.screen_names:
            self.parent.add_widget(self.get_screen_object_from_screen_name('Help Screen_1'))
        self.android_bluetooth = AndroidBluetoothClass(self.parent)
        self.android_bluetooth.get_paired_devices()

    def load_content(self, dt, parent_manager):
        if self.first_open_state == 0:
            if 'Help Screen_1' not in parent_manager.screen_names:
                parent_manager.add_widget(self.get_screen_object_from_screen_name('Help Screen_1'))
            self.set_bars_colors_screen_2()
            parent_manager.current = 'Help Screen_1'

        else :
            if 'Main Screen' not in parent_manager.screen_names:
                parent_manager.add_widget(self.get_screen_object_from_screen_name('Main Screen'))
            self.set_bars_colors_screen_1()
            parent_manager.current = 'Main Screen'

        self.has_loaded = True
        print("MainScreen loaded and displayed.")


    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        return screen_object

    def set_bars_colors_screen_2(self):
        set_bars_colors(
            [244/255, 249/255, 252/255,1],
            [244/255, 249/255, 252/255,1],
            "Dark" 
        )

    def set_bars_colors_screen_1(self):
        set_bars_colors(
            [244/255, 249/255, 252/255,1],
            [17/255, 172/255, 104/255,1],
            "Dark" 
        )
