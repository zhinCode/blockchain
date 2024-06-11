from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from key_management import generate_keys, load_private_key, load_public_key
import os

class Wallet:
    def __init__(self, private_key_path="private_key.pem", public_key_path="public_key.pem"):
        if os.path.exists(private_key_path) and os.path.exists(public_key_path):
            self.private_key = load_private_key(private_key_path)
            self.public_key = load_public_key(public_key_path)
        else:
            self.private_key, self.public_key = generate_keys()
            self.save_keys(private_key_path, public_key_path)
        self.address = self.get_address()

    def save_keys(self, private_key_path, public_key_path):
        with open(private_key_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(public_key_path, 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def get_address(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()

    def sign_transaction(self, transaction):
        message = f"{transaction.sender}{transaction.recipient}{transaction.amount}".encode('utf-8')
        transaction.signature = self.private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        ).hex()

    def verify_transaction(self, transaction):
        public_key = serialization.load_pem_public_key(bytes.fromhex(transaction.sender))
        message = f"{transaction.sender}{transaction.recipient}{transaction.amount}".encode('utf-8')
        try:
            public_key.verify(
                bytes.fromhex(transaction.signature),
                message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except:
            return False
