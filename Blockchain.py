from hashlib import sha256
import json
import time
import pickle
from datetime import datetime
import random
import base64
from Block import *


class Blockchain:
    difficulty = 2  # Using difficulty 2 computation

    def _init_(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.peer = []
        self.translist = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create genesis block
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        # Adding data to block by computing new and previous hashes
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        # Proof of work
        return (
            block_hash.startswith('0' * Blockchain.difficulty)
            and block_hash == block.compute_hash()
        )

    def proof_of_work(self, block):
        # Proof of work
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def add_peer(self, peer_details):
        self.peer.append(peer_details)

    def add_transaction(self, trans_details):
        # Add transaction
        self.translist.append(trans_details)

    def mine(self):
        # Mine transaction
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
            previous_hash=last_block.hash,
        )

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []

        return new_block.index

    def save_object(self, obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)