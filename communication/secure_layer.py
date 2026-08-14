import json 
import base64
import os

from cryptography.fernet import Fernet

class SecureCommunicationLayer:

    def __init__(self):
        key = os.getenv("SCL_KEY")


        if not key:
            key = Fernet.generate_key()


        self.cipher = Fernet(key)


        def encrypt(self , message : dict)-> str:
            raw = json.dumps(message).encode()

            encrypted = self.cipher.encrypt(raw)

            return base64.b64encode(encrypted).decode()

        def decrypt(self , message : str)-> dict:
            encrypted = base64.b64decode(message.encode())

            raw = self.cipher.decrypt(encrypted)

            return json.loads(raw.decode())


        
