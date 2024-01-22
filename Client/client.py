import hashlib
from .User import User 
from .User import send_message, receive_message
from .User import encrypt_message, decrypt_message
from .User import sign_message, verify_signature


server_pub_key=[]


class Client(User):
    def __init__(self, username, host="127.0.0.1", port=1234, socket=""):
        super().__init__(username, host)
        self.port = port
        self.socket = socket


    def send_encrypted_message(self, message:str):
        # send encrypted messages to the server
        encrypted_message = encrypt_message(server_pub_key[0], bytes(message, 'utf-8'))
        send_message(encrypted_message, self.socket)
        signature = sign_message(self.private_key, encrypted_message)
        encrypted_signature = encrypt_message(server_pub_key[0], signature, blockwise=True)
        send_message(encrypted_signature, self.socket)


    def handle_message(self):
        # handle messages received from the server
        i = 0
        while True:
            try:
                if i == 0:
                    message = receive_message(self.socket)
                    print(f"\n{message}")
                    send_message(self.username.encode(), self.socket)
                    srv_public_key = receive_message(self.socket)
                    server_pub_key.append(srv_public_key)
                    print("Server public key received !")
                    print("Sending public key to server ...")
                    send_message(self.public_key, self.socket)
                    print("Public key sent to server !")
                    my_datas = f"{self.host} {self.public_ip} {self.city} {self.region} {self.location}"
                    print("Sending encrypted datas with encrypted signature to server ...")
                    self.send_encrypted_message(my_datas)
                    print("Datas and encrypted signature sent to server !")
                    i += 1
                #elif ...
            except Exception as e:
                print(f"An error occured when handling a message : {e}")
                if self.socket != "":
                    print("\nExiting the server..")
                    self.socket.close()


    def write_message(self):
        # write a message and send it to the server
        while True:
            try:
                message = input('')
                self.send_encrypted_message(message)
                print(f"You ➤ {message}")
            except KeyboardInterrupt:
                print("\nExiting the server..")
                if self.socket != "":
                    self.socket.close()
                break
