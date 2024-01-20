
import socket
import threading
from Crypto.Signature import pkcs1_15
from User import User, send_message, get_timestamp


class Server(User):
    def __init__(self, username, host="127.0.0.1", port=1234):
        super().__init__(username, host)
        self.port = port
        self.step = 0
        self.socket = None
        self.users = {}
    
    def verify_signature(self, client, hash256, signature):
        # verify the signature of a message
        try:
            pkcs1_15.new(self.users[client].get("public_key")).verify(hash256, signature)
            return True
        except (ValueError, TypeError):
            return False

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

    def handle_client(self, database):
        # handle a client by receiving and sending messages
        while True:
            try:
                client, address = self.socket.accept()
                print(f"Connection from {address} has been established..")
                if self.step == 0:
                    send_message("CONNECTED Welcome to CryptoChat server !", client)
                    message = self.receive_message(self.socket, 10)
                elif message.startswith("SERVER_PUBLIC_KEY") and self.step == 1:
                    send_message(f"SERVER_PUBLIC_KEY {self.public_key}", client)
                    message = self.receive_message(self.socket, 10)
                elif self.step == 2:
                    message = self.decrypt(message, self.private_key)
                    user_infos = message.split(" ")
                    timestamp = get_timestamp()
                    self.users[client] = {"username": user_infos[0],
                                          "public_key": user_infos[1],
                                          "host": user_infos[2],
                                          "public_ip": user_infos[3],
                                          "MAC": user_infos[4],
                                          "city": user_infos[5],
                                          "region": user_infos[6],
                                          "location": user_infos[7],
                                          "timestamp": timestamp}
                    database.insert_user(user_infos[0],user_infos[1],user_infos[2],user_infos[3],user_infos[4],user_infos[5],user_infos[6],user_infos[7],timestamp)
                    self.broadcast(f"NEW {user_infos[0]} joined the chat !")
                else:
                    users_copy = self.users.copy()
                    users_copy.pop(client)
                    if len(self.users) == 1:
                        send_message("Waiting for a second client ..", client)
                        continue
                    for user in users_copy.values():
                        receiver = user.get("username")
                    timestamp = get_timestamp()
                    encrypted_message, hash256, signature = self.broadcast(f"{self.users[client].get("username")}: {message}")
                    
                    database.insert_data('Conversations', 
                                         {'sender': self.users[client].get("username"),
                                          'receiver': receiver, 
                                          'message': encrypted_message, 
                                          'hash256': hash256, 
                                          'signature': signature, 
                                          'timestamp': timestamp})
                self.step += 1
                thread = threading.Thread(target=self.handle_client, args=(database,))
                thread.start()
            except Exception as e:
                print(f"Error : {e}\n")
                self.broadcast(f"LEFT {self.users[client].get("username")} left the chat !")
                self.users.pop(client)
                client.close()
                break

    def start(self, database, limit_clients=2):
        # start the server by listening on the host and port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(limit_clients)
        self.clear_console()
        print(f"\nServer listening on {self.host}:{self.port}\n")

        self.handle_client(database)
