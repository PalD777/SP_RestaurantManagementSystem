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
            if self.addr not in self.tables:
                if len(self.tables) == 0:
                    TABLE = 1
                else:
                    TABLE = max(self.tables.keys()) + 1
                self.tables[self.addr] = TABLE
            else:
                TABLE = self.tables[self.addr]

            return f'PING REPLY TABLE {TABLE}'.encode('utf-8')
        else:
            print('[!] Invalid PING request')
            print(b' '.join(req))
            return b'PING ERROR 400'

    def handle_menu(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            # data:image/jpeg;base64,
            for item in self.menu:
                print(Path(__file__))
                file_paths = list(Path(__file__).parent.glob(f'images/{item["id"]}.*'))
                if len(file_paths) == 0:
                    return b'MENU ERROR 502'
                else:
                    file_path = file_paths[0]
                item['img'] = self.base64_img(file_path)
                
            return f'MENU REPLY {json.dumps(self.menu)}'.encode('utf-8')
        else:
            print('[!] Invalid MENU request')
            print(b' '.join(req))
            return b'MENU ERROR 400'

    def handle_order(self, req):
        return b'ORDER ERROR 501'

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

    def quit(self):
        self.sock.close()

if __name__ == '__main__':
    server = Server()
    server.start()
    server.handle_conn()
    server.quit()
