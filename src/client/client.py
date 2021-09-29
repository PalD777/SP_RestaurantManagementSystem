import socket
import base64, json
from pathlib import Path

class Client:
    def __init__(self, host='127.0.0.1', port=9999, app_port=5000):
        self.HOST = host
        self.PORT = port
        self.APP_PORT = app_port
        self.table = None
    
    def send(self, msg):
        print(msg)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.HOST, self.PORT))
                print('Connected!')
                sock.sendall(msg)
                return self.recvall(sock)
        except Exception as e:
            raise e

    def recvall(self, sock, BUFF_SIZE=4096):
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE: # if it has ended
                break
        return data

    def handle_ping(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            resp = self.send(b' '.join(req)).upper().split()
            resp_is_valid = len(resp) == 4 and resp[0] == b'PING' and resp[1] == b'REPLY' and resp[2] == b'TABLE' and resp[3].isdigit()
            resp_is_error = len(resp) == 3 and resp[0] == b'PING' and resp[1] == b'ERROR' and resp[2].isdigit()

            if resp_is_error:
                return int(resp[2]), None
            elif resp_is_valid:
                self.table = int(resp[3])
                return 200, self.table
            else:
                print('[!] Invalid server response')
                print(b' '.join(resp))
                return 502, None
        else:
            print('[!] Invalid PING request')
            print(b' '.join(req))
            return 400, None

    def handle_menu(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            resp = self.send(b' '.join(req)).split(b' ')
            resp_is_valid = resp[0].upper() == b'MENU' and resp[1].upper() == b'REPLY'
            resp_is_error = len(resp) == 3 and resp[0].upper() == b'MENU' and resp[1].upper() == b'ERROR' and resp[2].isdigit()

            if resp_is_error:
                return int(resp[2]), None
            elif resp_is_valid:
                try:
                    menu = json.loads(b' '.join(resp[2:]))
                    # Menu = [{id:, name:, desc:, price:, img:(As base64)}]
                    with open(Path(__file__).parent / 'menu.json', 'w') as menu_file:
                        json.dump(menu, menu_file)
                    return 200, menu
                except json.JSONDecodeError:
                    print("[!] Couldn't decode JSON")
                    print(b' '.join(resp))
                    return 502, None
            else:
                print('[!] Invalid server response')
                print(b' '.join(resp))
                return 502, None
        else:
            print('[!] Invalid MENU request')
            print(b' '.join(req))
            return 400, None

    def handle_order(self, req):
        if len(req) > 2 and req[1].upper() == b'SEND':
            req.insert(2, str(self.table).encode('utf-8'))
            resp = self.send(b' '.join(req)).split(b' ')
            resp_is_valid = len(resp) == 2 and resp[0].upper() == b'ORDER' and resp[1].upper() == b'RECEIVED'
            resp_is_error = len(resp) == 3 and resp[0].upper() == b'ORDER' and resp[1].upper() == b'ERROR' and resp[2].isdigit()

            if resp_is_error:
                return int(resp[2]), None
            elif not resp_is_valid:
                print('[!] Invalid server response')
                print(b' '.join(resp))
                return 502, None
        else:
            print('[!] Invalid ORDER request')
            print(b' '.join(req))
            return 400, None

    def main(self):
        with open(Path(__file__).parent / 'requests.bin', 'w+b') as f:
            print(self.handle_ping(b'PING REQUEST'.split()))
            menu = self.handle_menu(b'MENU REQUEST'.split())
            print(str(menu)[:80])
            # Start Flask app here
            while True:
                req = f.readline().strip().split(b' ')
                if req == [b'']:
                    continue
                print(req)
                protcol = req[0].upper()
                print(protcol)
                if protcol == b'PING':
                    self.handle_ping(req)
                elif protcol == b'MENU':
                    self.handle_menu(req)
                elif protcol == b'ORDER':
                    self.handle_order(req)
                else:
                    print('[!] Unknown request protocol')
                    print(req)
                    print(b' '.join(req))

if __name__ == '__main__':
    client = Client()
    client.main()