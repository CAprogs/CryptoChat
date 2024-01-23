
import threading
from .User import User
from .User import send_message, receive_message, get_timestamp
from .User import encrypt_message, decrypt_message
from .User import sign_message, verify_signature


class Server(User):
    def __init__(self, username, host="127.0.0.1", port=1234, socket=""):
        super().__init__(username, host)
        self.port = port
        self.socket = socket
        self.users = {}

    def handle_encrypted_message(self, socket_obj, src_public_key:bytes, private_key:bytes):
        # handle encrypted messages received from the client
        encrypted_message = receive_message(socket_obj, decode=False)
        encrypted_signature = receive_message(socket_obj, decode=False)
        signature = decrypt_message(private_key, encrypted_signature, blockwise=True)
        if verify_signature(src_public_key, encrypted_message, signature):
            decrypted_message = decrypt_message(private_key, encrypted_message)
            return True, decrypted_message, encrypted_message
        else:
            return False, None, encrypted_message

    def send_encrypted_message(self, socket_obj, message:str, dest_public_key:bytes, private_key:bytes):
        # send encrypted messages to the server
        encrypted_message = encrypt_message(dest_public_key, bytes(message, 'utf-8'))
        send_message(encrypted_message, socket_obj)
        signature = sign_message(private_key, encrypted_message)
        encrypted_signature = encrypt_message(dest_public_key, signature, blockwise=True)
        send_message(encrypted_signature, socket_obj)

    def broadcast(self, message:str, receivers:list=None):
        # send a message to clients depending on the message type
        all_clients = list(self.users.keys())
        old_clients = all_clients[:-1]
        if message.startswith("NEW") and receivers is None:
            message = message.replace("NEW ", "")
            for client in old_clients:
                self.send_encrypted_message(client, message, self.users[client].get("public_key"), self.private_key)
        elif message.startswith("LEFT") and receivers is not None:
            message = message.replace("LEFT ", "")
            for client in receivers:
                self.send_encrypted_message(client, message, self.users[client].get("public_key"), self.private_key)
        elif receivers is not None:
            for client in receivers:
                self.send_encrypted_message(client, message, self.users[client].get("public_key"), self.private_key)
        elif receivers is None:
            for client in all_clients:
                self.send_encrypted_message(client, message, self.users[client].get("public_key"), self.private_key)
        else:
            print("An error occured when broadcasting the message !")

    def receive_client(self, batabase):
        while True:
            client, address = self.socket.accept()
            
            print(f"\nConnection from {address} has been established..")
            send_message(bytes("Welcome to CryptoChat server !", "utf-8"), client)
            client_username = receive_message(client)
            print(f"Username of the client is {client_username}\nSending public key to client..")
            send_message(self.public_key, client)
            print("Receiving public key from client..")
            client_public_key = receive_message(client, decode=False)
            print("Client public key received !\nHandling encrypted datas from client..")
            verified, decrypted_user_datas, encrypted_user_datas = self.handle_encrypted_message(client, client_public_key, self.private_key)
            if verified:
                print(f"Message from client verified !")
                print("Datas Decrypted !")
                user_datas = decrypted_user_datas.decode("utf-8").split(" ")
                timestamp = get_timestamp()
                self.users[client] = {"username": client_username,
                                    "public_key": client_public_key,
                                    "host": user_datas[0],
                                    "public_ip": user_datas[1],
                                    "city": user_datas[2],
                                    "region": user_datas[3],
                                    "location": user_datas[4],
                                    "timestamp": timestamp}
                if batabase.insert_user(client_username, client_public_key, user_datas[0], user_datas[1], user_datas[2], user_datas[3], user_datas[4], timestamp):
                    print(f"User ({client_username}) added to database !")
                self.broadcast(f"NEW {client_username} joined the chat !")

                thread = threading.Thread(target=self.handle_client, args=(client, batabase))
                thread.start()
            else:
                print("Signature not verified .. Decryption aborted !")


    def handle_client(self, client, database):
        # Listen to a specific client and broadcast his messages
        receivers_dict = self.users.copy()
        receivers_dict.pop(client)
        receivers_list = list(receivers_dict.keys())
        receivers_username = [self.users[client].get("username") for client in receivers_list]
        sender = self.users[client].get("username")
        sender_public_key = self.users[client].get("public_key")
        while True:
            try:
                verified, decrypted_message, encrypted_message = self.handle_encrypted_message(client, sender_public_key, self.private_key)
                if len(self.users) == 1 and verified:
                    self.broadcast("Please wait for another client ..", [client])
                elif len(self.users) == 2 and verified:
                    self.broadcast(f"{sender} ▻ {decrypted_message.decode("utf-8")}", receivers_list)
                    timestamp = get_timestamp()
                    database.insert_conversation(sender, receivers_list[0], encrypted_message.decode("utf-8"), timestamp)
                elif len(self.users) > 2 and verified: # Send message to all clients [except sender] if server has more than 2 clients
                    self.broadcast(f"{sender} ➤ {decrypted_message.decode("utf-8")}", receivers_list)
                    timestamp = get_timestamp()
                    database.insert_conversation(sender, str(receivers_username), encrypted_message.decode("utf-8"), timestamp)
                else:
                    pass
            except Exception as e:
                print(f"An error occured when handling a client : {e}")
                if len(self.users) == 2:
                    self.users.pop(client)
                    self.broadcast(f"LEFT {sender} left the chat !", receivers_list)
                client.close()
