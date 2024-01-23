"""                     _             _           _   
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_ 
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_ 
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Server
            |___/|_|                                  
"""


import os
import socket
from Server.server import Server
#from Server.User import file_path


SERVER_NAME = "Server"
HOST = "127.0.0.1"
PORT = 1234
LIMIT_CLIENTS = 2
LENGTH_OF_BYTES = 2048 # length of the RSA keys in bytes


if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(LIMIT_CLIENTS)
        os.system("clear")
        print(f"\nServer listening on {HOST}:{PORT}\n")
        
        server = Server(SERVER_NAME, HOST, PORT, s)

        # start the server
        server.receive_client()

    except KeyboardInterrupt:
        print("\nServer shutdown..")
        s.close()
