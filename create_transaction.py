import sys
from blockchain import Blockchain, Transaction
from wallet import Wallet

def create_transaction(sender_wallet_path, recipient_address, amount):
    # 지갑 로드
    wallet = Wallet(private_key_path=sender_wallet_path)

    # 트랜잭션 생성 및 서명
    transaction = Transaction(wallet.get_address(), recipient_address, amount)
    wallet.sign_transaction(transaction)

    # 블록체인 로드 (예제에서는 메모리 블록체인을 사용)
    difficulty = 2
    mining_reward = 50
    blockchain = Blockchain(difficulty, mining_reward)

    # 트랜잭션 추가
    blockchain.add_transaction(transaction)

    # 블록 생성 및 채굴
    miner_address = wallet.get_address()
    new_block = blockchain.create_new_block(miner_address)
    print(f"Block #{new_block.index} has been added to the blockchain!")
    print(f"Hash: {new_block.hash}\n")

    # 블록체인 상태 출력
    print("\n--- Current Blockchain ---")
    for block in blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Nonce: {block.nonce}")
        print("Transactions:")
        for tx in block.transactions:
            print(f"  {tx.sender} -> {tx.recipient}: {tx.amount}")
        print(f"Hash: {block.hash}\n")
    print("--- End of Blockchain ---\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_transaction.py <sender_wallet_path> <recipient_address> <amount>")
    else:
        create_transaction(sys.argv[1], sys.argv[2], float(sys.argv[3]))
