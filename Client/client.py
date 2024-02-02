from .User import User, ENC_DEC_MODE
from .User import send_message, receive_message
from .User import encrypt_message, decrypt_message
from .User import sign_message, verify_signature


server_pub_key = ""
server_username = ""


class Client(User):
    def __init__(self, username, host="127.0.0.1", port=1234, socket=""):
        super().__init__(username, host)
        self.port = port
        self.socket = socket

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

    def handle_message(self):
        global server_pub_key
        global server_username
        # handle messages received from the server
        step = "AUTH"
        while True:
            if step == "AUTH":
                message = receive_message(self.socket)
                print(f"\n{message}")
                send_message(self.username.encode(), self.socket)
                server_username = receive_message(self.socket)
                print("\nAuthentication ..")
                # print("Server username received !")
                server_pub_key = receive_message(self.socket, decode=False)
                # print("Server public key received !\nSending public key to server ...")
                send_message(self.public_key, self.socket)
                # print("Public key sent to server !")
                my_datas = f"{self.host} {self.public_ip} {self.city} {self.region} {self.location}"
                # print("Sending encrypted datas with encrypted signature to server ...")
                self.send_encrypted_message(self.socket, my_datas, server_pub_key, self.private_key)
                # print("Datas and encrypted signature sent to server !")
                print("\nAuthentication completed !\n\n▿ Chat session started, write something .. ▿\n")
                step = "MAIN"
            elif step == "MAIN":
                verified, decrypted_message, _ = self.handle_encrypted_message(self.socket, server_pub_key, self.private_key)
                if verified:
                    print(f"{server_username} >>> {decrypted_message.decode()}")
                else:
                    pass  # change to raise an error with server closed

    def write_message(self):
        # write a message and send it to the server
        while True:
            try:
                message = input('')
                self.send_encrypted_message(self.socket, message, server_pub_key, self.private_key)
                print(f"You ➤ {message}")
            except BrokenPipeError:
                print("\nServer is not running, can't send any message ..\nPress Ctrl + C to exit ..\n")
