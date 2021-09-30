import socket
import base64, json
from pathlib import Path
class Server:
    def __init__(self, port=9999):
        self.HOST = ''
        self.PORT = port
        self.tables = {}
        self.menu = [
                    {'id': 'A001', 'price':4, 'name': 'Crispy Fries', 'desc': 'Potato wedges deep fried to a golden crispiness.'},
                    {'id': 'A002', 'price':6, 'name': 'American Hamburger', 'desc': 'American-styled patty sandwiched between ham and buns.'},
                    {'id': 'B003', 'price':11, 'name': 'Chocolate Fountain', 'desc': 'Fluffy Marshmallow with dark chocolate fondue.'},
                    {'id': 'B001', 'price':28, 'name': 'Strawberry Cake', 'desc': 'Soft cake with lush strawberry topping and premium cream'},
                    {'id': 'F003', 'price':7, 'name': 'Rose Drink', 'desc': 'Sweet rose flavoured exclusive drink'},
                    {'id': 'R001', 'price':19, 'name': 'Chicken Roast', 'desc': 'Crisp and roasted chicken with barbeque sauce'},
                    {'id': 'A007', 'price':21, 'name': 'Italian spaghetti', 'desc': 'Fine spaghetti with exotic herb and mayo topping.'},
                    ]
        self.orders = self.get_orders()
    
    def start(self, max_clients=128, timeout=10):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(max_clients)
        self.sock.settimeout(timeout)
        print(f'[*] Server running on {self.get_ip()}:{self.PORT}')

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        s.close()
        return IP

    def handle_ping(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            return f'PING REPLY TABLE {self.get_table()}'.encode('utf-8')
        else:
            print('[!] Invalid PING request')
            print(b' '.join(req))
            return b'PING ERROR 400'

    def handle_menu(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            for item in self.menu:
                # Get all files with the same name as the id
                file_paths = list(Path(__file__).parent.glob(f'images/{item["id"]}.*'))
                if len(file_paths) == 0:
                    return b'MENU ERROR 502'    # No image found for a menu item
                else:
                    file_path = file_paths[0]
                item['img'] = self.base64_img(file_path)
                
            return f'MENU REPLY {json.dumps(self.menu)}'.encode('utf-8')
        else:
            print('[!] Invalid MENU request')
            print(b' '.join(req))
            return b'MENU ERROR 400'

    def handle_order(self, req):
        if len(req) > 3 and req[1].upper() == b'SEND' and req[2].isdigit():
            try:
                table = req[2].decode('utf-8')
                order = json.loads(b' '.join(req[3:]))
                print(order)
                if not isinstance(order, dict) or len(order) == 0:
                    return b'ORDER ERROR 400'
                ORDER_ID = self.parse_orders(table, order)
                # Add to SQL here
                with open(Path(__file__).parent / 'orders.json', 'w') as order_file:
                    json.dump(self.orders, order_file)
                return b'ORDER RECEIVED'
            except json.JSONDecodeError:
                print("[!] Couldn't decode JSON")
                print(b' '.join(req))
                return b'ORDER ERROR 400'
        else:
            print('[!] Invalid ORDER request')
            print(b' '.join(req))
            return b'ORDER ERROR 400'

    def handle_conn(self):
        while True:
            try:
                self.conn, addr = self.sock.accept()
                self.addr = addr[0]
                print(self.addr)
                with self.conn:
                    req = self.conn.recv(2048).strip().split(b' ')
                    if len(req) == 0:
                        continue
                    protocol = req[0].upper()
                    if protocol == b'PING':
                        resp = self.handle_ping(req)
                    elif protocol == b'MENU':
                        resp = self.handle_menu(req)
                    elif protocol == b'ORDER':
                        resp = self.handle_order(req)
                    else:
                        self.conn.sendall(b'PROTOCOL ERROR 400')
                    print(req)
                    print(resp[:80])
                    self.conn.sendall(resp)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break

    @staticmethod
    def base64_img(file_path):
        with open(file_path, mode='rb') as image_file:
            img = image_file.read()
        if file_path.suffix in ['.jpeg', '.jpg', '.jfif', '.pjpeg', '.pjp']:
            suffix = '.jpeg'
        else:
            suffix = file_path.suffix
        return f'data:image/{suffix[1:]};base64,' + base64.b64encode(img).decode('utf-8')

    def get_table(self):
        if self.addr not in self.tables:
            if len(self.tables) == 0:
                TABLE = 1
            else:
                TABLE = max(self.tables.keys()) + 1
            self.tables[self.addr] = TABLE
        else:
            TABLE = self.tables[self.addr]
        return TABLE

    def get_item_from_id(self, item_id):
        for item in self.menu:
            if item['id'] == item_id:
                return item
        else:
            return None

    @staticmethod
    def get_orders():
        '''
        Temporary code to use json to get orders.
        TODO
        Make sure it get order.json from its own directory
        Later, will use MySQL to connect to the orders database to retrieve all orders which have
        the boolean has served false
        When MySQL, just need this to find highest ORDER_ID (optional: that hasn't been served - would need another primary key in that case. UID generator?)
        '''
        import json
        # Orders = {order_id<str>:{table<int>:, total<float>:, order_done<bool>:, items:[{id<str>:, name<str>:, qty<int>:, price<float>:}]}}
        try:
            with open(Path(__file__).parent / 'orders.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(Path(__file__).parent / 'orders.json', 'w') as f:
                json.dump({}, f)
            return {}

    def parse_orders(self, table, order):
        # {order_id<str>:{table<int>:, total<float>:, order_done<bool>:, items:[{id<str>:, name<str>:, qty<int>:, price<float>:}]}}
        if len(self.orders) == 0:
            ORDER_ID = 1
        else:
            ORDER_ID = max(map(lambda x: int(x), self.orders.keys())) + 1
        ORDER_ID = str(ORDER_ID)
        self.orders[ORDER_ID] = {'table':table, 'total':0, 'order_done': False, 'items':[]}
        print(order)
        for item_id, qty in order.items():
            item = self.get_item_from_id(item_id)
            if not str(qty).isdigit() or item is None:
                continue
            self.orders[ORDER_ID]['total'] += item['price'] * int(qty)
            self.orders[ORDER_ID]["items"].append({
                'id': item_id,
                'name': item['name'],
                'qty': int(qty),
                'price': item['price']
                })
            print(self.orders)
        return ORDER_ID

    def quit(self):
        self.sock.close()

if __name__ == '__main__':
    server = Server()
    server.start()
    server.handle_conn()
    server.quit()
