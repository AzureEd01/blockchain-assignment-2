# gui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
from test3 import load_inventory, save_full_inventory, proof_of_work, save_block_to_file, BLOCKCHAIN_FILE

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Blockchain")
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

        self.entry_id.grid(row=0, column=1)
        self.entry_qty.grid(row=1, column=1)
        self.entry_price.grid(row=2, column=1)

        self.location_var = tk.StringVar(self.root)
        self.location_var.set("A")
        self.entry_location = tk.OptionMenu(self.root, self.location_var, "A", "B", "C", "D")
        self.entry_location.grid(row=3, column=1)

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

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
                "ItemID": self.entry_id.get().strip(),
                "ItemQTY": int(self.entry_qty.get().strip()),
                "ItemPrice": int(self.entry_price.get().strip()),
                "Location": self.location_var.get()
            }

            inventory = load_inventory()
            updated_inventory = [i for i in inventory if i["ItemID"] != item["ItemID"]] + [item]

            self.log("Mining block... please wait.")
            new_block = proof_of_work({"inventory": updated_inventory})
            self.blockchain.append(new_block)

            save_block_to_file(new_block)
            save_full_inventory(item)

            self.log(f"✅ Block mined with nonce {new_block['nonce']} and hash {new_block['hash']}")
            self.log(f"⏱️ Mining took {new_block['time_taken']:.2f} seconds.")
            self.log("Inventory and blockchain updated.")

            self.entry_id.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            # after mining and updating blockchain...

            save_block_to_file(new_block)
            save_full_inventory(updated_inventory)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for quantity and price.")
