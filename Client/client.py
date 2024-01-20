from .User import User, send_message


class Client(User):
    def __init__(self, username, host="127.0.0.1", port=1234):
        super().__init__(username, host)
        self.port = port
        self.socket = None
        self.server_pub_key = []

    def handle_message(self):
        # handle different types of messages
        while True:
            try:
                message = self.receive_message(self.socket, 10)
                if message.startswith("CONNECTED"):
                    print(message.replace("CONNECTED ", ""))
                    send_message(f"SERVER_PUBLIC_KEY", self.socket)
                elif message.startswith("SERVER_PUBLIC_KEY"):
                    self.server_pub_key.append(message.replace("SERVER_PUBLIC_KEY ", ""))
                    self.send_encrypted_message(self.socket, f"{self.username} {self.public_key} {self.host} {self.public_ip} {self.mac} {self.city} {self.region} {self.location}", self.server_pub_key[0])
                else:
                    message = self.decrypt(message)
                    print(message)
            except Exception as e:
                print(e)
                if self.socket is not None:
                    self.socket.close()
                break
    
    def write_message(self):
        # write a message and send it to the server
        while True:
            try:
                message = f"{self.username}: {input('')}"
                send_message(message, self.socket)
            except KeyboardInterrupt:
                print("\nClient exited..")
                if self.socket is not None:
                    self.socket.close()
                break
