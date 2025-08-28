import hashlib
import time
import requests
from urllib.parse import urlparse

#Block class skeleton
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = str(self.index) + str(self.data) + str(self.previous_hash) + str(self.timestamp)
        hash_bytes = hash_string.encode("utf-8")
        hash_object = hashlib.sha256(hash_bytes)
        block_hash = hash_object.hexdigest()
        return block_hash
    

#Blockchain class skeleton
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.currenttransactions = []
        self.nodes = set()

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.geturl())
    
    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")
    
    #Add new block method
    def add_block(self, data):
        last_block = self.chain[-1]
        new_index = last_block.index + 1
        new_block = Block(new_index, data, last_block.hash)
        self.chain.append(new_block)
        return new_block
    
    #Validate chain method
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            
            if current.previous_hash != previous.hash:
                return False
        
        return True
    
    #broadcast method
    def broadcast_new_block(self, new_block):
        for node in self.nodes:
            url = f"{node}/add_block"

            requests.post(url, json = {"data": block.data})

    def resolve_conflicts(self):
        import requests
        new_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            try:
                response = requests.get(f"{node}/chain")
                if response.status_code == 200:
                    node_chain = response.json()['chain']
                    node_chain_length = response.json()['length']

                    if node_chain_length > max_length:

                        valid_chain = []
                        for block_data in node_chain:
                            block = Block(
                                block_data['index'],
                                block_data['data'],
                                block_data['previous_hash']
                            )
                            block.timestamp = block_data['timestamp']
                            block.hash = block_data['hash']
                            valid_chain.append(block)
                        
                        temp_blockchain = Blockchain()
                        temp_blockchain.chain = valid_chain
                        if temp_blockchain.is_chain_valid():
                            max_length = node_chain_length
                            new_chain = valid_chain
            except Exception as e:
                print(f"Error fetching chain from node {node}: {e}")    
            
        if new_chain:
            self.chain = new_chain
            return True
        
        return False
    

    #test script
if __name__ == "__main__":
    my_chain = Blockchain()
    my_chain.add_block("First Block")
    my_chain.add_block("Second Block")

    for block in my_chain.chain:
        print(f"Index: {block.index}")
        print(f"Data: {block.data}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("-" * 30)

    print("Is blockchain valid?", my_chain.is_chain_valid())

    my_chain.chain[1].data = "Tampered Data"
    print("\nAfter tampering with Block 1:")
    print("Is blockchain valid?", my_chain.is_chain_valid())
