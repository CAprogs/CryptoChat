"""                     _             _           _
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Server
            |___/|_|

by @CAprogs (https://github.com/CAprogs)
"""


import socket
from Server.server import Server
from Server.User import clear_console


HOST = "127.0.0.1"              # Hosting on localhost
PORT = 1234                     # Port to open
LIMIT_CLIENTS = 1               # Limit the number of clients that can connect to the server
LENGTH_OF_BYTES = 2048          # Length of the RSA keys in bytes


if __name__ == '__main__':
    try:
        clear_console()
        print("")
        SERVER_NAME = input("Choose a username (CTRL + C to exit) ▶︎ ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(LIMIT_CLIENTS)
        print(f"\nHosting the chat on {HOST}:{PORT}\n\nWaiting for connection ...")

        server = Server(SERVER_NAME, HOST, PORT, s)

        server.authenticate_client()

    except KeyboardInterrupt:
        print("\nSession terminated !\n")
