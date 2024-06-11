from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, private_key=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None
        if private_key:
            self.sign_transaction(private_key)

    def sign_transaction(self, private_key):
        message = f"{self.sender}{self.recipient}{self.amount}".encode('utf-8')
        self.signature = private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        ).hex()

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature
        }

    @staticmethod
    def verify_transaction(transaction_data):
        public_key = serialization.load_pem_public_key(bytes.fromhex(transaction_data['sender']))
        message = f"{transaction_data['sender']}{transaction_data['recipient']}{transaction_data['amount']}".encode('utf-8')
        signature = bytes.fromhex(transaction_data['signature'])
        try:
            public_key.verify(
                signature,
                message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except:
            return False

    @staticmethod
    def from_dict(data):
        tx = Transaction(data['sender'], data['recipient'], data['amount'])
        tx.signature = data['signature']
        return tx
