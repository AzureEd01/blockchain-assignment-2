import hashlib
import json
import time

# Initial inventory
initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

BLOCKCHAIN_FILE = "blockchain_log.txt"

def md5_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

def proof_of_work(data: dict, difficulty: int = 4):
    base_string = json.dumps(data, sort_keys=True)
    nonce = 0
    while True:
        trial = base_string + str(nonce)
        hashed = md5_hash(trial)
        if hashed.startswith('0' * difficulty):
            return {
                "timestamp": time.time(),
                "data": data,
                "nonce": nonce,
                "hash": hashed
            }
        nonce += 1

def save_block_to_file(block: dict):
    with open(BLOCKCHAIN_FILE, "a") as f:
        f.write(json.dumps(block, indent=2))
        f.write("\n" + "=" * 60 + "\n")

def get_user_input():
    print("\nEnter new inventory item details:")
    item_id = input("ItemID: ")
    item_qty = int(input("ItemQTY: "))
    item_price = int(input("ItemPrice: "))
    location = input("Location: ")
    return {"ItemID": item_id, "ItemQTY": item_qty, "ItemPrice": item_price, "Location": location}

# Blockchain storage
blockchain = []

# Create and store genesis block
genesis_block = proof_of_work({"inventory": initial_inventory})
blockchain.append(genesis_block)
save_block_to_file(genesis_block)
print("\nGenesis block created and saved.")

# Main loop for user input
while True:
    new_item = get_user_input()
    last_inventory = blockchain[-1]["data"]["inventory"]
    updated_inventory = last_inventory + [new_item]
    
    print("Mining block... this may take a few seconds.")
    new_block = proof_of_work({"inventory": updated_inventory})
    blockchain.append(new_block)
    save_block_to_file(new_block)

    print(f"\n✅ Block mined successfully with nonce {new_block['nonce']} and hash {new_block['hash']}")
    print(f"Block saved to {BLOCKCHAIN_FILE}")

    cont = input("\nAdd another item? (y/n): ").strip().lower()
    if cont != 'y':
        print("Exiting...")
        break
