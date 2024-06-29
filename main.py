from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout  import MDRelativeLayout
from kivymd.uix.boxlayout  import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
from kivy.metrics import dp
import time
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

from kivy import platform
if platform == "android":
    from jnius import autoclass
# from kivymd.tools.hotreload.app import MDApp

class MainScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

devices_list =[]
style_state =[]

def snackbar(text:str):
    MDSnackbar(
        MDSnackbarText(
            text=text,
        ),
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.8,
    ).open()



class AndroidBluetoothClass:

    def get_paired_devices(self, DeviceName="HC-05"):
        devices_list = []
        try :
            snackbar("Searching for AndroidBluetoothSocket")
            print("Searching for AndroidBluetoothSocket")

            bluetooth_adapter = self.BluetoothAdapter.getDefaultAdapter()

            if not bluetooth_adapter.isEnabled():
                bluetooth_adapter.enable()
                snackbar("Enabling Bluetooth...")
                print("Enabling Bluetooth...")

            paired_devices = bluetooth_adapter.getBondedDevices().toArray()
            print(f"="*50)
            print(f"paired_devices = {paired_devices}")
            print(f"="*50)
            socket = None
            for index,device in enumerate(paired_devices):
                temp_list =[]
                if device.getName() == DeviceName  :
                    device_name = device.getName()
                    device_address = device.getAddress()
                    temp_list.append(index)
                    temp_list.append(device)
                    temp_list.append(device_name)
                    temp_list.append(device_address)
                    devices_list.append(temp_list) 
                    self.save()

                    try:
                        print(f"DeviceName = {device_name}")
                        print(f"getAddress = {device_address}")
                    except:pass
                    second_screen = self.KV.get_screen('second')
                    second_screen.ids.list.add_widget(
                        MDCard(

                        MDRelativeLayout(
                            MDIconButton(
                                icon= "pencil",
                                pos_hint= {"top": 1, "right": .92},
                            ),

                            MDIconButton(
                                icon= "delete",
                                pos_hint= {"top": 1, "right":1},
                            ),

                            MDBoxLayout(
                                MDLabel(
                                    text= f"{device_name}",
                                    adaptive_size= True,
                                    bold= True,
                                    halign= 'center',
                                    theme_text_color= "Custom",
                                    text_color = "#141b23",
                                    font_style = "Headline",
                                    role="small",
                                ),
                                MDLabel(
                                    text= f"{device_address}",
                                    adaptive_size= True,
                                    color= "grey",
                                    pos= ("12dp", "12dp"),
                                    bold= True,
                                ),
                                orientation= 'vertical',
                                padding = dp(15),

                            ),
                        ),
                        style= "filled",
                        pos_hint= {"center_x": .5, "center_y": .5},
                        padding= "4dp",
                        size_hint=(.9, None),
                        )
                    )
                    return devices_list
        except Exception as e:
            print(e)

    def get_connect_to_device(self, device):
        try :
            socket = device.createRfcommSocketToServiceRecord(
                self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            self.ReceiveData = self.BufferReader(self.InputStream(socket.getInputStream()))
            self.SendData = socket.getOutputStream()
            socket.connect()
            self.ConnectionEstablished = True
            print('Bluetooth Connection successful')
            snackbar("Bluetooth Connection successful")

            if not self.ConnectionEstablished:
                snackbar("Bluetooth Connection failed")
                print("Bluetooth Connection failed")
            return self.ConnectionEstablished
        
        except Exception as e:
            print(e)
            snackbar("Bluetooth Connection failed")
            print("Bluetooth Connection failed")
            return 0


    def BluetoothSend(self, Message):
        try:
            if self.ConnectionEstablished:
                self.SendData.write(Message.encode())
            else:
                snackbar('Bluetooth device not connected')
                print('Bluetooth device not connected')
        except :
            snackbar('Bluetooth device not connected')
            print('Bluetooth device not connected')


    def __init__(self,KV):
        self.stored_data = JsonStore('data.json')
        Clock.schedule_once(lambda *args: self.load())
        self.KV = KV
        try:
            snackbar("Initializing Bluetooth")
            print("Initializing Bluetooth")
            if platform == "android":
                self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
                self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
                self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
                self.UUID = autoclass('java.util.UUID')
                self.BufferReader = autoclass('java.io.BufferedReader')
                self.InputStream = autoclass('java.io.InputStreamReader')
            self.ConnectionEstablished = False
            snackbar("Bluetooth initialization finished")
            print("Bluetooth initialization finished")
        except :
            snackbar("Bluetooth Can not initialization")
            print("Bluetooth Can not initialization")

    def load(self):
        style_loaded = self.stored_data.get('style')
        devices_loaded = self.stored_data.get('devices')
        print("from load")
        print(devices_loaded)
        print(style_loaded)

    def save(self):
        self.stored_data.put('devices', List=devices_list)
        self.stored_data.put('style', List2=style_state)
        print("="*50)
        print("saved")
        print(devices_list)
        print(style_state)
        print("="*50)

    def __del__(self):
        snackbar("Destroying Bluetooth class")
        print('Destroying Bluetooth class')



class MyApp(MDApp):
    # DEBUG = True
    
    def switch_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.stored_data = JsonStore('data.json')
        Clock.schedule_once(lambda *args: self.load())
    
    def load(self):
        style_loaded = self.stored_data.get('style')
        devices_loaded = self.stored_data.get('devices')
        print(devices_loaded)
        print(style_loaded)

    def save(self):
        self.stored_data.put('devices', List=devices_list)
        self.stored_data.put('style', List2=style_state)


    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission 
            request_permissions([Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH_SCAN,Permission.ACCESS_FINE_LOCATION])

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.KV = Builder.load_file("kivy.kv")
        self.android_bluetooth = AndroidBluetoothClass(self.KV)
        devices_list = self.android_bluetooth.get_paired_devices()
        print("="*50)
        print("devices_list")
        print(devices_list)
        print("="*50)

        return self.KV
    
    

    def send_wheels_up(self):
        self.android_bluetooth.BluetoothSend('1')
    def send_wheels_down(self):
        self.android_bluetooth.BluetoothSend('2')
    def send_wheels_stop(self):
        self.android_bluetooth.BluetoothSend('3')

    def send_brooms_up(self):
        self.android_bluetooth.BluetoothSend('4')
    def send_brooms_down(self):
        self.android_bluetooth.BluetoothSend('5')
    def send_brooms_stop(self):
        self.android_bluetooth.BluetoothSend('6')

    def send_pump_up(self):
        self.android_bluetooth.BluetoothSend('7')
    def send_pump_down(self):
        self.android_bluetooth.BluetoothSend('8')
    def send_pump_stop(self):
        self.android_bluetooth.BluetoothSend('9')


    def connect_bluetooth(self):
        # self.android_bluetooth.get_connect_to_device("HC-05")  
        self.android_bluetooth.get_paired_devices("HC-05")  

    def go_to_second_screen(self):
        self.root.current = 'second'
        self.connect_bluetooth()
        
    def go_back_to_main_screen(self):
        self.root.current = 'main'

MyApp().run()
