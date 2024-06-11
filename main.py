import sys
import time
from blockchain import Blockchain, Transaction
from p2p_network import Node
from wallet import Wallet
from colorama import Fore, Style, init
from logo import display_logo, display_app_info

# 색상 초기화
init(autoreset=True)

# 상수 변수
APP_VERSION = "0.0.1"
APP_AUTHOR = "Zhin"
APP_YEAR = "2024"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB

def print_blockchain(blockchain):
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

def mine_block(blockchain, miner_address):
    new_block = blockchain.create_new_block(miner_address)
    print(f"Block #{new_block.index} has been added to the blockchain!")
    print(f"Hash: {new_block.hash}\n")
    print_blockchain(blockchain)

def main():
    # 실행 옵션 확인
    test_mode = '-test' in sys.argv

    # 지갑 생성
    wallet = Wallet()

    difficulty = 2  # 난이도 조절
    mining_reward = 50  # 채굴 보상
    blockchain = Blockchain(difficulty, mining_reward, test_mode)

    # 채굴자 주소 설정
    miner_address = wallet.get_address()

    if not test_mode:
        # 네트워크 노드 시작
        node = Node('localhost', 5000, blockchain)
        node.start()

        # 다른 노드와의 연결 시도
        while True:
            try:
                node.connect_to_peer('localhost', 5001)
                break  # 연결 성공 시 루프 종료
            except ConnectionRefusedError:
                print("Connection failed, retrying...")
                time.sleep(5)  # 5초 후 재시도

    # 연속적으로 채굴
    while True:
        mine_block(blockchain, miner_address)
        time.sleep(10)  # 10초 대기 후 다음 블록 채굴

if __name__ == "__main__":
    display_logo()
    display_app_info(APP_VERSION, APP_AUTHOR, APP_YEAR)
    main()
