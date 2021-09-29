import socket
import ssl

class Server:
    def __init__(self, port=9999):
        self.HOST = ''
        self.PORT = port
        self.tables = {}
    
    def start(self, max_clients=128):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(max_clients)
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
        pass

    def handle_order(self, req):
        pass

    def handle_conn(self):
        while True:
            self.conn, addr = self.sock.accept()
            self.addr = addr[0]
            print(self.addr)
            with self.conn:
                try:
                    req = self.conn.recv(2048).strip().split(b' ')
                    if len(req) == 0:
                        self.conn.sendadd(b'PROTOCOL ERROR 400')
                    protocol = req[0].upper()
                    if protocol == b'PING':
                        resp = self.handle_ping(req)
                    elif protocol == b'MENU':
                        resp = self.handle_menu(req)
                    elif protocol == b'ORDER':
                        resp = self.handle_order(req)
                    print(req)
                    print(resp)
                    self.conn.sendall(resp)
                except KeyboardInterrupt:
                    break

    def quit(self):
        self.sock.close()

if __name__ == '__main__':
    server = Server()
    server.start()
    server.handle_conn()
    server.quit()
