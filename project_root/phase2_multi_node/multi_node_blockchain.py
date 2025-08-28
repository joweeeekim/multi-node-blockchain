from phase1_basic_blockchain.block import Block, Blockchain

# -----------------------------
# Step 1: Create 5 nodes dynamically
# -----------------------------
nodes = [Blockchain() for _ in range(5)]

# -----------------------------
# Step 2: Broadcast function
# -----------------------------
def broadcast_block(new_block, nodes, creator_node):
    for node in nodes:
        if node != creator_node and node.chain[-1].hash == new_block.previous_hash:
            node.chain.append(new_block)

# -----------------------------
# Step 3: Consensus mechanism
# -----------------------------
def consensus(nodes):
    longest_chain = None
    max_length = 0

    # find the longest valid chain
    for node in nodes:
        if node.is_chain_valid() and len(node.chain) > max_length:
            max_length = len(node.chain)
            longest_chain = node.chain

    # update all nodes to adopt the longest valid chain
    for node in nodes:
        if node.chain != longest_chain:
            node.chain = longest_chain.copy()

# -----------------------------
# Step 4: Add initial blocks from Node 1
# -----------------------------
creator_node = nodes[0]

for i in range(1, 4):
    new_block = Block(
        creator_node.chain[-1].index + 1,
        f"Block {i} from Node 1",
        creator_node.chain[-1].hash
    )
    creator_node.chain.append(new_block)
    broadcast_block(new_block, nodes, creator_node)

# -----------------------------
# Step 5: Validate all nodes initially
# -----------------------------
print("Initial validation of nodes:")
for i, node in enumerate(nodes):
    print(f"Node {i+1} chain valid? {node.is_chain_valid()}")

# -----------------------------
# Step 6: Tamper multiple nodes
# -----------------------------
nodes[1].chain[2].data = "Tampered Data Node 2"
nodes[2].chain[1].data = "Tampered Data Node 3"

print("\nAfter tampering multiple nodes:")
for i, node in enumerate(nodes):
    print(f"Node {i+1} chain valid? {node.is_chain_valid()}")

# -----------------------------
# Step 7: Apply consensus to fix tampering
# -----------------------------
consensus(nodes)

print("\nAfter consensus resolves tampering:")
for i, node in enumerate(nodes):
    print(f"Node {i+1} chain valid? {node.is_chain_valid()}")

# -----------------------------
# Step 8: Add new blocks dynamically after consensus
# -----------------------------
for j in range(4, 7):
    new_block = Block(
        creator_node.chain[-1].index + 1,
        f"Dynamic Block {j} from Node 1",
        creator_node.chain[-1].hash
    )
    creator_node.chain.append(new_block)
    broadcast_block(new_block, nodes, creator_node)

# Apply consensus again after adding new blocks
consensus(nodes)

print("\nAfter adding new blocks dynamically and applying consensus:")
for i, node in enumerate(nodes):
    print(f"Node {i+1} chain valid? {node.is_chain_valid()}")

# -----------------------------
# Step 9: Print final chains for verification
# -----------------------------
for i, node in enumerate(nodes):
    print(f"\nNode {i+1} final chain:")
    for block in node.chain:
        print(f"Index: {block.index}, Data: {block.data}, Hash: {block.hash}")
