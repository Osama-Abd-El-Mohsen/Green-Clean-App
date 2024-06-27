from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from jnius import autoclass
from kivy import platform

layout = '''
BoxLayout:
    id: boxlayout
    orientation:'vertical'
    adaptive_size: True

    MDIconButton:
        icon: "bluetooth"
        pos_hint: {'center_x':0.5,'center_y':0.875}
        user_font_size: "40sp"
        on_release: app.android_bluetooth.getAndroidBluetoothSocket('HC-05')

    MDIconButton:
        icon: "led-on"
        user_font_size: "40sp"
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        on_release: app.send_command_a()

    MDIconButton:
        icon: "led-off"
        user_font_size: "40sp"
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        on_release: app.send_command_b()
'''

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
        toast("Sending Bluetooth message")
        print("Sending Bluetooth message")
        if self.ConnectionEstablished:
            self.SendData.write(Message.encode())
        else:
            print('Bluetooth device not connected')

    def BluetoothReceive(self):
        toast("Receiving Bluetooth message")
        print("Receiving Bluetooth message")
        DataStream = ''
        if self.ConnectionEstablished:
            DataStream = str(self.ReceiveData.readline())
        return DataStream

    def __init__(self):
        toast("Initializing Bluetooth")
        print("Initializing Bluetooth")
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

    def build(self):

        if platform == "android":
            from android.permissions import request_permissions, Permission 
            request_permissions([Permission.BLUETOOTH_CONNECT,Permission.BLUETOOTH_SCAN ])

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.android_bluetooth = AndroidBluetoothClass()

        return Builder.load_string(layout)

    def send_command_a(self):
        self.android_bluetooth.BluetoothSend('a')

    def send_command_b(self):
        self.android_bluetooth.BluetoothSend('b')

MyApp().run()


