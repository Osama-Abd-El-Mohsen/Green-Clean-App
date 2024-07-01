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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import *
from kivymd.uix.textfield import MDTextField,MDTextFieldHelperText,MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivy.uix.widget import Widget
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import *
import webbrowser
from kivymd.utils.set_bars_colors import set_bars_colors

from kivy import platform
if platform == "android":
    from android import activity
    from jnius import autoclass,cast

style_state = 'Light'
id_devices_list =[]
name_devices_list=[]
address_devices_list=[]
selected_address = ''

class MainScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

def snackbar(text:str):
    MDSnackbar(
        MDSnackbarText(
            text=text,
        ),
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.7,
    ).open()

class AndroidBluetoothClass:    
    def disconnect(self):
        if self.ConnectionEstablished:
            try:
                self.ReceiveData.close()
                self.SendData.close()
                self.ConnectionEstablished = False
                snackbar("Disconnected from device")
                print("Disconnected from device")
                main_screen = self.KV.get_screen('main')
                main_screen.ids.connect.text_color="red"
            except Exception as e:
                snackbar("Failed to disconnect")
                print("Failed to disconnect:", e)
                main_screen = self.KV.get_screen('main')
                main_screen.ids.connect.text_color="red"
        else:
            print("No connection to disconnect")
            main_screen = self.KV.get_screen('main')
            main_screen.ids.connect.text_color="red"

    def init_bluetooth(self):
        try:
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
            
            self.bluetooth_adapter = self.BluetoothAdapter.getDefaultAdapter()
            self.Intent = autoclass('android.content.Intent')
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')

            if not self.bluetooth_adapter.isEnabled():
                snackbar("Enabling Bluetooth...")
                print("Enabling Bluetooth...")
                self.bluetooth_adapter.enable()
                enableIntent = self.Intent(self.bluetooth_adapter.ACTION_REQUEST_ENABLE)
                currentActivity = cast('android.app.Activity', self.PythonActivity.mActivity)
                currentActivity.startActivity(enableIntent)

        except :
            snackbar("Bluetooth Can not initialization")
            print("Bluetooth Can not initialization")


    def get_paired_devices(self, DeviceName="HC-05"):
        global state
        try :
            self.init_bluetooth()
            paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()
            # print(f"="*50)
            # print(f"paired_devices = {paired_devices}")
            # print(f"="*50)
            
            if len(paired_devices)!=0:
                second_screen = self.KV.get_screen('second')
                second_screen.ids.list.clear_widgets()
                for device in paired_devices:
                    if device.getName() == DeviceName and device.getAddress() not in address_devices_list:
                        device_name = device.getName()
                        device_address = device.getAddress()
                        id_devices_list.append(device)
                        name_devices_list.append(device_name)
                        address_devices_list.append(device_address)
                        self.save()

                    elif device.getName() == DeviceName and device.getAddress() in address_devices_list:
                        temp_index =  address_devices_list.index(device.getAddress())
                        print(f"temp_index = {temp_index}")
                        device_name = name_devices_list[temp_index]
                        device_address = address_devices_list[temp_index]

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
                                    pos_hint= {"top": 1, "right": 1},
                                    on_release  = self.edit_device_card
                                ),

                                MDBoxLayout(
                                    MDLabel(
                                        id = "device_name",
                                        text= f"{device_name}",
                                        adaptive_size= True,
                                        bold= True,
                                        halign= 'center',
                                        theme_text_color= "Custom",
                                        text_color = "#141b23",
                                        font_style = "Headline",
                                        role="small",
                                        font_name="font/cairo"

                                    ),
                                    MDLabel(
                                        text= f"{device_address}",
                                        adaptive_size= True,
                                        color= "grey",
                                        pos= ("12dp", "12dp"),
                                    ),
                                    orientation= 'vertical',
                                    padding = dp(15),
                                ),
                            ),
                            id = f"{device_address}",
                            style= "filled",
                            pos_hint= {"center_x": .5, "center_y": .5},
                            # size_hint=(.9, None),
                            # size=(.1,.9) 

                            size_hint=(.5, None),
                            size=(1, 200),
                            padding=(10, 10, 10, 10),
                            )
                        )


        except Exception as e:
            print(e)

    def get_connect_to_device(self, address):
        print("="*50)
        print("in get_connect_to_device")
        print(f"address = {address}")
        print("="*50)
        try :
            self.disconnect()
            self.init_bluetooth()
            device = self.bluetooth_adapter.getRemoteDevice(address)
            print(f"="*50)
            print(f"device = {device}")
            print(f"device Name = {device.getName()}")
            print(f"device Address = {device.getAddress()}")
            print(f"device type = {type(device)}")
            print(f"="*50)
            socket = device.createRfcommSocketToServiceRecord(
                self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            self.ReceiveData = self.BufferReader(self.InputStream(socket.getInputStream()))
            self.SendData = socket.getOutputStream()
            socket.connect()
            self.ConnectionEstablished = True
            print('Bluetooth Connection successful')
            snackbar("Bluetooth Connection successful")
            main_screen = self.KV.get_screen('main')
            main_screen.ids.connect.text_color="#1aaa65"


            if not self.ConnectionEstablished:
                snackbar("Bluetooth Connection failed")
                print("Bluetooth Connection failed")
                main_screen = self.KV.get_screen('main')
                main_screen.ids.connect.text_color="red"
            return self.ConnectionEstablished
        
        except Exception as e:
            print(e)
            snackbar("Bluetooth Connection failed")
            print("Bluetooth Connection failed")
            main_screen = self.KV.get_screen('main')
            main_screen.ids.connect.text_color="red"
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
        self.KV = KV
        self.init_bluetooth()


    def save(self):
        # self.stored_data.put('devices', Id=id_devices_list)
        self.stored_data.put('devices1', Name=name_devices_list)
        self.stored_data.put('devices', Address=address_devices_list)
        self.stored_data.put('style', List2=style_state)
        print("="*50)
        print("saved")
        # print(id_devices_list)
        print(name_devices_list)
        print(address_devices_list)
        print(style_state)
        print("="*50)

    def edit_device_card(self, instance):
        try:
            print(instance)
            print(instance.parent.get_ids()["device_name"].text)
            print(instance.parent.get_ids()["device_name"])
            print(instance.parent.parent)
            print(instance.parent.parent.get_ids())

            # print(card.children[0].children[0].text)
        except Exception as e :
            print(e)

        card = instance.parent.parent
        device_name = instance.parent.get_ids()["device_name"].text

        self.dialog = MDDialog(
            MDDialogIcon(
                icon="pencil",
            ),
            MDDialogHeadlineText(
                text="Edit Device Name",
                font_style="Title",
                role='medium',
                bold=True
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="CANCEL",
                    ),
                    on_press=self.close_dialog
                ),
                MDButton(
                    MDButtonText(
                        text="Save",
                        font_style="Title", role='medium',
                        ),
                    on_press=lambda x: self.save_device_changes(x,card),
                    style="tonal",
                ),
                spacing="5dp",
            ),
            MDDialogContentContainer(
                MDTextField(
                    MDTextFieldHintText(
                        text="Edit Device",
                        halign="left",
                    ),
                    MDTextFieldHelperText(
                        text="Enter Device Name",
                        ),
                    theme_line_color="Custom",
                    id="device_name1",
                    text=device_name,
                    required=True,
                    mode="outlined",
                ),
                id="con",
                orientation="vertical",

            ),
            pos_hint = {"center_x": 0.5, "top": 0.8},
            width_offset = dp(10)
        )

        print("="*50)
        print("before dialog open")
        print("="*50)
        self.dialog.open()

    def close_dialog(self, instance):
        print("in close dia")
        self.dialog.dismiss()

    def save_device_changes(self,x,card):
        print("in save_device_changes")
        print(f"card id = {card.id}")
        print(f"new text = {x.parent.get_ids()['device_name1'].text}")
        device_name = x.parent.get_ids()['device_name1'].text

        # Update the stored information
        index = address_devices_list.index(card.id)
        name_devices_list[index] = device_name
        self.save()

        # Close the dialog
        self.dialog.dismiss("close")
        self.get_paired_devices("HC-05") 


    def __del__(self):
        snackbar("Destroying Bluetooth class")
        print('Destroying Bluetooth class')

menu = ""

class MyApp(MDApp):
    # DEBUG = True
    def set_bars_colors(self):
        set_bars_colors(
            [28/255, 162/255, 77/255,1],
            [28/255, 162/255, 77/255,1],
            "Dark" 
        )
    def open_menu(self, item):
        global menu
        menu_items = [
            {
                "font_name": "font/cairo",
                "text": f"{name}",
                "on_release": lambda x=name, y=address: self.menu_callback(x, y),
            } for name,address in zip(name_devices_list,address_devices_list)
        ]
        menu = MDDropdownMenu(caller=item, items=menu_items)
        menu.open()

    def menu_callback(self, text_item,address):
        global selected_address
        print("in callback")
        print("id_devices_list = ")
        print(id_devices_list)
        print("name_devices_list = ")
        print(name_devices_list)
        print("text_item = ")
        print(text_item)
        print("address = ")
        print(address)
        main_screen = self.KV.get_screen('main')
        main_screen.ids.drop_text.text = text_item
        selected_address = address
        menu.dismiss()

    def switch_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.stored_data = JsonStore('data.json')
        Clock.schedule_once(lambda *args: self.load())
    
    def load(self):
        global style_state,name_devices_list,address_devices_list
        style_state = self.stored_data.get('style')['List2']
        # id_devices_list = self.stored_data.get('devices')['Id']
        name_devices_list = self.stored_data.get('devices1')['Name']
        address_devices_list = self.stored_data.get('devices')['Address']

        print("from load")
        # print(id_devices_list)
        print(name_devices_list)
        print(address_devices_list)
        print(style_state)

    def save(self):
        # self.stored_data.put('devices', Id=id_devices_list)
        self.stored_data.put('devices1', Name=name_devices_list)
        self.stored_data.put('devices', Address=address_devices_list)
        self.stored_data.put('style', List2=style_state)
        print("="*50)
        print("saved")
        # print(id_devices_list)
        print(name_devices_list)
        print(address_devices_list)
        print(style_state)
        print("="*50)

    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission 
            request_permissions([Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH_SCAN,Permission.ACCESS_FINE_LOCATION,Permission.BLUETOOTH])

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.KV = Builder.load_file("kivy.kv")
        self.set_bars_colors()
        self.android_bluetooth = AndroidBluetoothClass(self.KV)
        self.android_bluetooth.get_paired_devices()

        return self.KV

    ####################### Info Dialog ##############################
    def info_dialog(self):
        self.InfoDialog = MDDialog(
            MDDialogIcon(
                icon="information",
            ),
            MDDialogHeadlineText(
                text="About App",
            ),
            MDDialogSupportingText(
                text="this app devolped by Osama Abd El Mohsen \n All Rights Reserved for Green Clean".capitalize(),
            ),

            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="gmail",
                    ),
                    MDListItemSupportingText(
                        text="Osama.m.abdelmohsen@gmail.com",
                    ),
                    on_press=self.info_email_link,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="whatsapp",
                    ),
                    MDListItemSupportingText(
                        text="+201067992759",
                    ),
                    on_press=self.info_whatsapp_link,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDDivider(),
                orientation="vertical",
            ),

            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Ok"),
                    style="text",
                    on_press=self.close_info_dialog
                ),

                spacing="8dp",
            ),
            id="infodialog"
        )
        self.InfoDialog.open()

    def close_info_dialog(self, *args):
        self.InfoDialog.dismiss()

    def info_email_link(self, *arg):
        webbrowser.open("mailto:Osama.m.abdelmohsen@gmail.com")
    def info_whatsapp_link(self, *arg):
        webbrowser.open("https://wa.me/+201067992759/")

####################### Info Dialog ##############################

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


    def bluetooth_devices(self):
        self.android_bluetooth.get_paired_devices("HC-05")  

    def connect_bluetooth(self):
        try :
            self.android_bluetooth.get_connect_to_device(selected_address)  
        except Exception as e :
            print(e)

    def go_to_second_screen(self):
        self.root.current = 'second'
        self.bluetooth_devices()
        
    def go_back_to_main_screen(self):
        self.root.current = 'main'

MyApp().run()
