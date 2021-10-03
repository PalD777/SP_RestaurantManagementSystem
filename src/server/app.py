from kivy.app import App
from kivy.logger import ColoredFormatter 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, DictProperty
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial
from pathlib import Path
import mysql.connector
import json

class InnerLayout(GridLayout):
    '''Contains all the app contents'''
    orders = DictProperty()
    curr_order = NumericProperty(0)

    def update(self, dt = 0):
        '''
        Keep the list of items updated
        TODO
        Beautify Buttons
        '''
        self.orders = self.get_orders()
        orders = sorted(filter(lambda x: str(x[0]).isdigit(), self.orders.items()), key=lambda x: int(x[0]))
        for order_id, details in orders:
            # When using SQL later, remove order_done verification from here as it will be handled in query
            self.curr_order = int(order_id)
            btn = Button(text = f'ORDER {order_id}',
                         font_size = 40,
                         background_color =[1, 0, 0, 3])
            btn2 = Button(background_normal = 'cancel.png',
                          size_hint_x = None,
                          size = (144, 144))

            btn.bind(on_release=partial(show_popup, details))
            btn2.bind(on_release=partial(self.remove, order_id, btn))

            self.add_widget(btn)
            self.add_widget(btn2)
    
    def get_orders(self):
        '''
        Temporary code to use json to get orders.
        TODO
        Make sure it get order.json from its own directory
        Later, will use MySQL to connect to the orders database to retrieve all orders which have
        the boolean has served false
        '''
        mydb = mysql.connector.connect(
                host="localhost",
                user="server",
                password="SP12345",
                database = "restaurant"
            )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM orders WHERE order_done = 0 AND id > %s", (self.curr_order,))
        myresult = mycursor.fetchall()
        orders = {}
        for item in myresult:
            orders[item[0]] = {'id':item[0], 'table_num':item[1], 'total':float(item[2]),'items':json.loads(item[4])}
        return orders

    def remove(self, item, btn, exitbtn):
        '''
        Callback function to delete a row on pressing cancel button
        TODO
        Update MySQL database to change has_served to true if pressed
        '''
        mydb = mysql.connector.connect(
                host="localhost",
                user="server",
                password="SP12345",
                database = "restaurant"
            )
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE orders SET order_done = TRUE WHERE id = %s", (item,))
        mydb.commit()
        self.remove_widget(btn)
        self.remove_widget(exitbtn)

class Order_Details(FloatLayout):
    '''Layout for popup contents containing order information'''
    popup = None
    text1 = StringProperty()
    text2 = StringProperty()
    text3 = StringProperty()
    def dismiss(self):
        '''Callback for closing popup'''
        Order_Details.popup.dismiss()

    def generate_text(self, details):
        '''
        TODO
        Retrieve order information and format and display it
        '''
        self.text1 = f'Table Number: {details["table_num"]}'
        self.text2 = f"{'ID':<5} {'Item Name':<20} {'Qty':<3} {'Price':<6}\n"
        for item in details['items']:
            self.text2 += f"{item['id']:<5} {item['name']:<20} {item['qty']:>3} ${item['price']:<5}\n"
        self.text3 = f'Total: ${details["total"]}'


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