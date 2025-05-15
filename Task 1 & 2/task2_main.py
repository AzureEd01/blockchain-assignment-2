import hashlib
import json
import os
import key_pairs
from key_pairs import stored_key_pairs as keys

INVENTORY_FILE = "Task 1 & 2/inventory.txt"
AUTHORIZED_USERS = {"admin001", "manager002", "auditor003"}
CLONES = ["Inventory1", "Inventory2", "Inventory3", "Inventory4"]

# Initial inventory data
initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

# GUI-binded variables initialized later
gui_vars = {}

def set_gui_vars(vars_dict):
    global gui_vars
    gui_vars = vars_dict

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

def sign(record, inv_name):
    record_bytes = record.replace(',', '').encode('utf-8')
    gui_vars["bytes_var"].set(record_bytes)

    hashed = hashlib.sha256(record_bytes).hexdigest()
    gui_vars["hash_var"].set(hashed)

    m = int(hashed, 16)
    gui_vars["dec_var"].set(m)

    private_key = keys['inv_' + inv_name + '_priv_key']
    s = pow(m, private_key['d'], private_key['n'])
    gui_vars["sig_var"].set(s)
    return s

def verify_sig(s, inv_name, record):
    public_key = keys['inv_' + inv_name + '_pub_key']
    dec_sig = pow(s, public_key['e'], public_key['n'])
    gui_vars["decsig_var"].set(dec_sig)

    cleaned_record = record.replace(',', '')
    expected = int(hashlib.sha256(cleaned_record.encode('utf-8')).hexdigest(), 16)
    gui_vars["original_msg_hashed_val"].set(expected)

    gui_vars["valid_var"].set("yes" if dec_sig == expected else "no")

def display_calcs(inv_name):
    attrs = ['p', 'q', 'e', 'n', 'd', 'phin']
    for attr in attrs:
        gui_vars[f"{attr}_var"].set(getattr(key_pairs, f'inv_{inv_name}_{attr}'))

def submit(itemid_var, qty_var, price_var, location_var, authority_var, error_var):
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
