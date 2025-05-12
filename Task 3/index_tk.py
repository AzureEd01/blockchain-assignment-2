import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

# Cryptographic constants
pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

pkg_n = pkg_p * pkg_q
pkg_phi_n = (pkg_p - 1) * (pkg_q - 1)
pkg_d = pow(pkg_e, -1, pkg_phi_n) % pkg_phi_n

# Inventory IDs and randoms
inventory_ids = {
    "A": 126,
    "B": 127,
    "C": 128,
    "D": 129
}
randoms = {
    "A": 621,
    "B": 721,
    "C": 821,
    "D": 921
}

def compute_signature(concatenated_msg):
    results = []
    
    # Secret Keys
    g = {k: pow(v, pkg_d, pkg_n) % pkg_n for k, v in inventory_ids.items()}
    results.append(f"Secret Keys: {g}")
    
    # Signature of Random Integers
    t_vals = {k: pow(v, pkg_e, pkg_n) % pkg_n for k, v in randoms.items()}
    results.append(f"t values: {t_vals}")
    
    # Aggregated t
    t = 1
    for val in t_vals.values():
        t = (t * val) % pkg_n
    results.append(f"Aggregated t: {t}")
    
    # Message Append
    m = str(t) + concatenated_msg
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)
    
    results.append(f"Concatenated Message: {m}")
    results.append(f"Hash (MD5): {hash_m}")
    results.append(f"Decimal Hash: {decimal_m}")
    
    # Individual Signatures
    s_vals = {}
    for k in inventory_ids.keys():
        s_k = g[k] * randoms[k]
        s_k = pow(s_k, decimal_m, pkg_n) % pkg_n
        s_vals[k] = s_k
    results.append(f"Signatures: {s_vals}")
    
    # Final Signature
    s = 1
    for val in s_vals.values():
        s = (s * val) % pkg_n
    results.append(f"Final Signature (s, t): ({s}, {t})")
    
    return "\n".join(results)

def on_calculate():
    item_id = entry_item_id.get().strip()
    item_qty = entry_item_qty.get().strip()
    item_price = entry_item_price.get().strip()
    location = entry_location.get().strip()

    if not (item_id and item_qty and item_price and location):
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    
    # Concatenate inputs into a solid string
    concatenated_msg = f"{item_id}{item_qty}{item_price}{location}"

    output_text.delete(1.0, tk.END)
    result = compute_signature(concatenated_msg)
    output_text.insert(tk.END, result)

# ===================== TKINTER GUI SETUP =====================

root = tk.Tk()
root.title("Inventory Signature System")
root.geometry("750x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# ------------------ Tab 1: Signature Generation ------------------ #
tab_gen = ttk.Frame(notebook)
notebook.add(tab_gen, text='Generate Signature')

tk.Label(tab_gen, text="Item ID:").pack()
entry_item_id = tk.Entry(tab_gen, width=50)
entry_item_id.pack(pady=2)

tk.Label(tab_gen, text="Item Quantity:").pack()
entry_item_qty = tk.Entry(tab_gen, width=50)
entry_item_qty.pack(pady=2)

tk.Label(tab_gen, text="Item Price:").pack()
entry_item_price = tk.Entry(tab_gen, width=50)
entry_item_price.pack(pady=2)

tk.Label(tab_gen, text="Location:").pack()
entry_location = tk.Entry(tab_gen, width=50)
entry_location.pack(pady=2)

tk.Button(tab_gen, text="Generate Signature", command=on_calculate).pack(pady=10)

output_text = tk.Text(tab_gen, height=20, width=80)
output_text.pack()

# ------------------ Tab 2: Verification (placeholder) ------------------ #
tab_verify = ttk.Frame(notebook)
notebook.add(tab_verify, text='Verify Signature')

tk.Label(tab_verify, text="Verification system coming soon...").pack(pady=20)

# ===================== RUN =====================
root.mainloop()
