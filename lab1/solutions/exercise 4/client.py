import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"10 15 5 18 23 111 18")         # sum = 200
    data = s.recv(1024)
    

print(f"Sum is: {float(data.decode())}")

