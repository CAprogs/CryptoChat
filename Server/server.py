
import threading
from Crypto.Signature import pkcs1_15
from .User import User, send_message,receive_message, get_timestamp, encrypt_message, decrypt_message


class Server(User):
    def __init__(self, username, host="127.0.0.1", port=1234, socket=""):
        super().__init__(username, host)
        self.port = port
        self.socket = socket
        self.users = {}
    
    def verify_signature(self, client, hash256, signature):
        # verify the signature of a message
        try:
            pkcs1_15.new(self.users[client].get("public_key")).verify(hash256, signature)
            return True
        except (ValueError, TypeError):
            return False

    '''
    def broadcast(self, message):
        # send a message to all clients depending on the message type
        clients = list(self.users.keys())
        if message.startswith("NEW"):
            old_clients = clients[:-1]
            message = message.replace("NEW ", "")
            for client in old_clients:
                send_message(message, client)
        elif message.startswith("LEFT"):
            message = message.replace("LEFT ", "")
            for client in clients:
                send_message(message, client)
        else:
            clients = list(self.users.keys())
            for client in clients:
                encrypted_message, hash256, signature = self.send_encrypted_message(message, client, self.users[client].get("public_key"))
                if self.verify_signature(client, hash256, signature):
                    return encrypted_message, hash256, signature
    '''
    def broadcast(self, message):
        clients = list(self.users.keys())
        for client in clients:
            send_message(message, client)

    def receive_client(self):
        while True:
            client, address = self.socket.accept()
            
            print(f"Connection from {address} has been established..")
            send_message("Welcome to CryptoChat server !".encode(), client)
            client_username = receive_message(client)
            print(f"Username of the client is {client_username}")
            print("Sending public key to client..")
            send_message(self.public_key, client)
            print("Receiving public key from client..")
            client_public_key = receive_message(client)
            print("Client public key received..")
            encrypted_user_datas = receive_message(client, decode=False)
            print("Received encrypted datas from client..")
            decrypted_user_datas = decrypt_message(self.private_key, encrypted_user_datas)
            print(f"Decrypted datas from client : {decrypted_user_datas}")
            user_datas = decrypted_user_datas.split(" ")
            timestamp = get_timestamp()
            self.users[client] = {"username": client_username,
                                "public_key": client_public_key.encode(),
                                "host": user_datas[0],
                                "public_ip": user_datas[1],
                                "city": user_datas[2],
                                "region": user_datas[3],
                                "location": user_datas[4],
                                "timestamp": timestamp}
            print("User datas :")
            print(self.users[client])
            '''
            database.insert_user(user_datas[0],user_datas[1],user_datas[2],user_datas[3],user_datas[4],user_datas[5],user_datas[6],user_datas[7],timestamp)
            self.broadcast(f"NEW {user_datas[0]} joined the chat !")
            print(f"{username} has joined the chat !")
            self.broadcast(f"NEW {username} joined the chat !", client)
            # receive a message from a client
            message = receive_message(client)
            if message == "":
                print("Did not receive any message..")
                return ""
            message = self.decrypt(message, self.private_key)
            print(message)
            return message
            '''

'''
    def handle_client(self, database):
        # handle a client by receiving and sending messages
        while True:
            try:
                users_copy = self.users.copy()
                users_copy.pop(client)
                if len(self.users) == 1:
                    send_message("Waiting for a second client ..", client)
                    continue
                for user in users_copy.values():
                    receiver = user.get("username", "UnknownUser")
                timestamp = get_timestamp()
                username = self.users.get(client, {}).get("username", "UnknownUser")
                encrypted_message, hash256, signature = self.broadcast(f"{username}: {message}")
                
                database.insert_data('Conversations', 
                                    {'sender': self.users[client].get("username"),
                                    'receiver': receiver, 
                                    'message': encrypted_message, 
                                    'hash256': hash256, 
                                    'signature': signature, 
                                    'timestamp': timestamp})

            except Exception as e:
                print(f"An error occured when handling a client : {e}\n")
                try:
                    username = self.users.get(client, {}).get("username", "UnknownUser")
                    self.broadcast(f"LEFT {username} left the chat !")
                    if client in self.users:
                        self.users.pop(client)
                    client.close()
                except Exception as e:
                    print(f"Another error occured when trying to close the socket : {e}\n")
                break
'''