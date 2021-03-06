import mysql.connector
from pathlib import Path
import base64
import argparse


menu = [
    {'id': 'A001', 'price': 4, 'name': 'Crispy Fries',
        'desc': 'Potato wedges deep fried to a golden crispiness.'},
    {'id': 'A002', 'price': 6, 'name': 'American Hamburger',
     'desc': 'American-styled patty sandwiched between ham and buns.'},
    {'id': 'B003', 'price': 11, 'name': 'Chocolate Fountain',
     'desc': 'Fluffy Marshmallow with dark chocolate fondue.'},
    {'id': 'B001', 'price': 28, 'name': 'Strawberry Cake',
     'desc': 'Soft cake with lush strawberry topping and premium cream'},
    {'id': 'F003', 'price': 7, 'name': 'Rose Drink',
     'desc': 'Sweet rose flavoured exclusive drink'},
    {'id': 'R001', 'price': 19, 'name': 'Chicken Roast',
     'desc': 'Crisp and roasted chicken with barbeque sauce'},
    {'id': 'A007', 'price': 21, 'name': 'Italian spaghetti',
     'desc': 'Fine spaghetti with exotic herb and mayo topping.'},
]


def add_images():
    '''Adds images to menu items'''
    for item in menu:
        file_paths = list(Path(__file__).parent.glob(f'images/{item["id"]}.*'))
        if len(file_paths) == 0:
            # No image found for a menu item - use a 404 picture
            file_path = Path(__file__).parent / 'images' / '404.jpg'
        else:
            file_path = file_paths[0]
        item['img'] = base64_img(file_path)
    return menu


def base64_img(file_path):
    '''Helper function to convert image into base64 content'''
    with open(file_path, mode='rb') as image_file:
        img = image_file.read()
    if file_path.suffix in ['.jpeg', '.jpg', '.jfif', '.pjpeg', '.pjp']:
        suffix = '.jpeg'
    else:
        suffix = file_path.suffix
    return f'data:image/{suffix[1:]};base64,' + base64.b64encode(img).decode('utf-8')


def change_menu():
    '''Runs SQL queries to clear table and insert the new menu data'''
    add_images()
    mydb = mysql.connector.connect(
        host="localhost",
        user="server",
        password="SP12345",
        database="restaurant"
    )
    mycursor = mydb.cursor()
    # Clear all existing entries
    sql1 = "TRUNCATE TABLE menu"
    mycursor.execute(sql1)
    mydb.commit()
    # Add the new entries from the menu variable
    sql = "INSERT INTO menu (id, item, descr, price, img) VALUES (%s, %s, %s, %s, %s)"
    val = []
    for item in menu:
        val.append((item['id'], item['name'], item['desc'],
                   item['price'], item['img']))
    mycursor.executemany(sql, val)
    mydb.commit()
    print('[*] Menu has been updated')


def reset_orders():
    '''Deletes all orders and resets auto increment'''
    mydb = mysql.connector.connect(
        host="localhost",
        user="server",
        password="SP12345",
        database="restaurant"
    )
    mycursor = mydb.cursor()
    # Clear all existing entries and reset auto increment
    sql1 = "TRUNCATE TABLE orders"
    mycursor.execute(sql1)
    mydb.commit()
    print('[*] Orders have been reset')


if __name__ == "__main__":
    # Adds command line arg for choosing what to modify
    parser = argparse.ArgumentParser(
        description='Helper utility for modifying S&P Restaurant SQL Database')
    parser.add_argument('target', choices=['menu', 'orders', 'both'], metavar='modification_target',
                        help='Specifies what to modify. Possible values: menu, orders, both')
    args = parser.parse_args()
    if args.target in ['menu', 'both']:
        change_menu()
    if args.target in ['orders', 'both']:
        reset_orders()
