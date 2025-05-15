#libraries
import hashlib
# from keys import gen_partial_sig
# from keys import gen_multi_sig
# from pkg_server import pkg_search_qty
from pkg_server import keygen
from inventory_A_server import calc_tA

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
    #searches for a item id to get the qty---------
    record_id = record_var.get()
    #A
    from inventory_A_server import inventory_A_search
    qty_A = inventory_A_search(record_id)
    #B
    from inventory_B_server import inventory_B_search
    qty_B = inventory_B_search(record_id)
    #C
    from inventory_C_server import inventory_C_search
    qty_C = inventory_C_search(record_id)
    #D
    from inventory_D_server import inventory_D_search
    qty_D = inventory_D_search(record_id)

    #calculate t for signing ------------------------
    #get tA
    tA = calc_tA()
    print("tA is ", tA)

    #Get tB
    from inventory_B_server import calc_tB
    tB = calc_tB()
    print("tB is: ", tB)

    #Get tC
    from inventory_C_server import calc_tC
    tC = calc_tC()
    print("tC is: ", tC)

    #Get tD
    from inventory_D_server import calc_tD
    tD = calc_tD()
    print("tD is: ", tD)
    #------------------------------------------------
    #Calculate aggregated t -------------------------
    #A
    from inventory_A_server import a_calc_aggregated_t
    inv_a_agg_t = a_calc_aggregated_t(tA, tB, tC, tD)
    print("Inv A, Aggregated t= ", inv_a_agg_t)
    #B
    from inventory_B_server import b_calc_aggregated_t
    inv_b_agg_t = b_calc_aggregated_t(tA, tB, tC, tD)
    print("Inv B, Aggregated t= ", inv_b_agg_t)
    #C
    from inventory_C_server import c_calc_aggregated_t
    inv_c_agg_t = c_calc_aggregated_t(tA, tB, tC, tD)
    print("Inv C, Aggregated t= ", inv_c_agg_t)
    #D
    from inventory_D_server import d_calc_aggregated_t
    inv_d_agg_t = d_calc_aggregated_t(tA, tB, tC, tD)
    print("Inv D, Aggregated t= ", inv_d_agg_t)
    #-----------------------------------------------
    #Get secret keys from PKG
    #A
    from inventory_A_server import get_privkey_A
    gA = get_privkey_A()
    print("Inv A priv key: ", gA)
    #B
    from inventory_B_server import get_privkey_B
    gB = get_privkey_B()
    print("Inv B priv key: ", gB)
    #C
    from inventory_C_server import get_privkey_C
    gC = get_privkey_C()
    print("Inv C priv key: ", gC)
    #D
    from inventory_D_server import get_privkey_D
    gD = get_privkey_D()
    print("Inv D priv key: ", gD)
    #------------------------------------------------
    #partial signature calculations 
    #A
    from inventory_A_server import a_calc_partial_sig
    sA = a_calc_partial_sig(qty_A, inv_a_agg_t, gA)
    print("Inv A partial sig: ", sA)
    #B
    from inventory_B_server import b_calc_partial_sig
    sB = b_calc_partial_sig(qty_B, inv_b_agg_t, gB)
    print("Inv B partial sig: ", sB)
    #C
    from inventory_C_server import c_calc_partial_sig
    sC = c_calc_partial_sig(qty_C, inv_c_agg_t, gC)
    print("Inv C partial sig: ", sC)
    #D
    from inventory_D_server import d_calc_partial_sig
    sD = d_calc_partial_sig(qty_D, inv_d_agg_t, gD)
    print("Inv D partial sig: ", sD)
    #------------------------------------------------
    #calculating multi-signature
    #A
    from inventory_A_server import a_calc_multisig
    a_multi_s = a_calc_multisig(sA, sB, sC, sD)
    print("Inv A, Multi-sig: ", a_multi_s)
    #B
    from inventory_B_server import b_calc_multisig
    b_multi_s = b_calc_multisig(sA, sB, sC, sD)
    print("Inv B, Multi-sig: ", b_multi_s)
    #C
    from inventory_C_server import c_calc_multisig
    c_multi_s = c_calc_multisig(sA, sB, sC, sD)
    print("Inv C, Multi-sig: ", c_multi_s)
    #D
    from inventory_D_server import d_calc_multisig
    d_multi_s = d_calc_multisig(sA, sB, sC, sD)
    print("Inv D, Multi-sig: ", d_multi_s)
    #------------------------------------------------
    
    #PKG encrypts the message for validation
    from pkg_server import pkg_encrypt_message
    a_validation_result = pkg_encrypt_message(a_multi_s)
    print("Valid with A: ", a_validation_result)
    b_validation_result = pkg_encrypt_message(b_multi_s)
    print("Valid with B: ", b_validation_result)
    c_validation_result = pkg_encrypt_message(c_multi_s)
    print("Valid with C: ", c_validation_result)
    d_validation_result = pkg_encrypt_message(d_multi_s)
    print("Valid with D: ", d_validation_result)

    #result is computedt using identities 
    from pkg_server import pkg_encrypt_second
    second_validation_result = pkg_encrypt_second(tA, qty_A)
    print("Second validation: ", second_validation_result)


#UI--------------------------------------------------
#prompt to ask for an ID to search for 
tk.Label(m, text='Item ID: ').grid(row=0)
#inputbox
tk.Entry(m, textvariable = record_var).grid(row=0, column= 1)
#enter button
entBtn = tk.Button(m, text='Enter', command = submit).grid(row=2, column= 0)

m.mainloop()