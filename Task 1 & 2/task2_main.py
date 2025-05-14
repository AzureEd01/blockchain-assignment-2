import tkinter as tk
import hashlib
import json
import os
import key_pairs
from key_pairs import stored_key_pairs as keys

# === Inventory Setup ===
INVENTORY_FILE = "inventory.txt"
AUTHORIZED_USERS = {"admin001", "manager002", "auditor003"}
CLONES = ["Inventory1", "Inventory2", "Inventory3", "Inventory4"]

initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

def initialize_inventory():
    data = {clone: initial_inventory.copy() for clone in CLONES}
    save_inventory(data)
    return data

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return initialize_inventory()
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=2)

# === RSA Functions ===
def sign(record, inv_name):
    record_bytes = record.encode('utf-8')
    bytes_var.set(record_bytes)
    
    hashed = hashlib.sha256(record_bytes).hexdigest()
    hash_var.set(hashed)
    
    m = int(hashed, 16)
    dec_var.set(m)
    
    private_key = keys['inv_' + inv_name + '_priv_key']
    s = pow(m, private_key['d'], private_key['n'])
    sig_var.set(s)
    return s

def verify_sig(s, inv_name, record):
    public_key = keys['inv_' + inv_name + '_pub_key']
    dec_sig = pow(s, public_key['e'], public_key['n'])
    decsig_var.set(dec_sig)
    
    expected = int(hashlib.sha256(record.encode('utf-8')).hexdigest(), 16)
    original_msg_hashed_val.set(expected)
    
    valid_var.set("yes" if dec_sig == expected else "no")

def display_calcs(inv_name):
    attrs = ['p', 'q', 'e', 'n', 'd', 'phin']
    for attr in attrs:
        globals()[f'{attr}_var'].set(getattr(key_pairs, f'inv_{inv_name}_{attr}'))

# === Inventory Add + Sign Logic ===
def submit():
    try:
        item_id = itemid_var.get().strip()
        qty = int(qty_var.get())
        price = int(price_var.get())
        loc = location_var.get().strip().upper()
        authority = authority_var.get().strip()
        
        if authority not in AUTHORIZED_USERS:
            error_var.set("Unauthorized authority ID.")
            return
        
        inv_data = load_inventory()
        base_inventory = inv_data["Inventory1"]
        
        if any(item["ItemID"] == item_id for item in base_inventory):
            error_var.set(f"ItemID '{item_id}' already exists.")
            return
        
        new_item = {
            "ItemID": item_id,
            "ItemQTY": qty,
            "ItemPrice": price,
            "Location": loc
        }

        updated_inventory = base_inventory + [new_item]
        for clone in CLONES:
            inv_data[clone] = updated_inventory.copy()
        save_inventory(inv_data)

        record = f"{item_id},{qty},{price},{loc}"
        signature = sign(record, loc.lower())
        display_calcs(loc.lower())
        verify_sig(signature, loc.lower(), record)
        error_var.set("✅ Item added and signed successfully!")

    except ValueError as ve:
        error_var.set(f"Value Error: {ve}")
    except Exception as e:
        error_var.set(f"Error: {e}")

# === GUI Setup ===
m = tk.Tk()
m.title("Inventory Manager + RSA Signer")

# Input Vars
itemid_var = tk.StringVar()
qty_var = tk.StringVar()
price_var = tk.StringVar()
location_var = tk.StringVar()
authority_var = tk.StringVar()
error_var = tk.StringVar()

# RSA Display Vars
p_var, q_var, e_var, n_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
d_var, phin_var = tk.StringVar(), tk.StringVar()
bytes_var, hash_var, dec_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
sig_var, decsig_var, valid_var, original_msg_hashed_val = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

# === GUI Layout ===
tk.Label(m, text='ItemID').grid(row=0, column=0)
tk.Entry(m, textvariable=itemid_var).grid(row=0, column=1)

tk.Label(m, text='Quantity').grid(row=1, column=0)
tk.Entry(m, textvariable=qty_var).grid(row=1, column=1)

tk.Label(m, text='Price').grid(row=2, column=0)
tk.Entry(m, textvariable=price_var).grid(row=2, column=1)

tk.Label(m, text='Location (A/B/C/D)').grid(row=3, column=0)
tk.Entry(m, textvariable=location_var).grid(row=3, column=1)

tk.Label(m, text='Authority ID').grid(row=4, column=0)
tk.Entry(m, textvariable=authority_var).grid(row=4, column=1)

tk.Button(m, text='Add Item + Sign', command=submit).grid(row=5, column=0, columnspan=2)
tk.Label(m, textvariable=error_var, fg="red").grid(row=6, column=0, columnspan=2)

tk.Label(m, text='=== RSA Calculations ===').grid(row=7, column=0, columnspan=2)
# Display Vars
labels = [
    ("p =", p_var), ("q =", q_var), ("e =", e_var),
    ("n =", n_var), ("d =", d_var), ("phi(n) =", phin_var),
    ("Record Bytes =", bytes_var), ("Hashed =", hash_var),
    ("Decimal =", dec_var), ("Signature =", sig_var),
    ("Decrypted Sig =", decsig_var), ("Original Hash =", original_msg_hashed_val),
    ("Valid Signature?", valid_var)
]

for idx, (text, var) in enumerate(labels, start=8):
    tk.Label(m, text=text).grid(row=idx, column=0)
    tk.Label(m, textvariable=var).grid(row=idx, column=1)

m.mainloop()
