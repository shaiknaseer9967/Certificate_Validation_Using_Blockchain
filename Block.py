from hashlib import sha256
import json
import time

class Block:
    def _init_(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that returns the hash of the block contents.
        """
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }

        # Convert the block data to a JSON string and sort keys for consistency
        block_string = json.dumps(block_data, sort_keys=True)

        # Return the SHA-256 hash of the block string
        return sha256(block_string.encode()).hexdigest()