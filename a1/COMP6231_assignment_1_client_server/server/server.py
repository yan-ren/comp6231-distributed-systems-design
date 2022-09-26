import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path
from base64 import b64encode


BUFFER_SIZE = 1024

def get_working_directory_info(working_directory):
    """
    Creates a string representation of a working directory and its contents.
    :param working_directory: path to the directory
    :return: string of the directory and its contents.
    """
    dirs = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_dir()])
    files = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_file()])
    dir_info = f'Current Directory: {working_directory}:\n|{dirs}{files}'
    return dir_info


def generate_random_eof_token():
    """Helper method to generates a random token that starts with '<' and ends with '>'.
     The total length of the token (including '<' and '>') should be 10.
     Examples: '<1f56xc5d>', '<KfOVnVMV>'
     return: the generated token.
     """
    return str.encode('<') + b64encode(os.urandom(10))[:8] + str.encode('>')


def receive_message_ending_with_token(active_socket, buffer_size, eof_token):
    """
    Same implementation as in receive_message_ending_with_token() in client.py
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


def handle_cd(current_working_directory, new_working_directory):
    """
    Handles the client cd commands. Reads the client command and changes the current_working_directory variable 
    accordingly. Returns the absolute path of the new current working directory.
    :param current_working_directory: string of current working directory
    :param new_working_directory: name of the sub directory or '..' for parent
    :return: absolute path of new current working directory
    """
    raise NotImplementedError('Your implementation here.')


def handle_mkdir(current_working_directory, directory_name):
    """
    Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
    :param current_working_directory: string of current working directory
    :param directory_name: name of new sub directory
    """
    raise NotImplementedError('Your implementation here.')


def handle_rm(current_working_directory, object_name):
    """
    Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
    based on the object type (directory/file).
    :param current_working_directory: string of current working directory
    :param object_name: name of sub directory or file to remove
    """
    raise NotImplementedError('Your implementation here.')


def handle_ul(current_working_directory, file_name, service_socket, eof_token):
    """
    Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
    file in the current working directory.
    Use the helper method: receive_message_ending_with_token() to receive the message from the client.
    :param current_working_directory: string of current working directory
    :param file_name: name of the file to be created.
    :param service_socket: active socket with the client to read the payload/contents from.
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


def handle_dl(current_working_directory, file_name, service_socket, eof_token):
    """
    Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
    given socket.
    :param current_working_directory: string of current working directory
    :param file_name: name of the file to be sent to client
    :param service_socket: active service socket with the client
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


class ClientThread(Thread):
    def __init__(self, service_socket : socket.socket, address : str):
        Thread.__init__(self)
        self.service_socket = service_socket
        self.address = address
        self.cwd = os.getcwd()
        self.eof_token = generate_random_eof_token().decode()

    def run(self):
        print ("Connection from : ", self.address)
        # initialize the connection
        # send random eof token
        self.service_socket.sendall(str.encode(self.eof_token))

        # establish working directory
        # send the current dir info
        self.service_socket.sendall(self.pack_msg(get_working_directory_info(self.cwd)))

        while True:
            # get the command and arguments and call the corresponding method
            received = receive_message_ending_with_token(self.service_socket, BUFFER_SIZE, self.eof_token)
            if received.decode() == 'exit':
                break
            
            # send current dir info
            self.service_socket.sendall(self.pack_msg(get_working_directory_info(self.cwd)))

        print('Connection closed from:', self.address)

    def pack_msg(self, msg: str):
        return str.encode(msg) + str.encode(self.eof_token)

def main():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print("server started, waiting for client request...")
        while True:
            try:
                s.listen()
                c_socket, c_address = s.accept()
                new_thread = ClientThread(c_socket, c_address)
                new_thread.daemon = True
                new_thread.start()
            except KeyboardInterrupt:
                print("server closed with KeyboardInterrupt!")
                break

if __name__ == '__main__':
    main()


