import socket
import threading
import json
from blockchain import Blockchain, Block, Transaction

class Node:
    def __init__(self, host: str, port: int, blockchain: Blockchain):
        self.host = host
        self.port = port
        self.server = None
        self.peers = []
        self.blockchain = blockchain

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Node started on {self.host}:{self.port}")
        threading.Thread(target=self.listen_for_peers).start()

    def listen_for_peers(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected to peer {address}")
            threading.Thread(target=self.handle_peer, args=(client,)).start()

    def handle_peer(self, client):
        while True:
            try:
                data = client.recv(1024).decode('utf-8')
                if data:
                    self.handle_message(data)
            except Exception as e:
                print(f"Error handling peer: {e}")
                client.close()
                return

    def handle_message(self, message):
        data = json.loads(message)
        if data["type"] == "new_block":
            new_block_data = data["block"]
            new_block = Block.from_dict(new_block_data)
            if self.blockchain.add_block(new_block):
                print(f"New block added to blockchain: {new_block.index}")
            else:
                print("Failed to add block to blockchain")
        elif data["type"] == "new_transaction":
            transaction_data = data["transaction"]
            transaction = Transaction.from_dict(transaction_data)
            self.blockchain.add_transaction(transaction)

    def connect_to_peer(self, peer_host: str, peer_port: int):
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer.connect((peer_host, peer_port))
        self.peers.append(peer)
        print(f"Connected to peer {peer_host}:{peer_port}")

    def broadcast(self, message: str):
        for peer in self.peers:
            try:
                peer.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting to peer: {e}")

    def broadcast_new_block(self, block: Block):
        block_data = json.dumps({
            "type": "new_block",
            "block": block.to_dict()
        })
        self.broadcast(block_data)

    def broadcast_new_transaction(self, transaction: Transaction):
        transaction_data = json.dumps({
            "type": "new_transaction",
            "transaction": transaction.to_dict()
        })
        self.broadcast(transaction_data)
