import socket

HOST = "127.0.0.1"  # localhost
PORT = 65432  # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = bytearray()
        while True:                             # keep receiving until we get '<EOF>'
            packet = conn.recv(1024)
            data.extend(packet)
            if packet.decode()[-5:] == '<EOF>':
                data = data[:-5]
                break
            
        message = f'I got "{data.decode()}" from you and I am sending it back.<EOF>'
        conn.sendall(str.encode(message))