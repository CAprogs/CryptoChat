
import threading
from .User import User, ENC_DEC_MODE
from .User import send_message, receive_message, get_timestamp
from .User import encrypt_message, decrypt_message
from .User import sign_message, verify_signature
import time


users = {}
conversations = {}
threads = []
stop_event = threading.Event()


class Server(User):
    def __init__(self, username, host="127.0.0.1", port=1234, socket=""):
        super().__init__(username, host)
        self.port = port
        self.socket = socket
        self.timestamp = get_timestamp()
        self.nb = 0

    def handle_encrypted_message(self, socket_obj, src_public_key: bytes, private_key: bytes):
        # handle encrypted messages received from the client
        encrypted_message = receive_message(socket_obj, decode=False)
        if encrypted_message is None:
            return False, None, None
        encrypted_signature = receive_message(socket_obj, decode=False)
        signature = decrypt_message(private_key, encrypted_signature, blockwise=True)
        if verify_signature(src_public_key, encrypted_message, signature):
            decrypted_message = decrypt_message(private_key, encrypted_message)
            return True, decrypted_message, encrypted_message
        else:
            return False, None, encrypted_message

    def send_encrypted_message(self, socket_obj, message: str, dest_public_key: bytes, private_key: bytes):
        # send encrypted messages to the server
        encrypted_message = encrypt_message(dest_public_key, bytes(message, ENC_DEC_MODE))
        send_message(encrypted_message, socket_obj)
        signature = sign_message(private_key, encrypted_message)
        encrypted_signature = encrypt_message(dest_public_key, signature, blockwise=True)
        send_message(encrypted_signature, socket_obj)

    def authenticate_client(self):
        # Listen to new clients and handle them
        global users
        client, address = self.socket.accept()

        print(f"\nConnection from {address} has been established..")
        send_message("Welcome to CryptoChat server !".encode(ENC_DEC_MODE), client)
        client_username = receive_message(client)
        print(f"\n ▶︎ {client_username} ◀︎ joined the Chat !\n")
        # print("\nSending username to client ..")
        send_message(self.username.encode(ENC_DEC_MODE), client)
        time.sleep(0.5)
        # print("Sending public key to client ...")
        send_message(self.public_key, client)
        # print("Receiving client's public key ...")
        client_public_key = receive_message(client, decode=False)
        # print("Client public key received !\nHandling encrypted datas from client..")
        verified, decrypted_user_datas, _ = self.handle_encrypted_message(client, client_public_key, self.private_key)
        if verified:
            print("Client authenticated !\n\n▿ Chat session started, write something .. ▿\n")
            user_datas = decrypted_user_datas.decode(ENC_DEC_MODE).split(" ")
            timestamp = get_timestamp()
            users[client] = {"username": client_username,
                             "public_key": client_public_key,
                             "host": user_datas[0],
                             "public_ip": user_datas[1],
                             "city": user_datas[2],
                             "region": user_datas[3],
                             "location": user_datas[4],
                             "timestamp": timestamp}
            
            writing_thread = threading.Thread(target=self.write_to_client, args=(client,))
            receiving_thread = threading.Thread(target=self.receive_from_client, args=(client,))
            threads.append(writing_thread)
            threads.append(receiving_thread)
            for thread in threads:
                thread.daemon = True # Kill the threads when the main thread is killed
                thread.start() # Start the threads
            for thread in threads: # Wait for the threads to finish
                thread.join()
        else:
            print("Client authentication failed !\nShutting down the Session ..")
            self.socket.close()
            return

    def write_to_client(self, client):
        # Send a message to the client
        global users
        global conversations
        global stop_event

        while not stop_event.is_set():
            message = input('')
            client_username = users[client].get("username")
            self.send_encrypted_message(client, message, users[client].get("public_key"), self.private_key)
            print(f"You ➤ {message}")
            timestamp = get_timestamp()
            conversations[self.nb] = {"sender": self.username, "receiver": client_username, "message": message, "timestamp": timestamp}
            self.nb += 1


    def receive_from_client(self, client):
        # Listen to the client and print his messages
        global users
        global conversations
        global stop_event

        client_username = users[client].get("username")
        while not stop_event.is_set():
            verified, decrypted_message, _ = self.handle_encrypted_message(client, users[client].get("public_key"), self.private_key)
            if verified:
                print(f"{client_username} >>> {decrypted_message.decode(ENC_DEC_MODE)}")
                timestamp = get_timestamp()
                conversations[self.nb] = {"sender": client_username, "receiver": self.username, "message": decrypted_message.decode(ENC_DEC_MODE), "timestamp": timestamp}
                self.nb += 1
            else:
                print(f"\n ▶︎ {client_username} ◀︎ left the chat !\n\nPress Ctrl + C to exit ..\n")
                stop_event.set()
                self.socket.close()
