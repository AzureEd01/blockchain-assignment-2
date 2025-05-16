import random
import hashlib
import datetime

# Initial shared inventory data
initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

# Each node starts with the same inventory
inventories = {
    "Node1": initial_inventory.copy(),
    "Node2": initial_inventory.copy(),
    "Node3": initial_inventory.copy(),
    "Node4": initial_inventory.copy()
}

# Function to get user input for a new record
def get_new_record():
    print("Enter new record details:")
    item_id = input("ItemID: ").strip()
    qty = int(input("ItemQTY: ").strip())
    price = int(input("ItemPrice: ").strip())
    location = input("Location: ").strip().upper()
    return {"ItemID": item_id, "ItemQTY": qty, "ItemPrice": price, "Location": location}

# Validation logic
def validate_record(record, existing_inventory):
    for item in existing_inventory:
        if item["ItemID"] == record["ItemID"]:
            return False  # Reject if duplicate ItemID
    return True

# Get new record from user
new_record = get_new_record()

# Simulate authorized nodes
authorized_nodes = list(inventories.keys())

# Randomly pick a proposer
proposer = random.choice(authorized_nodes)
print(f"\n[INFO] Proposer for this round: {proposer}")

# Voting process
votes = {}
for node in authorized_nodes:
    vote = validate_record(new_record, inventories[node])
    votes[node] = vote
    print(f"[VOTE] {node} voted {'ACCEPT' if vote else 'REJECT'}")

# Consensus logic
approvals = sum(votes.values())
if approvals >= (len(authorized_nodes) // 2 + 1):
    print("\n[CONSENSUS] Consensus reached. Adding record to all inventories...")
    for node in inventories:
        inventories[node].append(new_record)
else:
    print("\n[CONSENSUS] Consensus NOT reached. Record rejected.")

# Final state
print("\n[FINAL INVENTORY STATE]")
for node, records in inventories.items():
    print(f"{node}:")
    for r in records:
        print(f"  {r}")
    print()
