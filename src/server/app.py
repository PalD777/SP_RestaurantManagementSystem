from kivy.app import App
from kivy.logger import ColoredFormatter 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial


class InnerLayout(GridLayout):
    '''Contains all the app contents'''
    orders = ListProperty()
    index = NumericProperty(0)

    def update(self, dt = 0):
        '''
        Keep the list of items updated
        TODO
        Beautify Buttons
        '''
        self.orders = self.get_orders()
        for item in self.orders[self.index:]:
            btn = Button(text = item[0],
                         font_size = 40,
                         background_color =[1, 0, 0, 3])
            btn2 = Button(background_normal = 'cancel.png',
                          size_hint_x = None,
                          size = (144, 144))

            btn.bind(on_release=partial(show_popup, item[1]))
            btn2.bind(on_release=partial(self.remove, item, btn))

            self.add_widget(btn)
            self.add_widget(btn2)
            self.index += 1
    
    def get_orders(self):
        '''
        Temporary code to use json to get orders.
        TODO
        Make sure it get order.json from its own directory
        Later, will use MySQL to connect to the orders database to retrieve all orders which have
        the boolean has served false
        '''
        import json
        try:
            with open('orders.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open('orders.json', 'w') as f:
                json.dump([], f)
            return []

    def remove(self, item, btn, exitbtn):
        '''
        Callback function to delete a row on pressing cancel button
        TODO
        Update MySQL database to change has_served to true if pressed
        '''
        self.remove_widget(btn)
        self.remove_widget(exitbtn)

class Order_Details(FloatLayout):
    '''Layout for popup contents containing order information'''
    popup = None
    text1 = StringProperty()
    def dismiss(self):
        '''Callback for closing popup'''
        Order_Details.popup.dismiss()

    def generate_text(self, bill_id):
        '''
        TODO
        Retrieve order information and format and display it
        '''
        self.text1 = f'ORDER ID IS {bill_id}'


class RestaurantServerApp(App):    
    '''Main App'''
    def build(self):
        '''Set the base layout and functionality'''
        root = ScrollView() # Allow scrolling
        main = InnerLayout(cols = 2,
                    cols_minimum = {0: 400, 1: 150},
                    row_default_height = 144,
                    padding = ('0dp', '1dp', '0dp', '0dp'),
                    size_hint = (1, None))
        main.bind(minimum_height=main.setter('height')) # Adjust height so scroll updates with resize
        main.update() # Update at start
        Clock.schedule_interval(main.update, 10) # Call update every 10 seconds
        root.add_widget(main)
        return root

def show_popup(bill_id, _):
    '''Generate order information in a popup'''
    show = Order_Details()
    show.generate_text(bill_id)
    popupWindow = Popup(title="Order", content=show, size=(400,400))
    Order_Details.popup = popupWindow
    popupWindow.open()

root = RestaurantServerApp() 

root.run()