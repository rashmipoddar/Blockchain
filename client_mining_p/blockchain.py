# Paste your version of blockchain.py from the basic_block_gp
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof' : proof,
            'previous_hash': previous_hash or self.hash(self.last_block) 
            # self.hash(self.chain[-1]) is the same as self.hash(self.last_block) 
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Create the block_string
        # Use json.dumps to convert json into a string
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        # sort_keys = True will keep the order of key-values pairs in the dictionary
        string_block = json.dumps(block, sort_keys=True)

        # Hash this string using sha256
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        raw_hash = hashlib.sha256(string_block.encode())

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hex_hash = raw_hash.hexdigest()

        # Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string + proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # print('The block_string is ', block_string)
        guess = f'{block_string}{proof}'.encode()
        # print('The guess is ', guess)
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:6] == '000000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    print(data)
    if data['proof'] and data['id']:
      string_block = json.dumps(blockchain.last_block, sort_keys=True)
      validity = blockchain.valid_proof(string_block, data['proof'])
      if validity:
        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(data['proof'], previous_hash)
        response = {
          'message': 'New Block Forged'
        }
      else: 
        response = {
          'message': 'The proof is not valid or late'
        } 
      return jsonify(response), 200
    else:
      response = {
        'message': 'Id and proof both are needed'
      }  
      return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def chain_last_block():
    response = {
        # Return the last block in chain
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
