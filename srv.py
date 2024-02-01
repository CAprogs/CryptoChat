"""                     _             _           _
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Server
            |___/|_|

by @CAprogs (https://github.com/CAprogs)
"""


import socket
from Server.server import Server, conversations, users
from Server.User import clear_console, ENC_DEC_MODE
from Server.Database import DatabaseHandler, DB_NAME


HOST = "127.0.0.1"              # Hosting on localhost
PORT = 1234                     # Port to open
LIMIT_CLIENTS = 1               # Number of clients that can connect to the server
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
        database = DatabaseHandler(DB_NAME)
        print("\n\nSaving datas ..\nExiting Session ..")
        # register conversations
        for id, conversation in conversations.items():
            database.insert_conversation(conversation["sender"],
                                         conversation["receiver"],
                                         conversation["message"],
                                         conversation["timestamp"])
        # register the server as an user
        database.insert_user(server.username, 
                             server.public_key.decode(ENC_DEC_MODE), 
                             server.host,
                             server.public_ip,
                             server.city,
                             server.region, 
                             server.location, 
                             server.timestamp)
        # register all users
        for id, user in users.items():
            database.insert_user(user['username'], 
                                 user['public_key'].decode(ENC_DEC_MODE), 
                                 user['host'], 
                                 user['public_ip'],
                                 user['city'], 
                                 user['region'], 
                                 user['location'],
                                 user['timestamp'])
        database.conn.close()
        print("\nSession closed !\n")
