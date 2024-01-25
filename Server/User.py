import requests
import json
import os
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def file_path(directory:str="", filename:str=""):
    # Return the path of a file
    return os.path.join(directory, filename)

def clear_console():
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

def save_datas(datas, filename, indent=2):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            old_datas = json.load(file)
            datas += old_datas

    with open(filename, "w") as file:
        json.dump(datas, file, indent=indent)
    print(f"\nDatas saved successfully in {filename}")

def get_timestamp():
    # Get the current timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return timestamp

def send_message(message:bytes, socket_obj):
    # Send a message to a socket
    socket_obj.send(message)

def receive_message(socket_obj, bytes_to_recv:int=4096, decode:bool=True, encoding:str='utf-8'):
    # Receive a message from a socket
    try:
        message = socket_obj.recv(bytes_to_recv)
        if decode:
            return message.decode(encoding)
        else:
            return message
    except Exception as e:
        #print(f"Error when receiving message : {e}")
        return None

def generate_RSA_key(username:str, length:int=2048):
    # Generate a pair of RSA keys
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

def encrypt_message(public_key:bytes, message:bytes, blockwise:bool=False):
    # Encrypt message with the public key
    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)

        if not blockwise:
            # Encrypt the entire message at once
            encrypted_message = cipher.encrypt(message)
        else:
            # Divide the message into smaller blocks
            block_size = 190  # based on the key size and padding
            message_blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]
            # Encrypt each block separately
            encrypted_blocks = [cipher.encrypt(block) for block in message_blocks]
            # Concatenate the encrypted blocks to form the complete encrypted message
            encrypted_message = b''.join(encrypted_blocks)
        return encrypted_message
    except (ValueError, TypeError) as e:
        print(f"Error when encrypting : {e}")

def decrypt_message(private_key:bytes, encrypted_message:bytes, blockwise:bool=False):
    # Decrypt message with the private key
    try:
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)

        if not blockwise:
            # Decrypt the entire message at once
            decrypted_message = cipher.decrypt(encrypted_message)
        else:
            # Divide the encrypted message into smaller blocks
            block_size = 256
            encrypted_blocks = [encrypted_message[i:i+block_size] for i in range(0, len(encrypted_message), block_size)]
            # Decrypt each block separately
            decrypted_blocks = [cipher.decrypt(block) for block in encrypted_blocks]
            # Concatenate the decrypted blocks to form the complete decrypted message
            decrypted_message = b''.join(decrypted_blocks)
        return decrypted_message
    except (ValueError, TypeError) as e:
            print(f"Error when decrypting : {e}")

def verify_signature(public_key:bytes, message:bytes, signature:bytes):
    # Verify the signature using the public key
    try:
        key = RSA.import_key(public_key)
        hash_obj = SHA256.new(message)
        pkcs1_15.new(key).verify(hash_obj, signature)
        return True
    except (ValueError, TypeError):
        return False

def sign_message(private_key:bytes, message:bytes):
    # Sign message with the private key
    try:
        key = RSA.import_key(private_key)
        hash_data = SHA256.new(message)
        signature = pkcs1_15.new(key).sign(hash_data)
        return signature
    except Exception as e:
        print(e)


class User:
    def __init__(self, username:str, host:str="127.0.0.1"):
        self.username = username
        self.host = host
        self.private_key, self.public_key = generate_RSA_key(username) if not os.path.exists(username + "_private_key.pem") else self.load_keys(username)
        # get the public ip address, city, region and location
        self.public_ip, self.city, self.region, self.location = self.geolocate()
    
    def load_keys(self, username:str):
        # load the keys from the files
        private_key_file = username + "_private_key.pem"
        public_key_file = username + "_public_key.pem"
        with open(private_key_file, "rb") as file:
            private_key = file.read()
        with open(public_key_file, "rb") as file:
            public_key = file.read()
        print("Keys loaded successfully !")
        return private_key, public_key

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
