"""                     _             _           _   
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_ 
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_ 
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Client
            |___/|_|

by @CAprogs (https://github.com/CAprogs)
"""


import socket
import threading
from Client.client import Client
from Client.User import clear_console


HOST = "127.0.0.1"              # Host to connect to
PORT = 1234                     # Port to connect to
LENGTH_OF_BYTES = 2048          # Length of the RSA keys in bytes


if __name__ == '__main__':
    try:
        clear_console()
        print("")
        CLIENT_NAME = input("Choose a username (CTRL + C to exit) ▶︎ ")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        client = Client(CLIENT_NAME, HOST, PORT, socket=s)

        threading.Thread(target=client.handle_message).start()
        threading.Thread(target=client.write_message).start()

    except KeyboardInterrupt:
        print("\n\nExiting the chat ..\n\nSession closed !")

    except ConnectionRefusedError:
        print("\nServer is not running ..\n\nPlease try again later !\n")
