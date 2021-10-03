import socket
import base64, json
from pathlib import Path
import mysql.connector
class Server:
    def __init__(self, port=9999):
        self.HOST = ''
        self.PORT = port
        self.tables = {}
        self.get_menu()
    
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
            menu = self.get_menu()
            return f'MENU REPLY {json.dumps(menu)}'.encode('utf-8')
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
                if self.parse_orders(table, order) == 200:
                    return b'ORDER RECEIVED'
                else:
                    return b'ORDER ERROR 500'
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

    def get_menu(self):
        '''should be list of dictionary preferably'''
        mydb = mysql.connector.connect(
                host="localhost",
                user="server",
                password="SP12345",
                database = "restaurant"
            )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM menu")
        myresult = mycursor.fetchall()
        self.menu = []
        for item in myresult:
            self.menu.append({'id':item[0],'name':item[1],'desc':item[2],'price':float(item[3]),'img':item[4]})
        return self.menu
    

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

    def parse_orders(self, table, order):
        mydb = mysql.connector.connect(
                host="localhost",
                user="server",
                password="SP12345",
                database = "restaurant"
            )
        mycursor = mydb.cursor()
        sql = "INSERT INTO orders (table_num, total, items) VALUES (%s, %s, %s)"
        print('inserting')
        total = 0
        items = []
        for item_id, qty in order.items():
            item = self.get_item_from_id(item_id)
            if not str(qty).isdigit() or item is None:
                continue
            total += item['price'] * int(qty)
            items.append({
                'id': item_id,
                'name': item['name'],
                'qty': int(qty),
                'price': item['price']
                })
        print(items)
        print(total)
        mycursor.execute(sql, (table, total, json.dumps(items)))
        mydb.commit()
        return 200

    def quit(self):
        self.sock.close()

if __name__ == '__main__':
    server = Server()
    server.start()
    server.handle_conn()
    server.quit()
