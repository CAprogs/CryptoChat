"""                     _             _           _   
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_ 
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_ 
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Client
            |___/|_|                                  
"""


import socket
import threading
import os
import threading
from Client.client import Client
from Client.User import file_path


HOST = "127.0.0.1"
PORT = 1234
LENGTH_OF_BYTES = 2048 # length of the RSA keys in bytes

if __name__ == '__main__':
    try:
        
        CLIENT_NAME = input("\nChoose a username :")
        
        client = Client(CLIENT_NAME)

        client.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.socket.connect((HOST, PORT))

        # verify if the client has already generated a pair of keys
        private_key_file = file_path("keys", client.username + "_private_key.pem")
        public_key_file = file_path("keys", client.username + "_public_key.pem")
        if os.path.exists(private_key_file) and os.path.exists(public_key_file):
            with open(private_key_file, 'rb') as file:
                client.private_key = file.read()
            with open(public_key_file, 'rb') as file:
                client.public_key = file.read()
        else:
            client.generate_RSA_keys(LENGTH_OF_BYTES)

        receive_thread = threading.Thread(target=client.receive)
        receive_thread.start()
        
        write_thread = threading.Thread(target=client.write)
        write_thread.start()
        
    except KeyboardInterrupt:
        print("\Server exited..")
        if client.socket is not None:
            client.socket.close()
