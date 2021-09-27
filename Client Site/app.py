import time
import json
import requests
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = 'Secret Key 123'
menu = [
    {'id': 'A001', 'price':4, 'name': 'Crispy Fries', 'description': 'Potato wedges deep fried to a golden crispiness.', 'image_url':'images/menu-item-01.jpg'},
    {'id': 'A002', 'price':6, 'name': 'American Hamburger', 'description': 'American-styled patty sandwiched between ham and buns.', 'image_url':'images/menu-item-02.jpg'},
    {'id': 'B003', 'price':11, 'name': 'Chocolate Fountain', 'description': 'Fluffy Marshmallow with dark chocolate fondue.', 'image_url':'images/menu-item-01.jpg'},
    {'id': 'B001', 'price':28, 'name': 'Strawberry Cake', 'description': 'Soft cake with lush strawberry topping and premium cream', 'image_url':'images/menu-item-02.jpg'},
    {'id': 'F003', 'price':7, 'name': 'Rose Drink', 'description': 'Sweet rose flavoured exclusive drink', 'image_url':'images/menu-item-02.jpg'},
    {'id': 'R001', 'price':19, 'name': 'Chicken Roast', 'description': 'Crisp and roasted chicken with barbeque sauce', 'image_url':'images/menu-item-03.jpg'},
    {'id': 'A007', 'price':21, 'name': 'Italian spaghetti', 'description': 'Fine spaghetti with exotic herb and mayo topping.', 'image_url':'images/menu-item-04.jpg'},

]

@app.route("/", methods=['GET', 'POST'])
def home():
    # Key --> Name, Value --> Value
    if request.method == 'POST':
        print(list(request.form.values()))
        qty, item_id = request.form.values()
        if 'cart' not in session:
            session['cart'] = {}
        if not qty.isdigit or int(qty) <= 0:
            print('Error!', qty)
            return "Invalid Request\n<a href='/'>Go back to main page</a>", 400
        qty = int(qty)
        session['cart'][item_id] = session['cart'].get(item_id, 0) + qty
        session.modified = True
        print(session)
    return render_template("index.html", menu=menu)

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    # Key --> Name, Value --> Value
    if request.method == 'POST':
        print(list(request.form.values()))
        qty, item_id = request.form.values()
        if 'cart' not in session:
            session['cart'] = {}
        if not qty.isdigit or int(qty) <= 0:
            print('Error!', qty)
            return "Invalid Request\n<a href='/'>Go back to main page</a>", 400
        qty = int(qty)
        session['cart'][item_id] = session['cart'].get(item_id, 0) + qty
        session.modified = True
        print(session)
    return render_template("cart.html", menu=menu)

if __name__ == "__main__":
    app.run(debug=True)
