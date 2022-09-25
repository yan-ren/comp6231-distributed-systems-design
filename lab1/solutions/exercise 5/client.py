import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Very Long Message "*200 + b"<EOF>")
    data = bytearray()
    while True:                             # keep receiving until we get '<EOF>'
        packet = s.recv(1024)
        data.extend(packet)
        if packet.decode()[-5:] == '<EOF>':
            data = data[:-5]
            break
    
    
print(f"Server says: {data.decode()}")

