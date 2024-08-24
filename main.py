############################################################
########################## Imports #########################
############################################################
import json
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout  import MDRelativeLayout
from kivymd.uix.boxlayout  import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog,MDDialogButtonContainer,MDDialogIcon,MDDialogHeadlineText,MDDialogSupportingText,MDDialogContentContainer
from kivymd.uix.textfield import MDTextField,MDTextFieldHelperText,MDTextFieldHintText
from kivymd.uix.progressindicator.progressindicator import MDCircularProgressIndicator
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.widget import Widget
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory as F
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition,WipeTransition,ScreenManager,Screen,NoTransition
import datetime
# from kivymd.tools.hotreload.app import MDApp
if platform == "android":
    from android import activity
    from jnius import autoclass,cast
if platform != "android":
    Window.size = (406, 762)
    Window.always_on_top = True
Window.clearcolor = (244/255, 249/255, 252/255, 1)
x = datetime.datetime.now()


############################################################
################ ScreenManager & Load Screen ###############
############################################################
class MyScreenManager(ScreenManager) :
    pass

class LoadScreen(Screen):
    pass

############################################################
###################### Global Variabls #####################
############################################################
app_version = 2.5
style_state = 'Light'
id_devices_list =[]
name_devices_list=[]
address_devices_list=[]
selected_address = ''
first_open_state = 0
RSM1 = 0
LSM1 = 0
RSM2 = 0
LSM2 = 0
RSM3 = 0
LSM3 = 0
SR = 0
W = 0

############################################################
##################### helper Functions #####################
############################################################
def snackbar(text:str):
    MDSnackbar(
        MDSnackbarText(
            text=text,
            theme_text_color= "Custom",
            theme_font_name= "Custom",
            theme_font_size= "Custom",
            font_name="BPoppins",
            text_color = "#081415",
            font_size = dp(15),
        pos_hint={"center_x": 0.5},
        ),
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.7,
        background_color = "#fefefe",
        radius= [30, 30, 30 ,30],
        theme_shadow_softness= "Custom",
        shadow_softness= 10,
        theme_elevation_level= "Custom",
        elevation_level= 1,
    ).open()



############################################################
################# Bluetooth Control Class ##################
############################################################
class AndroidBluetoothClass:    
    def __init__(self,root):
        self.stored_data = JsonStore('data.json')
        self.root = root
        # self.init_bluetooth()
    
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
            print("Bluetooth initialization finished")
            
            self.bluetooth_adapter = self.BluetoothAdapter.getDefaultAdapter()
            self.Intent = autoclass('android.content.Intent')
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')

            if not self.bluetooth_adapter.isEnabled():
                # snackbar("Enabling Bluetooth...")
                print("Enabling Bluetooth...")
                self.bluetooth_adapter.enable()
                enableIntent = self.Intent(self.bluetooth_adapter.ACTION_REQUEST_ENABLE)
                currentActivity = cast('android.app.Activity', self.PythonActivity.mActivity)
                currentActivity.startActivity(enableIntent)

        except :
            # snackbar("Bluetooth Can not initialization")
            print("Bluetooth Can not initialization")
    
    def get_paired_devices(self, DeviceName="HC-05"):
        global state
        try :
            self.init_bluetooth()
            paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()
            print(f"="*50)
            print(f"paired_devices = {paired_devices}")
            print(f"="*50)
            
            print("in get_paired_devices")
            if len(paired_devices)!=0:
                print("in if")
                second_screen = self.root.get_screen('Devices Screen')
                second_screen.ids.list.clear_widgets()
                for device in paired_devices:
                    if device.getName() == DeviceName and device.getAddress() not in address_devices_list:
                        device_name = device.getName()
                        device_address = device.getAddress()
                        id_devices_list.append(device)
                        name_devices_list.append(device_name)
                        address_devices_list.append(device_address)
                        self.save_to_JSON()

                    elif device.getName() == DeviceName and device.getAddress() in address_devices_list:
                        temp_index =  address_devices_list.index(device.getAddress())
                        print(f"temp_index = {temp_index}")
                        device_name = name_devices_list[temp_index]
                        device_address = address_devices_list[temp_index]

                        try:
                            print(f"DeviceName = {device_name}")
                            print(f"getAddress = {device_address}")
                        except:pass
                        second_screen = self.root.get_screen('Devices Screen')
                        second_screen.ids.list.add_widget(
                            MDCard(

                            MDRelativeLayout(
                                MDIconButton(
                                    icon= "pencil",
                                    pos_hint= {"top": 1, "right": 1},
                                    on_release  = self.edit_device_card,
                                    theme_text_color= "Custom",
                                    text_color = "#222627",
                                    theme_font_size= "Custom",
                                    size= (dp(25), dp(25)),
                                    font_size= dp(25)

                                ),

                                MDBoxLayout(
                                    MDLabel(
                                        id = "device_name",
                                        text= f"{device_name}",
                                        adaptive_size= True,
                                        theme_text_color= "Custom",
                                        theme_font_name= "Custom",
                                        theme_font_size= "Custom",
                                        font_name="BPoppins",
                                        text_color = "#081415",
                                        font_size = dp(18),

                                    ),
                                    MDLabel(
                                        text= f"{device_address}",
                                        adaptive_size= True,
                                        pos= ("12dp", "12dp"),
                                        theme_text_color= "Custom",
                                        theme_font_name= "Custom",
                                        theme_font_size= "Custom",
                                        font_name="MPoppins",
                                        text_color = "#5b5b5a",
                                        font_size = dp(16),
                                    ),
                                    orientation= 'vertical',
                                    padding = dp(15),
                                ),
                            ),
                            id = f"{device_address}",
                            style= "elevated",
                            pos_hint= {"center_x": .5, "center_y": .5},
                            theme_bg_color= "Custom",
                            md_bg_color = "#fefefe",
                            theme_shadow_softness= "Custom",
                            shadow_softness= 15,
                            theme_elevation_level= "Custom",
                            elevation_level= 1,

                            size_hint=(.5, None),
                            size=(1, 250),
                            padding=(10, 10, 10, 10),
                            state_hover = 0,
                            state_press = 0,
                            
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
            main_screen = self.root.get_screen('Main Screen')
            main_screen.ids.connect.text_color="#1aaa65"


            if not self.ConnectionEstablished:
                snackbar("Bluetooth Connection failed")
                print("Bluetooth Connection failed")
                main_screen = self.root.get_screen('Main Screen')
                main_screen.ids.connect.text_color="red"
            return self.ConnectionEstablished
        
        except Exception as e:
            print(e)
            snackbar("Bluetooth Connection failed")
            print("Bluetooth Connection failed")
            main_screen = self.root.get_screen('Main Screen')
            main_screen.ids.connect.text_color="red"
            return 0
    
    def disconnect(self):
        if self.ConnectionEstablished:
            try:
                self.ReceiveData.close()
                self.SendData.close()
                self.ConnectionEstablished = False
                print("Disconnected from device")
                main_screen = self.root.get_screen('Main Screen')
                main_screen.ids.connect.text_color="red"
            except Exception as e:
                print("Failed to disconnect:", e)
                main_screen = self.root.get_screen('Main Screen')
                main_screen.ids.connect.text_color="red"
        else:
            print("No connection to disconnect")
            main_screen = self.root.get_screen('Main Screen')
            main_screen.ids.connect.text_color="red"

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

    def BluetoothReceive(self):
        DataStream = ''
        if self.ConnectionEstablished:
            DataStream = str(self.ReceiveData.readLine())
            print(f"recevied data = {DataStream}")
            print("Receiving Bluetooth message")
        return DataStream


############################################################
############## Edit & Save data  to DataBase ###############
############################################################
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
        # device_name = instance.parent.get_ids()["device_name"].text
        device_name = card.children[0].children[0].children[1].text

        print("="*50)
        print("in edit_device_card")
        print(device_name)
        print("="*50)

        
        self.dialog = MDDialog(
            MDDialogIcon(
                icon="pencil",
                theme_icon_color= "Custom",
                icon_color= "#11ac68"
            ),
            MDDialogHeadlineText(
                text="Edit Device Name",
                theme_text_color= "Custom",
                theme_font_name= "Custom",
                theme_font_size= "Custom",
                font_name="BPoppins",
                text_color = "#222627",
                font_size = dp(15)
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Cancel",
                        theme_text_color= "Custom",
                        theme_font_name= "Custom",
                        theme_font_size= "Custom",
                        font_name="BPoppins",
                        text_color = "#222627",
                        font_size = dp(13)
                    ),
                    fab_state= "expand",
                    style= "tonal",
                    theme_bg_color= "Custom",
                    md_bg_color= "#fefefe",
                    on_release=self.close_dialog,
                ),
                MDButton(
                    MDButtonText(
                        text="Save",
                        font_style="Title", role='medium',
                        theme_text_color= "Custom",
                        theme_font_name= "Custom",
                        theme_font_size= "Custom",
                        font_name="BPoppins",
                        text_color = "#222627",
                        font_size = dp(13)
                        ),
                    fab_state= "expand",
                    style= "tonal",
                    theme_bg_color= "Custom",
                    md_bg_color= "#11ac68",
                    on_release=lambda x: self.save_device_changes(x,card),
                ),
                spacing="5dp",
            ),
            MDDialogContentContainer(
                MDTextField(
                    MDTextFieldHintText(
                        text="Edit Device",
                        theme_text_color= "Custom",
                        theme_font_name= "Custom",
                        theme_font_size= "Custom",
                        font_name="BPoppins",
                        halign="left",
                        font_size = dp(13)

                    ),
                    MDTextFieldHelperText(
                        text="Enter Device Name",
                        theme_text_color= "Custom",
                        theme_font_name= "Custom",
                        theme_font_size= "Custom",
                        font_name="BPoppins",
                        font_size = dp(15)
                        
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
            theme_bg_color= "Custom",
            pos_hint = {"center_x": 0.5, "top": 0.8},
            width_offset = dp(10),
            _md_bg_color = "#f4f9fc",
            state_hover = 0,
            state_press = 0,
            auto_dismiss = False

        )

        print("="*50)
        print("before dialog open")
        print("="*50)
        self.dialog.open()

    def close_dialog(self, instance):
        print("in close dia")
        self.dialog.dismiss()

    def save_to_JSON(self):
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
    
    def save_device_changes(self,x,card):

        # Close the dialog
        if len(x.parent.get_ids()['device_name1'].text) != 0 :
            print("in save_device_changes")
            print(f"card id = {card.id}")
            print(f"new text = {x.parent.get_ids()['device_name1'].text}")
            device_name = x.parent.get_ids()['device_name1'].text

            # Update the stored information
            index = address_devices_list.index(card.id)
            name_devices_list[index] = device_name
            self.save_to_JSON()
            self.dialog.dismiss("close")
            self.get_paired_devices("HC-05") 
        else : x.parent.get_ids()['device_name1'].text = "Robot_x"

    def __del__(self):
        print('Destroying Bluetooth class')

menu = ""


LOADING_KV = """
MyScreenManager:
    LoadScreen:
        name: 'Load Screen'
        app: app

        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: "#f4f9fc"
            spacing:'1dp'
            size_hint: (1, 1)
            MDBoxLayout:
                orientation: 'horizontal'
                padding: '7dp'
                spacing: '20dp'
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.2, .2)
                md_bg_color: "#f4f9fc"
                MDCircularProgressIndicator:
                    size_hint: (.5, .5)
                    size: ("48dp", "48dp")
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    color: "#11ac68"
                    line_width : 4
"""
from kivy.lang.builder import Builder


############################################################
######################## App Class #########################
############################################################
class MyApp(MDApp):
    # DEBUG = True
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.Android_back_click)

    def build(self):
        self.stored_data = JsonStore('data.json')
        self.load_from_JSON()
        self.screen_manager = MyScreenManager(transition = WipeTransition())
        if platform == "android":
            from android.permissions import request_permissions, Permission 
            request_permissions([Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH_SCAN,Permission.ACCESS_FINE_LOCATION,Permission.BLUETOOTH])
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"   
        

        y = datetime.datetime.now()
        print(y-x)
        self.screen_manager.transition = WipeTransition() 
        return Builder.load_string(LOADING_KV)
    
    def on_start(self):
        self.load_main()
        self.help_page()
        y = datetime.datetime.now()
        print(y-x)

        self.android_bluetooth = AndroidBluetoothClass(self.root)
        self.android_bluetooth.get_paired_devices()

    # if first time open the app go to help screens
    def help_page(self):
        global first_open_state
        self.set_bars_colors_screen_2()
        first_open_state = 1
        self.save_to_JSON()
        print(datetime.datetime.now()-x)

    def Android_back_click(self,window,key,*largs):
            if key in [27, 1001]:
                self.root.transition = SlideTransition(direction='up')
                self.set_bars_colors_screen_1()
                self.root.current = 'Main Screen'
                return True

    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        return screen_object


    # changing topbar and navigation bar color
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

    def switch_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def load_from_JSON(self):
        global style_state,name_devices_list,address_devices_list,first_open_state
        style_state = self.stored_data.get('style')['List2']
        # id_devices_list = self.stored_data.get('devices')['Id']
        name_devices_list = self.stored_data.get('devices1')['Name']
        address_devices_list = self.stored_data.get('devices')['Address']
        first_open_state = self.stored_data.get('state')['first']

        print("from load")
        # print(id_devices_list)
        print(name_devices_list)
        print(address_devices_list)
        print(style_state)

    def save_to_JSON(self):
        # self.stored_data.put('devices', Id=id_devices_list)
        self.stored_data.put('devices1', Name=name_devices_list)
        self.stored_data.put('devices', Address=address_devices_list)
        self.stored_data.put('style', List2=style_state)
        self.stored_data.put('state', first=first_open_state)
        print("="*50)
        print("saved")
        # print(id_devices_list)
        print(name_devices_list)
        print(address_devices_list)
        print(style_state)
        print("="*50)
    
    def open_devices_menu(self, item):
        global menu
        menu_items = [
            {
                "font_name": "BPoppins",
                "text": f"{name}",
                "on_release": lambda x=name, y=address: self.menu_callback(x, y),
            } for name,address in zip(name_devices_list,address_devices_list)
        ]
        menu = MDDropdownMenu(
            caller=item,
            items=menu_items,
            theme_bg_color= "Custom",
            theme_divider_color= "Custom",
            theme_line_color= "Custom",
            _md_bg_color = "#f4f9fc",
            line_color = "#11ac68",
            position="bottom",
            )
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
        main_screen = self.root.get_screen('Main Screen')
        main_screen.ids.drop_text.text = text_item
        selected_address = address
        menu.dismiss()
    
    def info_dialog(self):
        self.InfoDialog = MDDialog(
            MDDialogIcon(
                icon="information",
                theme_icon_color= "Custom",
                icon_color= "#11ac68"
            ),
            MDDialogHeadlineText(
                text="About App",
                theme_text_color= "Custom",
                theme_font_name= "Custom",
                theme_font_size= "Custom",
                font_name="BPoppins",
                text_color = "#081415",
                font_size = dp(18),
            ),
            MDDialogSupportingText(
                text="All Rights Reserved for Green Clean\n".capitalize(),
                halign= 'center',
                theme_text_color= "Custom",
                theme_font_name= "Custom",
                theme_font_size= "Custom",
                font_name="MPoppins",
                text_color = "#282827",
                font_size = dp(13),
            ),

            MDDialogContentContainer(
                MDLabel(
                    text = f'V {app_version}',
                    halign= 'center',
                    theme_text_color= "Custom",
                    theme_font_name= "Custom",
                    theme_font_size= "Custom",
                    font_name="BPoppins",
                    text_color = "#081415",
                    font_size = dp(12),
                ),
                orientation= 'vertical'
            ),

            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Ok",
                        theme_text_color= "Custom",
                        theme_font_name= "Custom",
                        theme_font_size= "Custom",
                        font_name="BPoppins",
                        text_color = "#f4f9fc",
                        font_size = dp(13),
                        ),
                    style= "tonal",
                    theme_bg_color= "Custom",
                    md_bg_color= "#282827",
                    on_release=self.close_info_dialog,
                ),
                spacing="8dp",
            ),
            id="infodialog",
            theme_bg_color= "Custom",
            _md_bg_color = "#f4f9fc",
            state_hover = 0,
            state_press = 0,
        )
        self.InfoDialog.open()

    def close_info_dialog(self, *args):
        self.InfoDialog.dismiss()


############################################################
################# Screens Buttons Functions ################
##################### Sending Commands #####################
############################################################
    def update_info_label(self):
        self.root.get_screen('Main Screen').ids.WheelsSpeed.text = str(RSM1) 
        self.root.get_screen('Main Screen').ids.BroomsSpeed.text = str(RSM2) 
        self.root.get_screen('Main Screen').ids.PumpSpeed.text = str(RSM3)
        self.root.get_screen('Main Screen').ids.GlassSpeed.text = str(SR)
        self.root.get_screen('Main Screen').ids.pumpState.text = "PUMP : ON" if abs(W) ==1 else  "PUMP : OFF"

    def bluetooth_devices(self):
        self.android_bluetooth.get_paired_devices("HC-05")  

    def connect_bluetooth(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        try :
            self.android_bluetooth.get_connect_to_device(selected_address) 
            self.android_bluetooth.BluetoothSend('c')
            dic = self.android_bluetooth.BluetoothReceive()
            dic=dic.replace("'",'"')
            dic = json.loads(dic)
            print("="*50)
            print(dic)
            print("="*50)
            
            RSM1 = dic['RSM1']
            LSM1 = dic['LSM1']
            RSM2 = dic['RSM2']
            LSM2 = dic['LSM2']
            RSM3 = dic['RSM3']
            LSM3 = dic['LSM3']
            SR   = dic['SR']
            W   = dic['W']
            self.update_info_label()
        except Exception as e :
            print(e)

    def edit(self,instance):
        self.android_bluetooth.edit_device_card(instance)  

    def go_back_to_help_1_screen(self):
        if 'Help Screen_1' not in self.root.screen_names:
            self.root.add_widget(self.get_screen_object_from_screen_name('Help Screen_1'))
        self.root.transition = SlideTransition(direction='left')
        self.root.current = 'Help Screen_1'
        self.set_bars_colors_screen_2()

    def go_back_to_help_2_screen(self):
        if 'Help Screen_2' not in self.root.screen_names:
            self.root.add_widget(self.get_screen_object_from_screen_name('Help Screen_2'))
        self.root.transition = WipeTransition()
        self.root.current = 'Help Screen_2'
        self.set_bars_colors_screen_2()

    def go_back_to_help_3_screen(self):
        if 'Help Screen_3' not in self.root.screen_names:
            self.root.add_widget(self.get_screen_object_from_screen_name('Help Screen_3'))
        self.root.transition = WipeTransition()
        self.root.current = 'Help Screen_3'
        self.set_bars_colors_screen_2()

    def go_to_second_screen(self):

        if 'Devices Screen' not in self.root.screen_names:
            from screens.devices_screen import DevicesScreen
            screen = DevicesScreen(name='Devices Screen')
            self.root.add_widget(screen)
        self.root.transition = SlideTransition(direction='down')
        self.root.current = 'Devices Screen'
        self.set_bars_colors_screen_2()
        self.bluetooth_devices()

    def load_main(self):
        if 'Main Screen' not in self.root.screen_names:
            self.root.add_widget(self.get_screen_object_from_screen_name('Main Screen'))
        self.set_bars_colors_screen_1()
        self.root.current = 'Main Screen'

    def go_back_to_main_screen(self):
        self.root.transition = SlideTransition(direction='right')
        self.load_main()

    def send_wheels_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('1')
            RSM1+=1
            LSM1+=1
            if RSM1 >= 4 : RSM1 = 4
            if LSM1 >= 4 : LSM1 = 4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_wheels_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('2')
            RSM1-=1
            LSM1-=1        
            if LSM1 <= -4 : LSM1 = -4
            if RSM1 <= -4 : RSM1 = -4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_wheels_stop(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('3')
            LSM1=0
            RSM1=0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_brooms_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('4')
            RSM2+=1
            LSM2+=1
            if RSM2 >= 4 : RSM2 = 4
            if LSM2 >= 4 : LSM2 = 4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_brooms_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('5')
            RSM2-=1
            LSM2-=1
            if LSM2 <= -4 : LSM2 = -4
            if RSM2 <= -4 : RSM2 = -4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_brooms_stop(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('6')
            LSM2=0
            RSM2=0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_pump_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('7')
            RSM3+=1
            LSM3-=1
            if RSM3 >= 3 : RSM3 = 3
            if LSM3 >= 3 : LSM3 = 3
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_pump_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('8')
            RSM3-=1
            LSM3-=1
            if LSM3 <= 0 : LSM3 = 0
            if RSM3 <= 0 : RSM3 = 0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_pump_stop(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('9')
            RSM3=0
            LSM3=0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_deg_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('s')
            SR+=1
            if SR > 3 : SR = 0
            self.update_info_label()
        else : snackbar("Not connected to a robot")
    
    # def send_deg_down(self):
    #     global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
    #     if self.android_bluetooth.ConnectionEstablished:
    #         self.android_bluetooth.BluetoothSend('w')
    #         SR-=1
    #         if SR < 0 : SR = 3
    #         self.update_info_label()
    #     else : snackbar("Not connected to a robot")
        
    def send_deg_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR,W
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('w')
            W=~W
            print(abs(W))
            self.update_info_label()
        else : snackbar("Not connected to a robot")



if __name__ == "__main__":

    LabelBase.register (name="BPoppins", fn_regular="font/Poppins/Poppins-Bold.ttf")
    LabelBase.register (name="MPoppins", fn_regular="font/Poppins/Poppins-Medium.ttf")

    LabelBase.register (name="BBCairo", fn_regular="font/cairo/Cairo-Black.ttf")
    
    MyApp().run()