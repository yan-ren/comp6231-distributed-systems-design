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
    while True:  # keep receiving until we get eof_token
        packet = active_socket.recv(buffer_size)
        data.extend(packet)
        if packet[-len(eof_token):] == eof_token:
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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    print('Connected to server at IP:', host, 'and Port:', port)

    eof_token = bytearray()
    while True:
        packet = s.recv(BUFFER_SIZE)
        eof_token.extend(packet)
        if len(eof_token) == EOF_TOKEN_SIZE:
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
    client_socket.sendall(pack_msg(command_and_arg, eof_token))
    data = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    print(data.decode())


def issue_mkdir(command_and_arg, client_socket, eof_token):
    """
    Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    client_socket.sendall(pack_msg(command_and_arg, eof_token))
    data = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    print(data.decode())


def issue_rm(command_and_arg, client_socket, eof_token):
    """
    Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    client_socket.sendall(pack_msg(command_and_arg, eof_token))
    data = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    print(data.decode())


def issue_ul(command_and_arg, client_socket, eof_token):
    """
    Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
    and sends it to the server. The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    args = command_and_arg.split(' ')
    if len(args) != 2:
        print('invalid ul command: ' + command_and_arg + " , missing arguments")
        return

    try:
        file = open(args[1], 'rb')
        data = file.read()
        file.close()
    except OSError as e:
        print('could not open/read file ' + args[1] + ', error:' + str(e))
        return

    # sending the filename
    client_socket.sendall(pack_msg(command_and_arg, eof_token))
    # get response
    resp = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    print(resp.decode())
    # sending the file
    client_socket.sendall(data+eof_token)
    # get response
    resp = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    print(resp.decode())


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
    args = command_and_arg.split(' ')
    if len(args) != 2:
        print('invalid dl command: ' + command_and_arg + " , missing arguments")
        return

    # sending the dl command and file name
    client_socket.sendall(pack_msg(command_and_arg, eof_token))
    print('requesting file: ' + args[1])
    # get response
    resp = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    if resp.decode().startswith('error'):
        print(resp.decode())
        return

    # send request
    client_socket.sendall(pack_msg('ok', eof_token))

    # receive file
    resp = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)

    # save file
    try:
        file = open(args[1], 'wb')
        file.write(resp)
        file.close()
        print('successfully saved file ' + file.name)
    except OSError as e:
        print(e)
        return

    # send
    client_socket.sendall(pack_msg('ok', eof_token))
    # get response
    resp = receive_message_ending_with_token(client_socket, BUFFER_SIZE, eof_token)
    print(resp.decode())


def pack_msg(msg: str, eof_token: bytes):
    return str.encode(msg) + eof_token


def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    # initialize
    s, eof_token = initialize(HOST, PORT)
    while True:
        try:
            # get user input
            user_input = input("$> ").strip()

            # call the corresponding command function or exit
            if user_input == 'exit':
                s.sendall(pack_msg(user_input, eof_token))
                break
            elif user_input.startswith('cd'):
                issue_cd(user_input, s, eof_token)
            elif user_input.startswith('mkdir'):
                issue_mkdir(user_input, s, eof_token)
            elif user_input.startswith('rm'):
                issue_rm(user_input, s, eof_token)
            elif user_input.startswith('ls'):
                s.sendall(pack_msg(user_input, eof_token))
                data = receive_message_ending_with_token(s, BUFFER_SIZE, eof_token)
                print(data.decode())
            elif user_input.startswith('ul'):
                issue_ul(user_input, s, eof_token)
            elif user_input.startswith('dl'):
                issue_dl(user_input, s, eof_token)
            else:
                print('unknown command: ' + user_input)
        except KeyboardInterrupt:
            print('client closed with KeyboardInterrupt!')
            break
    print('Exiting the application.')


if __name__ == '__main__':
    main()
