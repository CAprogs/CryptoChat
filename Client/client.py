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

    def handle_encrypted_message(self, encrypted_message:bytes, socket_obj, src_public_key:bytes, private_key:bytes):
        # handle encrypted messages received from the client
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

    def handle_message(self):
        # handle messages received from the server
        step = "AUTH"
        while True:
            try:
                message = receive_message(self.socket)
                if step == "AUTH":
                    print(f"\n{message}")
                    send_message(self.username.encode(), self.socket)
                    srv_public_key = receive_message(self.socket, decode=False)
                    server_pub_key.append(srv_public_key)
                    print("Server public key received !")
                    print("Sending public key to server ...")
                    send_message(self.public_key, self.socket)
                    print("Public key sent to server !")
                    my_datas = f"{self.host} {self.public_ip} {self.city} {self.region} {self.location}"
                    print("Sending encrypted datas with encrypted signature to server ...")
                    self.send_encrypted_message(self.socket, my_datas, server_pub_key[0], self.private_key)
                    print("Datas and encrypted signature sent to server !")
                    step = "MAIN"
                elif step == "MAIN":
                    if message.startswith("NEW"):
                        print(f"\n{message.replace("NEW ", "")}\n")
                    else:
                        encrypted_message = bytes(message, "utf-8")
                        verified, decrypted_message, encrypted_message = self.handle_encrypted_message(encrypted_message, self.socket, server_pub_key[0], self.private_key)
                        if verified:
                            print(decrypted_message)
                        else:
                            print("Can't verify the message !")
            except Exception as e:
                print(f"An error occured when handling a message : {e}")
                if self.socket != "":
                    print("\nExiting the server..")
                    self.socket.close()
                break


    def write_message(self):
        # write a message and send it to the server
        while True:
            try:
                message = input('')
                self.send_encrypted_message(self.socket, message, server_pub_key[0], self.private_key)
                print(f"You ➤ {message}")
            except KeyboardInterrupt:
                print("\nExiting the server..")
                if self.socket != "":
                    self.socket.close()
                break
