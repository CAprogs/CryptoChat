"""                     _             _           _   
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_ 
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_ 
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Server
            |___/|_|                                  
"""


import os
from Server.server import Server, file_path
from Server.Database import DB


SERVER_NAME = "Server"
HOST = "127.0.0.1"
PORT = 1234
LIMIT_CLIENTS = 2
LENGTH_OF_BYTES = 2048 # length of the RSA keys in bytes


if __name__ == '__main__':
    try:
        server = Server(SERVER_NAME, HOST, PORT)

        # verify if the server has already generated a pair of keys
        private_key_file = file_path("keys", server.username + "_private_key.pem")
        public_key_file = file_path("keys", server.username + "_public_key.pem")
        if os.path.exists(private_key_file) and os.path.exists(public_key_file):
            with open(private_key_file, 'rb') as file:
                server.private_key = file.read()
            with open(public_key_file, 'rb') as file:
                server.public_key = file.read()
        else:
            server.generate_RSA_keys(LENGTH_OF_BYTES)

        # start the server
        server.start(DB, LIMIT_CLIENTS)
    
    except KeyboardInterrupt:
        print("\nServer shutdown..")
        if server.socket is not None:
            server.socket.close()
        DB.conn.close()
