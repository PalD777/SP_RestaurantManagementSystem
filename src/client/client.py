import socket
import base64
import json
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
import argparse
from threading import Thread
from waitress import serve
from app import app


class Client:
    def __init__(self, host='127.0.0.1', port=9999, flask_app=None):
        self.HOST = host
        self.PORT = port
        self.flask_app = flask_app
        self.table = None

    def send(self, msg):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.HOST, self.PORT))
                print('[*] Connection Established!')
                sock.sendall(msg)
                return self.recvall(sock)
        except ConnectionRefusedError:
            protocol = msg.strip().split(b' ')[0].upper()
            return protocol + b' ERROR 503'
        except Exception as e:
            raise e

    def recvall(self, sock, BUFF_SIZE=4096):
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:  # if it has ended
                break
        return data

    def handle_ping(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            resp = self.send(b' '.join(req)).upper().split()
            resp_is_valid = len(
                resp) == 4 and resp[0] == b'PING' and resp[1] == b'REPLY' and resp[2] == b'TABLE' and resp[3].isdigit()
            resp_is_error = len(
                resp) == 3 and resp[0] == b'PING' and resp[1] == b'ERROR' and resp[2].isdigit()

            if resp_is_error:
                return int(resp[2]), None
            elif resp_is_valid:
                self.table = int(resp[3])
                return 200, self.table
            else:
                print('[!] Invalid server response')
                print(f"[!] Response: {b' '.join(resp).decode('utf-8')}")
                return 502, None
        else:
            print('[!] Invalid PING request')
            print(f"[!] Request: {b' '.join(req).decode('utf-8')}")
            return 400, None

    def handle_menu(self, req):
        if len(req) == 2 and req[1].upper() == b'REQUEST':
            resp = self.send(b' '.join(req)).split(b' ')
            resp_is_valid = resp[0].upper(
            ) == b'MENU' and resp[1].upper() == b'REPLY'
            resp_is_error = len(resp) == 3 and resp[0].upper(
            ) == b'MENU' and resp[1].upper() == b'ERROR' and resp[2].isdigit()

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
                    print(f"[!] Response: {b' '.join(resp).decode('utf-8')}")
                    return 502, None
            else:
                print('[!] Invalid server response')
                print(f"[!] Response: {b' '.join(resp).decode('utf-8')}")
                return 502, None
        else:
            print('[!] Invalid MENU request')
            print(f"[!] Request: {b' '.join(req).decode('utf-8')}")
            return 400, None

    def handle_order(self, req):
        if len(req) > 2 and req[1].upper() == b'SEND':
            req.insert(2, str(self.table).encode('utf-8'))
            resp = self.send(b' '.join(req)).split(b' ')
            resp_is_valid = len(resp) == 2 and resp[0].upper(
            ) == b'ORDER' and resp[1].upper() == b'RECEIVED'
            resp_is_error = len(resp) == 3 and resp[0].upper(
            ) == b'ORDER' and resp[1].upper() == b'ERROR' and resp[2].isdigit()

            if resp_is_error:
                return int(resp[2]), None
            elif not resp_is_valid:
                print('[!] Invalid server response')
                print(f"[!] Response: {b' '.join(resp).decode('utf-8')}")
                return 502, None
            else:
                return 200, None
        else:
            print('[!] Invalid ORDER request')
            print(f"[!] Request: {b' '.join(req).decode('utf-8')}")
            return 400, None

    def update_menu(self):
        print('[*] Updating menu')
        self.handle_menu(b'MENU REQUEST'.split())

    @staticmethod
    def error_warning(status, data):
        if status != 200:
            print(f"[!] ERROR - Encounted status {status}")
        return data

    def main(self):
        with open(Path(__file__).parent / 'requests.bin', 'w+b') as f:
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.update_menu, 'interval', minutes=2)
            scheduler.start()

            self.error_warning(*self.handle_ping(b'PING REQUEST'.split()))
            self.error_warning(*self.handle_menu(b'MENU REQUEST'.split()))

            while True:
                req = f.readline().strip().split(b' ')
                if req == [b'']:
                    continue
                protcol = req[0].upper()
                print(f'[*] Sending {protcol.decode("utf-8")} request')
                if protcol == b'PING':
                    self.error_warning(*self.handle_ping(req))
                elif protcol == b'MENU':
                    self.error_warning(*self.handle_menu(req))
                elif protcol == b'ORDER':
                    self.error_warning(*self.handle_order(req))
                else:
                    print('[!] Unknown request protocol')
                    print(f"[!] Request: {b' '.join(req).decode('utf-8')}")


def serve_app(app, port):
    serve(app, port=port, threads=10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run the client for S&P Restaurant App')
    parser.add_argument('-s', '--sip', '--server-ip', default='127.0.0.1',
                        help='Specifies Server IP Address', dest='ip')
    parser.add_argument('-p', '--sp', '--s-port', '--server-port', default='9999',
                        type=int, help='Specifies Server port', dest='server_port')
    parser.add_argument('-f', '--fp', '--f-port', '--flask-ip', default='5000',
                        type=int, help='Specifies Flask App port', dest='flask_port')
    args = parser.parse_args()
    flask_app = Thread(target=serve_app, args=(
        app, args.flask_port), daemon=True)
    flask_app.start()
    client = Client(args.ip, args.server_port, flask_app)
    client.main()
