import requests
import json
import os
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def file_path(directory="", filename=""):
    # return the path of a file
    return os.path.join(directory, filename)

def get_timestamp():
    # get the current timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return timestamp

def send_message(message, socket_obj):
    # send a message to a socket
    socket_obj.send(message)

def receive_message(socket_obj, bytes_to_recv=4096, decode=True, encoding='utf-8'):
    # receive a message from a socket
    try:
        message = socket_obj.recv(bytes_to_recv)
        if decode:
            return message.decode(encoding)
        else:
            return message
    except Exception as e:
        print(f"Error when receiving message : {e}")
        return ""

def generate_RSA_key(username, length=2048):
    # generate a pair of RSA keys
    key = RSA.generate(length)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    private_key_file = username + "_private_key.pem"
    public_key_file = username + "_public_key.pem"
    with open(private_key_file, "wb") as file:
        file.write(private_key)
    with open(public_key_file, "wb") as file:
        file.write(public_key)
    print("Keys saved successfully !")
    return private_key, public_key

def encrypt_message(public_key, message):
    # Encrypt message with the public key
    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        return encrypted_message
    except (ValueError, TypeError) as e:
        print(f"Error when encrypting : {e}")

def decrypt_message(private_key, encrypted_message):
    # Decrypt message with the private key
    try:
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode('utf-8')
    except (ValueError, TypeError) as e:
            print(f"Error when decrypting : {e}")

class User:
    def __init__(self, username, host="127.0.0.1"):
        self.username = username
        self.host = host
        self.private_key, self.public_key = generate_RSA_key(username) if not os.path.exists(username + "_private_key.pem") else self.load_keys(username)
        # get the public ip address, city, region and location
        self.public_ip, self.city, self.region, self.location = self.geolocate()
    
    def load_keys(self, username):
        # load the keys from the files
        private_key_file = username + "_private_key.pem"
        public_key_file = username + "_public_key.pem"
        with open(private_key_file, "rb") as file:
            private_key = file.read()
        with open(public_key_file, "rb") as file:
            public_key = file.read()
        return private_key, public_key

    def sign_data(self, message):
        # Sign message with the private key
        try:
            key = RSA.import_key(self.private_key)
            # Hash the message using the SHA-256 hash function
            hash_data = SHA256.new(message)
            # Sign the hashed message using the private key
            signature = pkcs1_15.new(key).sign(hash_data)
            return hash_data, signature
        except Exception as e:
            print(e)

    def geolocate(self):
        # get the public ip address, city, region and location
        try:
            response = requests.get("https://ipinfo.io/json")
            if response.status_code == 200:
                file = json.loads(response.text)
                public_ip = file.get("ip")
                city = file.get("city")
                region = file.get("region")
                location = file.get("loc")
                return public_ip, city, region, location
            else:
                print(f"\nCan't access this page ! Status code : {response.status_code}\n")
        except Exception as e:
            print("Error : ", e)        

    def clear_console(self):
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
