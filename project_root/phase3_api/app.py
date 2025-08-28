from flask import Flask, jsonify, request
from phase1_basic_blockchain.block import Blockchain

# Create Flask app
app = Flask(__name__)

# Create a single blockchain instance for this node
blockchain = Blockchain()

# Root route (just for testing server is up)
@app.route("/", methods=["GET"])
def index():
    return "Welcome to the Blockchain API!"

# Get full blockchain
@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "data": block.data,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify({"chain": chain_data, "length": len(chain_data)}), 200

# Add a new block
@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.get_json()
    if not data or "data" not in data:
        return jsonify({"error": "Invalid block data"}), 400

    new_block = blockchain.add_block(data["data"])
    return jsonify({
        "index": new_block.index,
        "data": new_block.data,
        "timestamp": new_block.timestamp,
        "previous_hash": new_block.previous_hash,
        "hash": new_block.hash
    }), 201

# Validate blockchain
@app.route("/is_valid", methods=["GET"])
def is_valid():
    valid = blockchain.is_chain_valid()
    return jsonify({"is_valid": valid}), 200

# Register a new nodes
@app.route("/register_node", methods=["POST"])
def register_node():
    values = request.get_json()
    nodes = values.get("nodes") if values else None
    
    if nodes is None or not isinstance(nodes, list):
        return jsonify({"error": "Invalid nodes data"}), 400
    
    for node in nodes:
        blockchain.register_node(node)
    
    return jsonify({"message": "new nodes have been added", "total_nodes": list(blockchain.nodes)}), 201

# Consensus route
@app.route("/resolve_conflicts", methods=["GET"])
def resolve_conflicts_route():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        return jsonify({"message": "Our chain was replaced with the longest valid chain.", "new_chain": [block.__dict__ for block in blockchain.chain]})
    else:
        return jsonify({"message": "Our chain is already the longest valid chain.", "chain": [block.__dict__ for block in blockchain.chain]})


if __name__ == "__main__":
    import sys
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

        app.run(host="127.0.0.1", port = port, debug=True)
