from typing import List, TypedDict
import logging
import sys
import time
import utils
import json
import hashlib


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class Transaction(TypedDict):
    sender_blockchain_address: str
    recipient_blockchain_address: str
    value: float  # 거래량


class Block(TypedDict):
    timestamp: float
    transactions: List[Transaction]
    nonce: int
    previous_hash: str  # 해싱된 이전 블록


class BlockChain:

    __MINNG_DIFFICULTY = 3
    __MINING_SENDER = "THE BLOCKCHAIN NETWORK"
    __MINING_REWARD = 1.0  # 마이닝 보상

    def __init__(self, blockchain_address=None):
        self.chain = []
        self.transaction_pool = []
        self.create_block(0, self.hash_block({}))  # 초기 블록 생성
        self.blockchain_address = blockchain_address

    def create_block(self, nonce, previous_hash):
        vanila_block: Block = {
            "timestamp": time.time(),
            "transactions": self.transaction_pool,
            "nonce": nonce,
            "previous_hash": previous_hash,
        }
        block = utils.sorted_dict_by_key(vanila_block)
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash_block(self, block):
        sorted_block = json.dumps(block, sort_keys=True)  # dictionary sorting : double check
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(
        self, sender_blockchain_address, recipient_blockchain_address, value: float
    ):
        vanila_transaction: Transaction = {
            "sender_blockchain_address": sender_blockchain_address,
            "recipient_blockchain_address": recipient_blockchain_address,
            "value": float(value),
        }
        transaction = utils.sorted_dict_by_key(vanila_transaction)
        self.transaction_pool.append(transaction)
        return True

    def valid_proof(self, transactions, previous_hash, nonce, difficulty=__MINNG_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key(
            {"transactions": transactions, "nonce": nonce, "previous_hash": previous_hash}
        )
        guess_hash = self.hash_block(guess_block)
        return guess_hash[:difficulty] == "0" * difficulty

    def proof_of_work(self):
        # 작업증명 : 블록체인의 보안을 유지하기 위해 해시값을 구하는 과정이다.
        # 모든 블록체인은 블록 생성 주기(비트코인은 10분)를 가지고 이 생성 주기마다 새로운 블록이 생성되고 블록체인에 추가된다.
        # 네트워크의 모든 노드가 동시에 블록을 만들 수 없게 하는 것이다. 작업증명에 성공한 노드만이 마이닝이 가능하여 보상을 받는다.
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash_block(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def mining(self):
        self.add_transaction(
            sender_blockchain_address=self.__MINING_SENDER,
            recipient_blockchain_address=self.blockchain_address,
            value=self.__MINING_REWARD,
        )
        nonce = self.proof_of_work()
        previous_hash = self.hash_block(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logger.info({"action": "mining", "status": "success"})
        return True

    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block["transactions"]:
                value = float(transaction["value"])
                if blockchain_address == transaction["recipient_blockchain_address"]:
                    total_amount += value
                if blockchain_address == transaction["sender_blockchain_address"]:
                    total_amount -= value
        return total_amount


if __name__ == "__main__":
    my_blockchain_address = "13gyu91237723g4g780921e"
    block_chain = BlockChain(blockchain_address=my_blockchain_address)
    utils.print_block_chain(block_chain.chain)

    block_chain.add_transaction("A", "B", 1.0)
    block_chain.mining()
    utils.print_block_chain(block_chain.chain)

    block_chain.add_transaction("C", "D", 3.2)
    block_chain.add_transaction("X", "Y", 12.3)
    block_chain.mining()
    utils.print_block_chain(block_chain.chain)

    print(f"me : {block_chain.calculate_total_amount(my_blockchain_address)}")
    print(f'C : {block_chain.calculate_total_amount("C")}')
    print(f'D : {block_chain.calculate_total_amount("D")}')
