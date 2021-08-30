import socket
import ssl
HOST = '10.30.164.55'
PORT = 1234
# context = ssl.create_default_context()
# context.load_verify_locations('cert.pem')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected!')
    s.sendall(b'Test!!!!')