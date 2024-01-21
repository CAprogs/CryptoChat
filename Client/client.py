from .User import User, send_message, receive_message, encrypt_message, decrypt_message


server_pub_key=[]


class Client(User):
    def __init__(self, username, host="127.0.0.1", port=1234, socket="", ):
        super().__init__(username, host)
        self.port = port
        self.socket = socket

    def handle_message(self):
        # handle different types of messages
        try:
            message = receive_message(self.socket)
            print(f"\n{message}")
            send_message(self.username.encode(), self.socket)
            srv_public_key = receive_message(self.socket)
            server_pub_key.append(srv_public_key)
            print("Server public key received !")
            print("sending public key to server ...")
            send_message(self.public_key, self.socket)
            print("Sending encrypted datas to server ...")
            encrypted_datas = encrypt_message(srv_public_key, f"{self.host} {self.public_ip} {self.city} {self.region} {self.location}")
            send_message(encrypted_datas, self.socket)
            print("Encrypted datas sent to server")
            '''
            print("Did not receive any message..")
            print("Server disconnected..")
            if self.socket != "":
                print("Closing the socket..")
                self.socket.close()
            '''

        except Exception as e:
            print(f"An error occured when handling a message : {e}")


    def write_message(self):
        # write a message and send it to the server
        while True:
            try:
                message = f"{self.username} > {input('')}"
                send_message(message, self.socket)
            except KeyboardInterrupt:
                print("\nClient exited..")
                if self.socket is not None:
                    self.socket.close()
                break
