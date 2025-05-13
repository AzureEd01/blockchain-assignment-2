import tkinter as tk
from tkinter import messagebox, scrolledtext
import hashlib
import time
import random

# ========== Blockchain Components ==========

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8') + 
                   str(self.previous_hash).encode('utf-8') + 
                   str(self.nonce).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.mine_block(DIFFICULTY)
        self.chain.append(new_block)

    def get_chain_as_text(self):
        text = ""
        for i, block in enumerate(self.chain):
            text += f"Block {i}:\n"
            text += f"  Data: {block.data}\n"
            text += f"  Nonce: {block.nonce}\n"
            text += f"  Hash: {block.hash}\n"
            text += f"  Previous Hash: {block.previous_hash}\n\n"
        return text

# ========== Inventory + UI Components ==========

# Initial inventory
initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

# Simulated nodes
inventories = {
    "Node1": initial_inventory.copy(),
    "Node2": initial_inventory.copy(),
    "Node3": initial_inventory.copy(),
    "Node4": initial_inventory.copy(),
}

DIFFICULTY = 4
blockchain = Blockchain()

def record_to_string(record):
    return f"{record['ItemID']}-{record['ItemQTY']}-{record['ItemPrice']}-{record['Location']}"

def is_valid_record(record, inventory):
    return all(existing["ItemID"] != record["ItemID"] for existing in inventory)

def log_output(msg):
    output_console.insert(tk.END, msg + "\n")
    output_console.see(tk.END)

def display_inventories():
    inventory_display.delete(1.0, tk.END)
    for node, records in inventories.items():
        inventory_display.insert(tk.END, f"{node}:\n")
        for r in records:
            inventory_display.insert(tk.END, f"  {r}\n")
        inventory_display.insert(tk.END, "\n")

def display_blockchain():
    chain_display.delete(1.0, tk.END)
    chain_display.insert(tk.END, blockchain.get_chain_as_text())

def submit_record():
    item_id = entry_id.get().strip()
    try:
        qty = int(entry_qty.get().strip())
        price = int(entry_price.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Quantity and Price must be numbers.")
        return
    location = entry_location.get().strip().upper()

    if not (item_id and location):
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    new_record = {
        "ItemID": item_id,
        "ItemQTY": qty,
        "ItemPrice": price,
        "Location": location,
    }

    record_str = record_to_string(new_record)
    miner = random.choice(list(inventories.keys()))
    log_output(f"\n[INFO] Miner selected: {miner}")

    valid = True
    for node, inventory in inventories.items():
        if not is_valid_record(new_record, inventory):
            log_output(f"[REJECT] {node} found duplicate ItemID.")
            valid = False
            break

    if valid:
        for node in inventories:
            inventories[node].append(new_record)

        # Add to blockchain
        block = Block(f"ADD: {record_str}", blockchain.chain[-1].hash)
        blockchain.add_block(block)

        log_output("[CONSENSUS] Record added to all nodes and mined.\n")
        display_inventories()
        display_blockchain()
    else:
        log_output("[CONSENSUS] Record rejected.\n")

def perform_search():
    search_term = entry_search.get().strip()
    if not search_term:
        messagebox.showerror("Input Error", "Please enter an ItemID to search.")
        return

    query_str = f"SEARCH_QUERY: ItemID={search_term}"
    log_output(f"\n[SEARCH] Starting Proof-of-Work for query: {query_str}")

    # Mine the query block (PoW)
    mined_block = Block(query_str, blockchain.chain[-1].hash)
    blockchain.add_block(mined_block)

    log_output(f"[MINED] Query block added to blockchain with hash: {mined_block.hash}")

    # Now perform the actual search
    found = False
    for node, records in inventories.items():
        for record in records:
            if record["ItemID"] == search_term:
                log_output(f"[{node}] Found: {record}")
                found = True
    if not found:
        log_output(f"[RESULT] ItemID '{search_term}' not found in any node.")

    display_blockchain()


# ========== UI Setup ==========

root = tk.Tk()
root.title("Inventory Blockchain PoW Demo")

# Input Fields
tk.Label(root, text="ItemID:").grid(row=0, column=0, sticky='e')
entry_id = tk.Entry(root, width=20)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Quantity:").grid(row=1, column=0, sticky='e')
entry_qty = tk.Entry(root, width=20)
entry_qty.grid(row=1, column=1)

tk.Label(root, text="Price:").grid(row=2, column=0, sticky='e')
entry_price = tk.Entry(root, width=20)
entry_price.grid(row=2, column=1)

tk.Label(root, text="Location:").grid(row=3, column=0, sticky='e')
entry_location = tk.Entry(root, width=20)
entry_location.grid(row=3, column=1)

submit_btn = tk.Button(root, text="Add Record", command=submit_record)
submit_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Search Section
tk.Label(root, text="Search ItemID:").grid(row=5, column=0, sticky='e')
entry_search = tk.Entry(root, width=20)
entry_search.grid(row=5, column=1)

search_btn = tk.Button(root, text="Search with PoW", command=perform_search)
search_btn.grid(row=6, column=0, columnspan=2, pady=5)

# Output Console
tk.Label(root, text="Console Output:").grid(row=7, column=0, columnspan=2)
output_console = scrolledtext.ScrolledText(root, height=10, width=60)
output_console.grid(row=8, column=0, columnspan=2)

# Inventory Display
tk.Label(root, text="Node Inventories:").grid(row=9, column=0, columnspan=2)
inventory_display = scrolledtext.ScrolledText(root, height=10, width=60)
inventory_display.grid(row=10, column=0, columnspan=2)

# Blockchain Display
tk.Label(root, text="Blockchain:").grid(row=11, column=0, columnspan=2)
chain_display = scrolledtext.ScrolledText(root, height=12, width=60)
chain_display.grid(row=12, column=0, columnspan=2)

display_inventories()
display_blockchain()
root.mainloop()
