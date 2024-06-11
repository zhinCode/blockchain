import hashlib
import time
import json
import os
from typing import List
from transaction import Transaction
from key_management import get_public_key_from_private

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: int, transactions: List[Transaction], nonce: int, hash: str):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = hash

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce,
            "hash": self.hash,
        }

    @staticmethod
    def from_dict(data):
        transactions = [Transaction.from_dict(tx) for tx in data['transactions']]
        return Block(
            data['index'],
            data['previous_hash'],
            data['timestamp'],
            transactions,
            data['nonce'],
            data['hash']
        )

class Blockchain:
    def __init__(self, difficulty: int, mining_reward: float, test_mode: bool = False):
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.test_mode = test_mode
        self.chain = []
        self.pending_transactions = []
        self.data_file = 'blockchain_test.json' if test_mode else 'blockchain_main.json'
        self.load_blockchain()

    def create_genesis_block(self):
        timestamp = int(time.time())
        genesis_block = Block(0, "0", timestamp, [], 0, self.calculate_hash(0, "0", timestamp, [], 0))
        return genesis_block

    def calculate_hash(self, index: int, previous_hash: str, timestamp: int, transactions: List[Transaction], nonce: int) -> str:
        mode_prefix = "test" if self.test_mode else "main"
        transaction_details = "".join([str(tx.sender) + str(tx.recipient) + str(tx.amount) for tx in transactions])
        value = f"{mode_prefix}{index}{previous_hash}{timestamp}{transaction_details}{nonce}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_transaction(self, transaction: Transaction):
        if Transaction.verify_transaction(transaction.to_dict()):
            self.pending_transactions.append(transaction)
        else:
            print("Invalid transaction")

    def create_new_block(self, miner_address: str):
        reward_tx = Transaction("System", miner_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)

        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = int(time.time())
        nonce, hash_value = self.proof_of_work(index, previous_block.hash, timestamp, self.pending_transactions)
        new_block = Block(index, previous_block.hash, timestamp, self.pending_transactions, nonce, hash_value)
        self.pending_transactions = []
        self.chain.append(new_block)
        self.save_blockchain()
        return new_block

    def proof_of_work(self, index: int, previous_hash: str, timestamp: int, transactions: List[Transaction]):
        nonce = 0
        while True:
            hash_value = self.calculate_hash(index, previous_hash, timestamp, transactions, nonce)
            if hash_value[:self.difficulty] == "0" * self.difficulty:
                return nonce, hash_value
            nonce += 1

    def validate_block(self, block: Block) -> bool:
        calculated_hash = self.calculate_hash(block.index, block.previous_hash, block.timestamp, block.transactions, block.nonce)
        if calculated_hash != block.hash:
            return False
        for tx in block.transactions:
            if not Transaction.verify_transaction(tx.to_dict()):
                return False
        return True

    def add_block(self, block: Block):
        if self.validate_block(block):
            self.chain.append(block)
            self.save_blockchain()
            return True
        return False

    def save_blockchain(self):
        with open(self.data_file, 'w') as f:
            data = {
                'chain': [block.to_dict() for block in self.chain],
                'pending_transactions': [tx.to_dict() for tx in self.pending_transactions]
            }
            json.dump(data, f, indent=4)

    def load_blockchain(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.chain = [Block.from_dict(block) for block in data['chain']]
                self.pending_transactions = [Transaction.from_dict(tx) for tx in data['pending_transactions']]
        else:
            self.chain = [self.create_genesis_block()]
            self.pending_transactions = []
