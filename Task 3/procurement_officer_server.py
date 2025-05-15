#libraries
import hashlib
from keys import gen_partial_sig
from keys import gen_multi_sig
from pkg_server import pkg_search_qty
from pkg_server import keygen

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

def submit():
#PKG makes the keys 
    keygen()


#searches for a item id to get the qty
    record_id = record_var.get()
    q = pkg_search_qty(record_id)
    print("THE THING: ", q)


#UI--------------------------------------------------------------------------------------------------
#prompt to ask for an ID to search for 
tk.Label(m, text='Item ID: ').grid(row=0)
#inputbox
tk.Entry(m, textvariable = record_var).grid(row=0, column= 1)
#enter button
entBtn = tk.Button(m, text='Enter', command = submit).grid(row=2, column= 0)

m.mainloop()