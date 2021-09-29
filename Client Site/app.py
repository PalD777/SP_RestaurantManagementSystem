import time
import json
import requests
import qrcode
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = 'Secret Key 123'

PORT = 5000

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        qty, item_id = request.form.values()
        update_cart([(item_id, qty)], mode='add')
        return ''
    else:
        menu = get_menu()
        return render_template("index.html", menu=menu)

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    # Initialise cart if not defined
    if 'cart' not in session:
        session['cart'] = {}

    if request.method == 'POST':
        if request.form['action'] == 'save':
            update_cart(request.form.items())
        elif request.form['action'] == 'checkout':
            update_cart(request.form.items())
            print('Checking out with: ', session['cart'])
            session['cart'] = {}
            # Server socket networking here

    return render_template("cart.html", cart=generate_cart(), total=find_total_cost())

@app.route("/qr")
def qr():
    ip = requests.get('https://api.ipify.org').text
    print(ip)
    img = qrcode.make(f'http://{ip}:{PORT}')
    img.save('static/images/qr.png')
    return render_template('qr.html')

# ---- HELPER FUNCTIONS ---- #
def get_menu():
    with open('menu.json') as menu_file:
        return json.load(menu_file)

def generate_cart():
    cart = []
    for item_id, qty in session['cart'].items():
        item = get_item_from_id(item_id)
        item['qty'] = qty
        cart.append(item)
    return cart

def get_item_from_id(item_id):
    menu = get_menu()
    for item in menu:
        if item['id'] == item_id:
            return item
    else:
        return None

def find_total_cost():
    total = 0
    for item_id, qty in session['cart'].items():
        price = get_item_from_id(item_id)['price']
        total += price * qty
    return total

def update_cart(data, mode='replace'):
    '''Helper function to update the cart based on data passed'''
    if 'cart' not in session:
        session['cart'] = {}

    for item_id, qty in data:
        if item_id == 'action': continue
        # Basic Input Validation
        if not qty.isdigit or int(qty) < 0 or get_item_from_id(item_id) is None:
            return """Invalid Request
            <a href='/'>Go back to main page</a>""", 400    # 400 = BadReques
        if mode == 'add':
            qty = session['cart'].get(item_id, 0) + int(qty)
        else:
            qty = int(qty)

        if qty == 0:
            del session['cart'][item_id]
        else:
            session['cart'][item_id] = qty
        session.modified = True     # To tell flask that a mutable object in session was changed


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True, use_evalex=False)
