import socket

HOST = "127.0.0.1"  # localhost
PORT = 65432  # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:                     # handle all requests from the client
            data = conn.recv(1024)
            if not data:
                break
            message = f'I got "{data.decode()}" from you and I am sending it back.'
            conn.sendall(str.encode(message))