from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from  kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
from kivy.metrics import dp
import time

from kivy import platform
if platform == "android":
    from jnius import autoclass
# from kivymd.tools.hotreload.app import MDApp

connecting_state = 0

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

    def getAndroidBluetoothSocket(self, DeviceName):
        try :
            global connecting_state
            connecting_state = 1
            snackbar("Searching for AndroidBluetoothSocket")
            print("Searching for AndroidBluetoothSocket")

            bluetooth_adapter = self.BluetoothAdapter.getDefaultAdapter()
            if not bluetooth_adapter.isEnabled():
                bluetooth_adapter.enable()
                snackbar("Enabling Bluetooth...")
                print("Enabling Bluetooth...")

            paired_devices = bluetooth_adapter.getBondedDevices().toArray()
            socket = None
            for device in paired_devices:
                if device.getName() == DeviceName:
                    socket = device.createRfcommSocketToServiceRecord(
                        self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                    self.ReceiveData = self.BufferReader(self.InputStream(socket.getInputStream()))
                    self.SendData = socket.getOutputStream()
                    socket.connect()
                    self.ConnectionEstablished = True
                    print('Bluetooth Connection successful')
                    snackbar("Bluetooth Connection successful")
                    break

            if not self.ConnectionEstablished:
                snackbar("Bluetooth Connection failed")
                print("Bluetooth Connection failed")
                connecting_state = 0
            return self.ConnectionEstablished
        except:
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


    def __init__(self):
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


    def __del__(self):
        global connecting_state
        connecting_state = 0
        snackbar("Destroying Bluetooth class")
        print('Destroying Bluetooth class')


class MyApp(MDApp):
    # DEBUG = True

    def switch_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission 
            request_permissions([Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH_SCAN,Permission.ACCESS_FINE_LOCATION])

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.android_bluetooth = AndroidBluetoothClass()
        self.KV = Builder.load_file("kivy.kv")
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
        if connecting_state == 0:
            self.android_bluetooth.getAndroidBluetoothSocket("HC-05")  


MyApp().run()
