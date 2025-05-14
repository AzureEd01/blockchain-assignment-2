#libraries
import hashlib
from keys import gen_partial_sig
from keys import gen_multi_sig

# ==========================================================================================================================
# Signature
# ==========================================================================================================================

# # procurement officer
# No idea where to use this
# p = 1080954735722463992988394149602856332100628417
# q = 1158106283320086444890911863299879973542293243
# e = 106506253943651610547613


# ==========================================================================================================================
# Verification
# ==========================================================================================================================
import tkinter as tk
#create a widget (named m for master)
m= tk.Tk()
record_var = tk.StringVar()

def file_search(inv_name, record_id):
    filename = inv_name + "_inventory_db.txt"

    #f is now the file object 
    with open(filename) as f:
        lines = f.readlines()
        item_qty = ''
        for row in lines:
            id = record_id
            #checking if the id is in the line
            if row.find(id) != -1:
                #break the line up so we can get the qty
                print(row.split(','))
                split_row = row.split(',')
                #get the qty (2nd value)
                qty = split_row[1]
                item_qty = qty
                return item_qty
        if not item_qty:
            print("Item doesnt exist.")
            return "not found"

def submit():
    #function for submit button
    #2: user query submission
    record_id = record_var.get()
    #3.a: Each inventory node searches its local database for the requested item record.
    qty_A = file_search('A', record_id)
    qty_B = file_search('B', record_id)
    qty_C = file_search('C', record_id)
    qty_D = file_search('D', record_id)
    #3.b: Each inventory generates partial signatures and combines their signatures with the Harn identity-based multi-signature algorithm
    #might add a wile not empty loop here
    s1 = gen_partial_sig('A', qty_A)
    s2 = gen_partial_sig('B', qty_B)
    s3 = gen_partial_sig('C', qty_C)
    s4 = gen_partial_sig('D', qty_D)
    #combining for multisig 
    s = gen_multi_sig(s1, s2, s3, s4)

#UI--------------------------------------------------------------------------------------------------
#prompt to ask for an ID to search for 
tk.Label(m, text='Item ID: ').grid(row=0)
#inputbox
tk.Entry(m, textvariable = record_var).grid(row=0, column= 1)
#enter button
entBtn = tk.Button(m, text='Enter', command = submit).grid(row=2, column= 0)

m.mainloop()