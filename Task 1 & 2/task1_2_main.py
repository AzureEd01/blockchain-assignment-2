import hashlib
import json
import time
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

import key_pairs
from key_pairs import stored_key_pairs as keys

INVENTORY_FILES = ["A_inventory_db.txt", "B_inventory_db.txt", "C_inventory_db.txt", "D_inventory_db.txt"]
BLOCKCHAIN_FILE = "blockchain_log.txt"

initial_inventory = [
    "001,18,19,C",
    "002,20,14,C",
    "003,22,16,B",
    "004,12,18,A"
]

def md5_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

def proof_of_work(data: dict, difficulty: int = 6):
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

# def save_block_to_file(block: dict):
#     with open(BLOCKCHAIN_FILE, "a") as f:
#         f.write(json.dumps(block, indent=2))
#         f.write("\n" + "=" * 60 + "\n")

def load_inventory_file(filename: str) -> list:
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            for line in initial_inventory:
                f.write(line + "\n")
        return initial_inventory.copy()
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def load_all_inventories() -> list:
    return load_inventory_file(INVENTORY_FILES[0])

def check_duplicate_itemid(itemid: str) -> bool:
    for file in INVENTORY_FILES:
        inventory = load_inventory_file(file)
        for line in inventory:
            parts = line.split(",")
            if parts[0] == itemid:
                return True
    return False

def save_inventory_to_all(inventory_lines: list):
    for file in INVENTORY_FILES:
        with open(file, "w") as f:
            for line in inventory_lines:
                f.write(line + "\n")

# RSA signing functions with detailed logging:

def sign(record, inv_name, log_func=None):
    if log_func:
        log_func("\n=== RSA Signing ===")
        log_func(f"Record to sign: {record}")

    record_bytes = record.encode('utf-8')
    hashed_record = hashlib.sha256(record_bytes).hexdigest()

    if log_func:
        log_func(f"SHA-256 hash of record (hex): {hashed_record}")

    m = int(hashed_record, 16)
    if log_func:
        log_func(f"Hash converted to int (m): {m}")

    private_key_pair = keys['inv_'+inv_name+'_priv_key']
    n = private_key_pair['n']
    d = private_key_pair['d']

    if log_func:
        log_func(f"Private key d: {d}")
        log_func(f"Private key n: {n}")

    s = pow(m, d, n)

    if log_func:
        log_func(f"Signature (s = m^d mod n): {s}")
    return s

def verify_sig(s, inv_name, record, log_func=None):
    if log_func:
        log_func("\n=== RSA Verification ===")
        log_func(f"Signature (int): {s}")

    public_key_pair = keys['inv_'+inv_name+'_pub_key']
    e = public_key_pair['e']
    n = public_key_pair['n']

    if log_func:
        log_func(f"Public key e: {e}")
        log_func(f"Public key n: {n}")

    dec_sig = pow(s, e, n)

    if log_func:
        log_func(f"Decrypted signature (m' = s^e mod n): {dec_sig}")

    hashed_record = hashlib.sha256(record.encode('utf-8')).hexdigest()
    decimal_hash = int(hashed_record, 16)

    if log_func:
        log_func(f"SHA-256 hash of original record (int): {decimal_hash}")

    valid = dec_sig == decimal_hash
    if log_func:
        log_func(f"Signature valid? {'Yes' if valid else 'No'}")
    return valid

# Inventory with only RSA detailed logs

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Blockchain with RSA Signing Logs")

        self.create_widgets()
        self.initialize_blockchain()

    def create_widgets(self):
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

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.log_output = scrolledtext.ScrolledText(self.root, width=90, height=30, state='disabled', font=("Consolas", 10))
        self.log_output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def log(self, message):
        self.log_output.configure(state='normal')
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.configure(state='disabled')
        self.log_output.see(tk.END)

    def initialize_blockchain(self):
        self.blockchain = []
        if not os.path.exists(BLOCKCHAIN_FILE):
            self.log("Creating genesis block...")
            inventory = load_all_inventories()
            inventory_dict = [self.parse_line_to_dict(line) for line in inventory]
            genesis_block = proof_of_work({"inventory": inventory_dict})
            self.blockchain.append(genesis_block)
            # save_block_to_file(genesis_block)
            self.log(f"Genesis block created in {genesis_block['time_taken']:.2f} seconds.")
        else:
            self.log("Blockchain log exists. Ready for new blocks.")

    def parse_line_to_dict(self, line: str) -> dict:
        parts = line.split(",")
        return {
            "ItemID": parts[0],
            "ItemQTY": int(parts[1]),
            "ItemPrice": int(parts[2]),
            "Location": parts[3]
        }

    def add_item(self):
        try:
            itemid = self.entry_id.get().strip()
            qty = int(self.entry_qty.get())
            price = int(self.entry_price.get())
            location = self.entry_location.get().strip().upper()

            if not itemid or not location:
                messagebox.showerror("Input Error", "ItemID and Location cannot be empty.")
                return

            if location not in ['A','B','C','D']:
                messagebox.showerror("Input Error", "Location must be one of A, B, C, or D.")
                return

            if check_duplicate_itemid(itemid):
                messagebox.showerror("Duplicate Error", f"ItemID '{itemid}' already exists in the inventory.")
                return

            record_for_signing = f"{itemid}{qty}{price}{location}"

            # Sign the record with detailed logs
            signature = sign(record_for_signing, location.lower(), log_func=self.log)

            # Verify the signature with detailed logs
            valid = verify_sig(signature, location.lower(), record_for_signing, log_func=self.log)

            new_record = f"{itemid},{qty},{price},{location}"

            inventory = load_all_inventories()
            inventory.append(new_record)

            inventory_dict = [self.parse_line_to_dict(line) for line in inventory]

            # Mining block but no detailed logs
            new_block = proof_of_work({"inventory": inventory_dict})
            self.blockchain.append(new_block)

            save_inventory_to_all(inventory)
            # save_block_to_file(new_block)

            self.log(f"\nBlock mined with nonce {new_block['nonce']} and hash {new_block['hash']}")
            self.log(f"⏱️ Mining took {new_block['time_taken']:.2f} seconds.")
            self.log("Inventory and blockchain updated.\n" + "="*60 + "\n")

            self.entry_id.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_location.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for quantity and price.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
