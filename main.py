############################################################
########################## Imports #########################
############################################################
import json
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout  import MDRelativeLayout
from kivymd.uix.boxlayout  import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog,MDDialogButtonContainer,MDDialogIcon,MDDialogHeadlineText,MDDialogSupportingText,MDDialogContentContainer
from kivymd.uix.textfield import MDTextField,MDTextFieldHelperText,MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.widget import Widget
from kivymd.utils.set_bars_colors import set_bars_colors
# from kivymd.tools.hotreload.app import MDApp
from kivy import platform
if platform == "android":
    from android import activity
    from jnius import autoclass,cast

############################################################
###################### Global Variabls #####################
############################################################
app_version = 1.7
style_state = 'Light'
id_devices_list =[]
name_devices_list=[]
address_devices_list=[]
selected_address = ''
RSM1 = 0
LSM1 = 0
RSM2 = 0
LSM2 = 0
RSM3 = 0
LSM3 = 0
SR = 0
############################################################
########################## Screens #########################
############################################################
class MainScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

############################################################
##################### helper Functions #####################
############################################################
def snackbar(text:str):
    MDSnackbar(
        MDSnackbarText(
            text=text,
        ),
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.7,
    ).open()


############################################################
################# Bluetooth Control Class ##################
############################################################
class AndroidBluetoothClass:    
    def __init__(self,KV):
        self.stored_data = JsonStore('data.json')
        self.KV = KV
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
            print(f"="*50)
            print(f"paired_devices = {paired_devices}")
            print(f"="*50)
            
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
        snackbar("Receiving Bluetooth message")
        print("Receiving Bluetooth message")
        DataStream = ''
        if self.ConnectionEstablished:
            DataStream = str(self.ReceiveData.readLine())
            print(f"recevied data = {DataStream}")
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
                    on_release=self.close_dialog
                ),
                MDButton(
                    MDButtonText(
                        text="Save",
                        font_style="Title", role='medium',
                        ),
                    on_release=lambda x: self.save_device_changes(x,card),
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
        print("in save_device_changes")
        print(f"card id = {card.id}")
        print(f"new text = {x.parent.get_ids()['device_name1'].text}")
        device_name = x.parent.get_ids()['device_name1'].text

        # Update the stored information
        index = address_devices_list.index(card.id)
        name_devices_list[index] = device_name
        self.save_to_JSON()

        # Close the dialog
        self.dialog.dismiss("close")
        self.get_paired_devices("HC-05") 

    def __del__(self):
        snackbar("Destroying Bluetooth class")
        print('Destroying Bluetooth class')

menu = ""

############################################################
######################## App Class #########################
############################################################
class MyApp(MDApp):
    # DEBUG = True
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.stored_data = JsonStore('data.json')
        Clock.schedule_once(lambda *args: self.load_from_JSON())

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
    # changing topbar and navigation bar color
    def set_bars_colors(self):
        set_bars_colors(
            [28/255, 162/255, 77/255,1],
            [28/255, 162/255, 77/255,1],
            "Dark" 
        )

    def switch_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def load_from_JSON(self):
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
    
    def open_devices_menu(self, item):
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
    
    def info_dialog(self):
        self.InfoDialog = MDDialog(
            MDDialogIcon(
                icon="information",
            ),
            MDDialogHeadlineText(
                text="About App",
            ),
            MDDialogSupportingText(
                text="All Rights Reserved for Green Clean\n".capitalize(),
            ),

            MDDialogContentContainer(
                MDLabel(
                    text = f'V {app_version}',
                    halign= 'center',
                    text_color = "#130f1e",
                    theme_text_color= "Custom",
                    bold= True,
                    font_style = "Headline",
                    role="medium"
                ),
                orientation= 'vertical'
            ),

            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Ok"),
                    style="text",
                    on_release=self.close_info_dialog
                ),
                spacing="8dp",
            ),
            id="infodialog",
        )
        self.InfoDialog.open()

    def close_info_dialog(self, *args):
        self.InfoDialog.dismiss()


############################################################
################# Screens Buttons Functions ################
##################### Sending Commands #####################
############################################################
    def update_info_label(self):
        self.KV.get_screen('main').ids.WheelsSpeed.text = str(RSM1) 
        self.KV.get_screen('main').ids.BroomsSpeed.text = str(RSM2) 
        self.KV.get_screen('main').ids.PumpSpeed.text = str(RSM3)
        self.KV.get_screen('main').ids.GlassSpeed.text = str(SR)

    def bluetooth_devices(self):
        self.android_bluetooth.get_paired_devices("HC-05")  

    def connect_bluetooth(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
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
            self.update_info_label()
        except Exception as e :
            print(e)

    def edit(self,instance):
        self.android_bluetooth.edit_device_card(instance)  

    def go_to_second_screen(self):
        self.root.current = 'second'
        self.bluetooth_devices()

    def go_back_to_main_screen(self):
        self.root.current = 'main'

    def send_wheels_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('1')
            RSM1+=1
            LSM1+=1
            if RSM1 >= 4 : RSM1 = 4
            if LSM1 >= 4 : LSM1 = 4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_wheels_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('2')
            RSM1-=1
            LSM1-=1        
            if LSM1 <= -4 : LSM1 = -4
            if RSM1 <= -4 : RSM1 = -4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_wheels_stop(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('3')
            LSM1=0
            RSM1=0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_brooms_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('4')
            RSM2+=1
            LSM2+=1
            if RSM2 >= 4 : RSM2 = 4
            if LSM2 >= 4 : LSM2 = 4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_brooms_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('5')
            RSM2-=1
            LSM2-=1
            if LSM2 <= -4 : LSM2 = -4
            if RSM2 <= -4 : RSM2 = -4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_brooms_stop(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('6')
            LSM2=0
            RSM2=0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_pump_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('7')
            RSM3+=1
            LSM3-=1
            if RSM3 >= 3 : RSM3 = 3
            if LSM3 >= 3 : LSM3 = 3
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_pump_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('8')
            RSM3-=1
            LSM3-=1
            if LSM3 <= 0 : LSM3 = 0
            if RSM3 <= 0 : RSM3 = 0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_pump_stop(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('9')
            RSM3=0
            LSM3=0
            self.update_info_label()
        else : snackbar("Not connected to a robot")

    def send_deg_up(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('s')
            SR+=1
            if SR > 4 : SR = 0
            self.update_info_label()
        else : snackbar("Not connected to a robot")
    
    def send_deg_down(self):
        global RSM1,LSM1,RSM2,LSM2,RSM3,LSM3,SR
        if self.android_bluetooth.ConnectionEstablished:
            self.android_bluetooth.BluetoothSend('n')
            SR-=1
            if SR < 0 : SR = 4
            self.update_info_label()
        else : snackbar("Not connected to a robot")

MyApp().run()
