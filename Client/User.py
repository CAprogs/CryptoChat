import requests
import json
import os
from Scanner import MyScanner
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def file_path(directory="", filename=""):
    return os.path.join(directory, filename)

def get_timestamp():
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return timestamp

def send_message(message, socket_obj):
    socket_obj.send(message.encode('utf-8'))

class User:
    def __init__(self, username, host="127.0.0.1"): #host = private ip
        self.username = username
        self.host = host
        self.pair_of_keys = None
        self.private_key = None
        self.public_key = None
        # instantiate a scanner object and get the mac address
        self.scanner = MyScanner(self.host)
        self.mac = self.scanner.mac_scan()
        # get the public ip address, city, region and location
        self.public_ip, self.city, self.region, self.location = self.geolocate()

    def generate_RSA_keys(self, length=2048):
        # Generate a pair of RSA keys and save them in a file
        try:
            self.pair_of_keys = RSA.generate(length)
            self.private_key = self.pair_of_keys.export_key()
            self.public_key = self.pair_of_keys.publickey().export_key()
            private_key_file = file_path("keys", self.username + "_private_key.pem")
            public_key_file = file_path("keys", self.username + "_public_key.pem")
            with open(private_key_file, "wb") as file:
                file.write(self.private_key)
            with open(public_key_file, "wb") as file:
                file.write(self.public_key)
            print("Keys saved successfully !")
        except Exception as e:
            print(e)
    
    def encrypt(self, data, dest_public_key):
        # Encrypt data with the public key of the receiver
        try:
            # Initialize an RSA cipher object with the PKCS1_OAEP padding scheme
            cipher = PKCS1_OAEP.new(dest_public_key)
            encrypted_data = cipher.encrypt(data)
            return encrypted_data
        except (ValueError, TypeError) as e:
            print(f"Error when encrypting : {e}")

    def decrypt(self, encrypted_data):
        # Decrypt data with the private key
        try:
            # Initialize an RSA cipher object with the PKCS1_OAEP padding scheme
            cipher = PKCS1_OAEP.new(self.public_key)
            decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
            return decrypted_data
        except (ValueError, TypeError) as e:
            print(f"Error when decrypting : {e}")
    
    def sign_data(self, data):
        # Sign data with the private key
        try:
            # Hash the data using the SHA-256 hash function
            hash_data = SHA256.new(data)
            # Sign the hashed data using the private key
            signature = pkcs1_15.new(self.pair_of_keys).sign(hash_data)
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
    
    def send_encrypted_message(self, socket_obj, message, dst_pub_key):
        # send an encrypted message to a socket
        encrypted_message = self.encrypt(message, dst_pub_key)
        hash_data, signature = self.sign_data(message, self.username)
        socket_obj.send(encrypted_message.encode('utf-8'))
        return encrypted_message, hash_data.hexdigest(), signature

    def receive_message(self, socket_obj, bytes_to_recv="5"):
        # receive a message from a socket
        full_msg = ""
        while True:
            msg = socket_obj.recv(bytes_to_recv).decode("utf-8")
            if len(msg) <= 0:
                break
            full_msg += msg
        return full_msg

    def clear_console(self):
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

