import logging
import sys
import time
import utils
import json
import hashlib

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class BlockChain:

    __MINNG_DIFFICULTY = 3

    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash_block({}))

    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key(
            {
                "timestamp": time.time(),
                "transactions": self.transaction_pool,
                "nonce": nonce,
                "previous_hash": previous_hash,
            }
        )
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash_block(self, block):
        sorted_block = json.dumps(block, sort_keys=True)  # dictionary sorting : double check
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(
        self, sender_blockchain_address, recipient_blockchain_address, value: float
    ):
        transaction = utils.sorted_dict_by_key(
            {
                "sender_blockchain_address": sender_blockchain_address,
                "recipient_blockchain_address": recipient_blockchain_address,
                "value": float(value),
            }
        )
        self.transaction_pool.append(transaction)
        return True

    def valid_proof(self, transactions, previous_hash, nonce, difficulty=__MINNG_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key(
            {"transactions": transactions, "nonce": nonce, "previous_hash": previous_hash}
        )
        guess_hash = self.hash_block(guess_block)
        return guess_hash[:difficulty] == "0" * difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash_block(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce


if __name__ == "__main__":
    block_chain = BlockChain()

    block_chain.add_transaction("A", "B", 1.0)
    previous_block = block_chain.hash_block(block_chain.chain[-1])
    nonce = block_chain.proof_of_work()
    block_chain.create_block(nonce, previous_block)

    block_chain.add_transaction("C", "D", 3.2)
    previous_block = block_chain.hash_block(block_chain.chain[-1])
    nonce = block_chain.proof_of_work()
    block_chain.create_block(nonce, previous_block)

    block_chain.add_transaction("X", "Y", 12.3)
    previous_block = block_chain.hash_block(block_chain.chain[-1])
    nonce = block_chain.proof_of_work()
    block_chain.create_block(nonce, previous_block)

    utils.print_block_chain(block_chain.chain)
