import socket
import ssl

class Server:
    def __init__(self, port=9999):
        self.HOST = ''
        self.PORT = port
        # self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # self.context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    
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

    def handle_conn(self):
        while True:
            conn, addr = self.sock.accept()
            with conn:
                print(f'[*] Connected by {addr[0]}:{addr[1]}')
                print(conn.recv(1024).decode('utf-8'))
                conn.sendall(b'HTTP/1.0 200 OK\n')
                conn.sendall(b'Content-Type: text/html\n\n')
                conn.sendall(b'<b>TEST</b>')

    def quit(self):
        self.sock.close()

if __name__ == '__main__':
    server = Server()
    server.start()
    server.handle_conn()
    server.quit()



'''
PING -
MENU -
ORDER <order obj> -


'''