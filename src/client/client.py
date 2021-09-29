import socket
import base64, json
'''


MENU:
Sends: MENU REQUEST
Recv: MENU REPLY $MENU_OBJ
MENU_OBJ: Serialise via JSON or pickle [loaded from SQL DB]
    {Id:..., Name:..., Img:..., Desc:..., Price:...}

ORDER:
Sends: ORDER SEND $TABLE_NO $ORDER_OBJ
Recv: ORDER RECEIVED
ORDER_OBJ: Serialised via JSON
     {Name: Qty}


For errors:
$PROTOCOL ERROR $ERROR_CODE
'''
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
            resp_is_error = resp[0].upper() == b'MENU' and resp[1].upper() == b'ERROR' and resp[2].isdigit() and len(resp) == 3

            if resp_is_error:
                return int(resp[2]), None
            elif resp_is_valid:
                try:
                    menu = json.loads(b' '.join(resp[2:]))
                    # Menu = [{id:, name:, desc:, price:, img:(As base64)}]
                    with open('menu.json', 'w') as menu_file:
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
        pass

    def main(self):
        with open('requests.bin', 'w+b') as f:
            print(self.handle_ping(b'PING REQUEST'.split()))
            menu = self.handle_menu(b'MENU REQUEST'.split())
            print(str(menu)[:80])

            while True:
                req = f.readline().strip().split()
                if req == []:
                    continue
                protcol = req[0].upper()
                print(protcol)
                if protcol == b'PING':
                    handle_ping(req)
                elif protcol == b'MENU':
                    pass
                elif protcol == b'ORDER':
                    pass
                else:
                    print('[!] Unknown request protocol')
                    print(b' '.join(req))

if __name__ == '__main__':
    client = Client()
    client.main()