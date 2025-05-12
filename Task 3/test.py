import hashlib
import tkinter as tkt
from tkinter import messagebox

# ======================== PKG Setup ========================

pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

pkg_n = pkg_p * pkg_q
pkg_phi_n = (pkg_p - 1) * (pkg_q - 1)
pkg_d = pow(pkg_e, -1, pkg_phi_n)

# ======================== Inventory Keys ========================

IDs = {'A': 126, 'B': 127, 'C': 128, 'D': 129}
randoms = {'A': 621, 'B': 721, 'C': 821, 'D': 921}
g = {}
t = {}

for k, ID in IDs.items():
    g[k] = pow(ID, pkg_d, pkg_n)

for k, r in randoms.items():
    t[k] = pow(r, pkg_e, pkg_n)

# Aggregate t
t_agg = 1
for tk in t.values():
    t_agg = (t_agg * tk) % pkg_n

# ======================== Read Inventory from File ========================

def load_inventory_from_file(filename="inventory_db.txt"):
    inventory = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            item = {
                "ItemID": parts[0],
                "ItemQTY": int(parts[1]),
                "ItemPrice": int(parts[2]),
                "Location": parts[3]
            }
            inventory.append(item)
    return inventory

# Load inventory data
inventory_data = load_inventory_from_file()

# ======================== Function to Handle Item Processing ========================

def process_item():
    item_id = entry_item_id.get().strip()

    # Find the item in the loaded inventory
    selected_item = None
    for item in inventory_data:
        if item["ItemID"] == item_id:
            selected_item = item
            break

    if selected_item is None:
        messagebox.showerror("Error", "Invalid item ID. Please select from 001, 002, 003, 004.")
        return

    response_data = f"{selected_item['ItemID']} - {selected_item['ItemQTY']} units - ${selected_item['ItemPrice']} - Location {selected_item['Location']}"
    
    # Concatenate the aggregated t and the selected response data
    m = str(t_agg) + response_data
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)

    # Multi-signature
    sigs = {}
    for k in IDs:
        product = g[k] * randoms[k]
        sigs[k] = pow(product, decimal_m, pkg_n)

    s_total = 1
    for s in sigs.values():
        s_total = (s_total * s) % pkg_n

    verification = pow(s_total, pkg_e, pkg_n)

    # Encryption (to PO)
    po_p = 1080954735722463992988394149602856332100628417
    po_q = 1158106283320086444890911863299879973542293243
    po_e = 106506253943651610547613
    po_n = po_p * po_q
    po_phi_n = (po_p - 1) * (po_q - 1)
    po_d = pow(po_e, -1, po_phi_n)

    cipher = pow(decimal_m, po_e, po_n)
    decrypted_m = pow(cipher, po_d, po_n)

    decryption_match = decrypted_m == decimal_m

    # Display the results
    result_text = (
        f"Item {item_id} selected: {response_data}\n"
        f"MD5 hash: {hash_m}\n"
        f"Decimal of hash: {decimal_m}\n"
        f"Final Multi-signature (s): {s_total}\n"
        f"Multi-signature pair (t, s): {t_agg} {s_total}\n"
        f"Verification (s^e mod n): {verification}\n"
        f"Encrypted message: {cipher}\n"
        f"Decrypted message: {decrypted_m}\n"
        f"Decryption match: {decryption_match}"
    )
    
    # Show results in the Text widget
    text_result.delete(1.0, tkt.END)
    text_result.insert(tkt.END, result_text)

# ======================== Set up GUI ========================

# Create the main window
root = tkt.Tk()
root.title("Item ID Crypto Processor")

# Create the input label and entry widget
label_item_id = tkt.Label(root, text="Enter the 3-digit item ID (001, 002, 003, 004):")
label_item_id.pack(pady=10)

entry_item_id = tkt.Entry(root)
entry_item_id.pack(pady=10)

# Button to process the item
btn_process = tkt.Button(root, text="Process Item", command=process_item)
btn_process.pack(pady=10)

# Create a Text widget to display results
text_result = tkt.Text(root, height=15, width=80)
text_result.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
    