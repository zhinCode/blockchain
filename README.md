# blockchain (zhinCoin)

project for blockchain technology.

## Features
- DLT(Distributed Ledger Technology)
- Proof of Work consensus algorithm
- transaction functionality
- Mining rewards
- peer-to-peer(P2P) network communication

## Requirements

- Python 3.x

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/zhinCode/blockchain.git
    cd blockchain
    ```

2. Install dependencies:

    ```sh
    pip install cryptography colorama
    ```

## Usage

1. By default, the program will run in peer-to-peer mode, attempting to connect to other nodes on the network.:
```sh
python main.py
```

2. You can specify the `-test` flag to run in test mode, which will mine blocks without attempting to connect to other nodes:
```sh
python main.py -test
```


## Configuration

To connect to additional peers, use the `connect_to_peer` method in the `Node` class:

```python
node.connect_to_peer('peer_address', peer_port)
# ex) node.connect_to_peer('localhost', '5001')
# ex) node.connect_to_peer('localhost', '5002')
# ...
```


## License
This project is licensed under the MIT License.

