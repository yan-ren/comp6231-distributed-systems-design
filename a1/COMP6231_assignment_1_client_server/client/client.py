import socket


EOF_TOKEN_SIZE = 10
BUFFER_SIZE = 1024

def receive_message_ending_with_token(active_socket, buffer_size, eof_token):
    """
    Same implementation as in receive_message_ending_with_token() in server.py
    A helper method to receives a bytearray message of arbitrary size sent on the socket.
    This method returns the message WITHOUT the eof_token at the end of the last packet.
    :param active_socket: a socket object that is connected to the server
    :param buffer_size: the buffer size of each recv() call
    :param eof_token: a token that denotes the end of the message.
    :return: a bytearray message with the eof_token stripped from the end.
    """
    data = bytearray()
    while True:                             # keep receiving until we get eof_token
        packet = active_socket.recv(buffer_size)
        data.extend(packet)
        if packet.decode()[-len(eof_token):] == eof_token:
            data = data[:-len(eof_token)]
            break

    return data


def initialize(host, port):
    """
    1) Creates a socket object and connects to the server.
    2) receives the random token (10 bytes) used to indicate end of messages.
    3) Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param host: the ip address of the server
    :param port: the port number of the server
    :return: the created socket object
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('Connected to server at IP:', host, 'and Port:', port)

    eof_token = bytearray()
    while True:
        packet = s.recv(BUFFER_SIZE)
        eof_token.extend(packet)
        if len(eof_token) == EOF_TOKEN_SIZE:
            eof_token = eof_token.decode()
            print('Handshake Done. EOF is:', eof_token)
            break

    data = receive_message_ending_with_token(s, BUFFER_SIZE, eof_token)
    print(data.decode())
    return s, eof_token


def issue_cd(command_and_arg, client_socket, eof_token):
    """
    Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


def issue_mkdir(command_and_arg, client_socket, eof_token):
    """
    Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


def issue_rm(command_and_arg, client_socket, eof_token):
    """
    Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


def issue_ul(command_and_arg, client_socket, eof_token):
    """
    Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
    and sends it to the server. The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


def issue_dl(command_and_arg, client_socket, eof_token):
    """
    Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
    socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
    the server.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    :return:
    """
    raise NotImplementedError('Your implementation here.')


def pack_msg(msg: str, eof_token: str):
    return str.encode(msg) + str.encode(eof_token)


def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    # initialize
    s, eof_token = initialize(HOST, PORT)
    while True:
        # get user input
        user_input = input("$> ")

        # call the corresponding command function or exit
        if user_input == 'exit':
            s.sendall(pack_msg(user_input, eof_token))
            break

    print('Exiting the application.')


if __name__ == '__main__':
    main()