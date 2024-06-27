from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivy import platform
if platform == "android":
    from jnius import autoclass
from kivymd.tools.hotreload.app import MDApp
from kivymd.utils.set_bars_colors import set_bars_colors


class AndroidBluetoothClass:

    def getAndroidBluetoothSocket(self, DeviceName):
        toast("Searching for AndroidBluetoothSocket")
        print("Searching for AndroidBluetoothSocket")
        paired_devices = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
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
                toast("Bluetooth Connection successful")
                break

        if not self.ConnectionEstablished:
            toast("Bluetooth Connection failed")
        return self.ConnectionEstablished

    def BluetoothSend(self, Message):
        if self.ConnectionEstablished:
            self.SendData.write(Message.encode())
        else:
            print('Bluetooth device not connected')

    def BluetoothReceive(self):
        DataStream = ''
        if self.ConnectionEstablished:
            DataStream = str(self.ReceiveData.readline())
        return DataStream

    def __init__(self):
        toast("Initializing Bluetooth")
        print("Initializing Bluetooth")
        if platform == "android":
            self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
            self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
            self.UUID = autoclass('java.util.UUID')
            self.BufferReader = autoclass('java.io.BufferedReader')
            self.InputStream = autoclass('java.io.InputStreamReader')
        self.ConnectionEstablished = False
        toast("Bluetooth initialization finished")
        print("Bluetooth initialization finished")

    def __del__(self):
        toast("Destroying Bluetooth class")
        print('Destroying Bluetooth class')

class MyApp(MDApp):
    DEBUG = True

    def switch_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    def build_app(self):

        if platform == "android":
            from android.permissions import request_permissions, Permission 
            request_permissions([Permission.BLUETOOTH_CONNECT,Permission.BLUETOOTH_SCAN ])

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.android_bluetooth = AndroidBluetoothClass()
        self.KV = Builder.load_file("kivy.kv")
        return self.KV

    def send_wheels_stop(self):
        self.android_bluetooth.BluetoothSend('a')

    def send_Broms_stop(self):
        self.android_bluetooth.BluetoothSend('b')

    def send_pump_stop(self):
        self.android_bluetooth.BluetoothSend('a')

    def send_command_b(self):
        self.android_bluetooth.BluetoothSend('b')

    def connect_bluetooth(self):
        self.android_bluetooth.getAndroidBluetoothSocket("HC-05")  # Replace "YourDeviceName" with the actual device name


MyApp().run()


