import hashlib
import json
import time
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

INVENTORY_FILE = "inventory.txt"
BLOCKCHAIN_FILE = "blockchain_log.txt"

initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

def md5_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

def proof_of_work(data: dict, difficulty: int = 4):
    base_string = json.dumps(data, sort_keys=True)
    nonce = 0
    start_time = time.time()
    
    while True:
        trial = base_string + str(nonce)
        hashed = md5_hash(trial)
        if hashed.startswith('0' * difficulty):
            end_time = time.time()
            return {
                "timestamp": end_time,
                "data": data,
                "nonce": nonce,
                "hash": hashed,
                "time_taken": end_time - start_time
            }
        nonce += 1


def save_block_to_file(block: dict):
    with open(BLOCKCHAIN_FILE, "a") as f:
        f.write(json.dumps(block, indent=2))
        f.write("\n" + "=" * 60 + "\n")

def load_inventory() -> list:
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "w") as f:
            json.dump(initial_inventory, f, indent=2)
        return initial_inventory
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(inventory: list):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=2)

# GUI Application
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Blockchain")

        self.create_widgets()
        self.initialize_blockchain()

    def create_widgets(self):
        # Entry Fields
        tk.Label(self.root, text="ItemID").grid(row=0, column=0)
        tk.Label(self.root, text="ItemQTY").grid(row=1, column=0)
        tk.Label(self.root, text="ItemPrice").grid(row=2, column=0)
        tk.Label(self.root, text="Location").grid(row=3, column=0)

        self.entry_id = tk.Entry(self.root)
        self.entry_qty = tk.Entry(self.root)
        self.entry_price = tk.Entry(self.root)
        self.entry_location = tk.Entry(self.root)

        self.entry_id.grid(row=0, column=1)
        self.entry_qty.grid(row=1, column=1)
        self.entry_price.grid(row=2, column=1)
        self.entry_location.grid(row=3, column=1)

        # Add Button
        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Log Output
        self.log_output = scrolledtext.ScrolledText(self.root, width=60, height=15, state='disabled')
        self.log_output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def log(self, message):
        self.log_output.configure(state='normal')
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.configure(state='disabled')
        self.log_output.see(tk.END)

    def initialize_blockchain(self):
        self.blockchain = []
        inventory = load_inventory()

        if not os.path.exists(BLOCKCHAIN_FILE):
            self.log("Creating genesis block...")
            genesis_block = proof_of_work({"inventory": inventory})
            self.blockchain.append(genesis_block)
            save_block_to_file(genesis_block)
            self.log(f"✅ Genesis block created in {genesis_block['time_taken']:.2f} seconds.")

        else:
            self.log("Blockchain log exists. Appending new blocks.")

    def add_item(self):
        try:
            item = {
                "ItemID": self.entry_id.get(),
                "ItemQTY": int(self.entry_qty.get()),
                "ItemPrice": int(self.entry_price.get()),
                "Location": self.entry_location.get()
            }

            inventory = load_inventory()
            updated_inventory = inventory + [item]

            self.log("Mining block... please wait.")
            new_block = proof_of_work({"inventory": updated_inventory})
            self.blockchain.append(new_block)

            save_block_to_file(new_block)
            save_inventory(updated_inventory)

            self.log(f"✅ Block mined with nonce {new_block['nonce']} and hash {new_block['hash']}")
            self.log(f"⏱️ Mining took {new_block['time_taken']:.2f} seconds.")
            self.log("Inventory and blockchain updated.")


            # Clear inputs
            self.entry_id.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_location.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for quantity and price.")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
