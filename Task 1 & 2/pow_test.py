import tkinter as tk
from tkinter import messagebox, scrolledtext
import hashlib
import time
import random

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

DIFFICULTY = 4  # Number of leading zeros required in hash

def record_to_string(record):
    return f"{record['ItemID']}-{record['ItemQTY']}-{record['ItemPrice']}-{record['Location']}"

def mine_block(base_str, difficulty, log):
    prefix = '0' * difficulty
    nonce = 0
    start_time = time.time()

    log(f"[MINING] Starting mining for: '{base_str}'")

    while True:
        text = base_str + str(nonce)
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        if hash_result.startswith(prefix):
            elapsed = time.time() - start_time
            log(f"[FOUND] Nonce: {nonce}")
            log(f"[HASH] {hash_result}")
            log(f"[TIME] {elapsed:.2f}s\n")
            return nonce, hash_result
        nonce += 1

def is_valid_record(record, inventory):
    return all(existing["ItemID"] != record["ItemID"] for existing in inventory)

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
    nonce, block_hash = mine_block(record_str, DIFFICULTY, log_output)

    valid = True
    for node, inventory in inventories.items():
        if not is_valid_record(new_record, inventory):
            log_output(f"[REJECT] {node} found duplicate ItemID.")
            valid = False
            break

    if valid:
        for node in inventories:
            inventories[node].append(new_record)
        log_output("[CONSENSUS] Record added to all nodes.\n")

        with open("mined_inventory_records.txt", "a") as file:
            file.write("==== New Record ====\n")
            file.write(f"ItemID: {item_id}\n")
            file.write(f"Quantity: {qty}\n")
            file.write(f"Price: {price}\n")
            file.write(f"Location: {location}\n")
            file.write(f"Nonce: {nonce}\n")
            file.write(f"Hash: {block_hash}\n")
            file.write("====================\n\n")
    else:
        log_output("[CONSENSUS] Record rejected.\n")

    display_inventories()

def perform_search():
    search_term = entry_search.get().strip()
    if not search_term:
        messagebox.showerror("Input Error", "Please enter an ItemID to search.")
        return

    log_output(f"\n[SEARCH] Initiating PoW to search for: '{search_term}'")
    nonce, block_hash = mine_block(search_term, DIFFICULTY, log_output)

    found = False
    output_console.insert(tk.END, f"[RESULT] Searching across nodes...\n")
    for node, records in inventories.items():
        for record in records:
            if record["ItemID"] == search_term:
                output_console.insert(tk.END, f"[{node}] Found: {record}\n")
                found = True
    if not found:
        output_console.insert(tk.END, f"[RESULT] ItemID '{search_term}' not found in any node.\n")

    output_console.see(tk.END)

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

# ================= UI ===================
root = tk.Tk()
root.title("Inventory PoW Demo")

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

# Submit Button
submit_btn = tk.Button(root, text="Add Record", command=submit_record)
submit_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Search Field and Button
tk.Label(root, text="Search ItemID:").grid(row=5, column=0, sticky='e')
entry_search = tk.Entry(root, width=20)
entry_search.grid(row=5, column=1)
search_btn = tk.Button(root, text="Search with PoW", command=perform_search)
search_btn.grid(row=6, column=0, columnspan=2, pady=5)

# Mining Output Console
tk.Label(root, text="Console Output:").grid(row=7, column=0, columnspan=2)
output_console = scrolledtext.ScrolledText(root, height=10, width=60, state='normal')
output_console.grid(row=8, column=0, columnspan=2, padx=5)

# Inventory Display
tk.Label(root, text="Node Inventories:").grid(row=9, column=0, columnspan=2)
inventory_display = scrolledtext.ScrolledText(root, height=12, width=60)
inventory_display.grid(row=10, column=0, columnspan=2, padx=5)

display_inventories()
root.mainloop()
