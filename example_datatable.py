from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp

data = {
        '1': {"name": "john", "age": "25", "gender": "male"},
        '2': {"name": "rewr", "age": "25", "gender": "male"},
        '3': {"name": "grgr", "age": "25", "gender": "male"},
        '4': {"name": "opoe", "age": "25", "gender": "male"},
        '5': {"name": "klwq", "age": "25", "gender": "male"},                                      
            }


class MainScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,            
            )
            
        self.table = MDDataTable(
            size_hint=(1, None),
            height=dp(500),
            check=True,
            column_data = [
                ("No .  ", dp(30)),
                ("Name  .  ", dp(30)),
                ("Age  .  ", dp(30)),
                ("Gender  .  ", dp(30)),               
            ],
            row_data=[
            (key, data[key]['name'], data[key]['age'], data[key]['gender'])
                for key in data.keys()                
            ],
            sorted_on="No  .  ",
            sorted_order="ASC"
            )   
        self.layout.add_widget(self.table)
        scroll_view = ScrollView(do_scroll_x=True) 
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)
        
        self.table.bind(on_check_press=self.handle_check_press)
        self.you_delete_row = []
        
        delete_button = MDRaisedButton(
            text="Delete",
            md_bg_color="red",
            on_release=self.handle_delete_press    
            )
        self.add_widget(delete_button)   
                
    def handle_check_press(self, instance_table, current_row):
        row_data = current_row[0]
        if current_row[-1]:
            self.you_delete_row.append(row_data)    
        else:
            try:
                self.you_delete_row.remove(row_data)     
            except ValueError as err:
                print(err)
            else:
                del data[row_data]
        #print(len(self.you_delete_row), self.you_delete_row)
         
    def handle_delete_press(self, instance_button):
        if not self.you_delete_row:
            return
        dialog = MDDialog(
            text="Age you sure for delete ? ",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args:dialog.dismiss(),                   
                    ),
                MDFlatButton(
                    text="Delete",
                    on_release=lambda *args:self.handle_delete_confirm(dialog)    
                    ),                    
                ]
            )
        dialog.open()
            
    def handle_delete_confirm(self, dialog):
        for row_data in self.you_delete_row:
            del data[row_data]
            if self.table.row_data:
                self.table.row_data = [ row for row in self.table.row_data if row[0] != row_data ]                
            else:
                self.table.row_data = []
        self.you_delete_row = []        
        dialog.dismiss()
        Snackbar(
            text="You succes remowe",
            pos_hint={"top": 1},
            snackbar_y="10dp",
            bg_color=(1, 0, 0, 1)
            ).open()
        

class ExampleApp(MDApp):
    def build(self):
        return MainScreen()


ExampleApp().run()