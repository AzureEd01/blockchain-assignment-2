import tkinter as tk
import task2_main as logic # calculation logic

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

# Bind GUI vars to logic
logic.set_gui_vars({
    "p_var": p_var, "q_var": q_var, "e_var": e_var, "n_var": n_var,
    "d_var": d_var, "phin_var": phin_var,
    "bytes_var": bytes_var, "hash_var": hash_var, "dec_var": dec_var,
    "sig_var": sig_var, "decsig_var": decsig_var,
    "valid_var": valid_var, "original_msg_hashed_val": original_msg_hashed_val
})

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

tk.Button(m, text='Add Item + Sign',
          command=lambda: logic.submit(itemid_var, qty_var, price_var, location_var, authority_var, error_var)).grid(row=5, column=0, columnspan=2)

tk.Label(m, textvariable=error_var, fg="red").grid(row=6, column=0, columnspan=2)

tk.Label(m, text='=== RSA Calculations ===').grid(row=7, column=0, columnspan=2)

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
