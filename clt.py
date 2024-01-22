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
#from Client.User import file_path


HOST = "127.0.0.1"
PORT = 1234
LENGTH_OF_BYTES = 2048 # length of the RSA keys in bytes

if __name__ == '__main__':
    try:
        os.system("clear")
        print("")
        CLIENT_NAME = input("Choose a username ▶︎ ")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        client = Client(CLIENT_NAME, HOST, PORT, socket=s)

        receive_thread = threading.Thread(target=client.handle_message)
        receive_thread.start()
        
        write_thread = threading.Thread(target=client.write_message)
        write_thread.start()

    except KeyboardInterrupt:
        print("\nServer exited..")
        try:
            client.socket.close()
        except:
            pass
        
