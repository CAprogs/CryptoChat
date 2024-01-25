"""                     _             _           _   
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_ 
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_ 
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Server
            |___/|_|                                  
"""


import socket
from Server.server import Server, conversations, users
from Server.User import clear_console, save_datas

HOST = "127.0.0.1"
PORT = 1234
LIMIT_CLIENTS = 1
LENGTH_OF_BYTES = 2048 # length of the RSA keys in bytes


if __name__ == '__main__':
    try:
        clear_console()
        SERVER_NAME = input("Choose a username (CTRL + C to exit) ▶︎ ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(LIMIT_CLIENTS)
        print(f"\nHosting the chat on {HOST} : {PORT}\n\nWaiting for connection ...")

        server = Server(SERVER_NAME, HOST, PORT, s)

        # start the server
        server.authenticate_client()

    except Exception as e:
        save_datas(conversations, "conversation.json")
        save_datas(users, "users.json")
        print("\nSession terminated !")
