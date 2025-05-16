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



# ==========================================================================================================================
# Verification
# ==========================================================================================================================
import tkinter as tk
#create a widget (named m for master)
m= tk.Tk()
record_var = tk.StringVar()

def submit():
    # PKG makes the keys 
    keygen()

    record_id = record_var.get()

    # Inventory lookups
    from inventory_A_server import inventory_A_search
    qty_A = inventory_A_search(record_id)

    from inventory_B_server import inventory_B_search
    qty_B = inventory_B_search(record_id)

    from inventory_C_server import inventory_C_search
    qty_C = inventory_C_search(record_id)

    from inventory_D_server import inventory_D_search
    qty_D = inventory_D_search(record_id)

    # Calculate t values
    from inventory_A_server import calc_tA
    tA = calc_tA()
    print("tA is ", tA)

    from inventory_B_server import calc_tB
    tB = calc_tB()
    print("tB is: ", tB)

    from inventory_C_server import calc_tC
    tC = calc_tC()
    print("tC is: ", tC)

    from inventory_D_server import calc_tD
    tD = calc_tD()
    print("tD is: ", tD)

    # Calculate aggregated t
    from inventory_A_server import a_calc_aggregated_t
    inv_a_agg_t = a_calc_aggregated_t(tA, tB, tC, tD)
    print("Agg T = ", inv_a_agg_t)

    from inventory_B_server import b_calc_aggregated_t
    inv_b_agg_t = b_calc_aggregated_t(tA, tB, tC, tD)

    from inventory_C_server import c_calc_aggregated_t
    inv_c_agg_t = c_calc_aggregated_t(tA, tB, tC, tD)

    from inventory_D_server import d_calc_aggregated_t
    inv_d_agg_t = d_calc_aggregated_t(tA, tB, tC, tD)

    # Get private keys
    from inventory_A_server import get_privkey_A
    gA = get_privkey_A()
    print("gA: ", gA)

    from inventory_B_server import get_privkey_B
    gB = get_privkey_B()
    print("gB: ", gB)

    from inventory_C_server import get_privkey_C
    gC = get_privkey_C()
    print("gC: ", gC)

    from inventory_D_server import get_privkey_D
    gD = get_privkey_D()
    print("gD: ", gD)

    # Generate partial signatures
    from inventory_A_server import a_calc_partial_sig
    sA = a_calc_partial_sig(qty_A, inv_a_agg_t, gA)
    print("sA: ", sA)

    from inventory_B_server import b_calc_partial_sig
    sB = b_calc_partial_sig(qty_B, inv_b_agg_t, gB)
    print("sB: ", sB)

    from inventory_C_server import c_calc_partial_sig
    sC = c_calc_partial_sig(qty_C, inv_c_agg_t, gC)
    print("sC: ", sC)

    from inventory_D_server import d_calc_partial_sig
    sD = d_calc_partial_sig(qty_D, inv_d_agg_t, gD)
    print("sD: ", sD)

    # Multi-signature calculation
    from inventory_A_server import a_calc_multisig
    a_multi_s = a_calc_multisig(sA, sB, sC, sD)
    print("Multi-sig: ", a_multi_s)

    from inventory_B_server import b_calc_multisig
    b_multi_s = b_calc_multisig(sA, sB, sC, sD)

    from inventory_C_server import c_calc_multisig
    c_multi_s = c_calc_multisig(sA, sB, sC, sD)

    from inventory_D_server import d_calc_multisig
    d_multi_s = d_calc_multisig(sA, sB, sC, sD)

    # Validation
    from user import proc_validate_message
    print("Valid with A: ", proc_validate_message(a_multi_s))
    print("Valid with B: ", proc_validate_message(b_multi_s))
    print("Valid with C: ", proc_validate_message(c_multi_s))
    print("Valid with D: ", proc_validate_message(d_multi_s))

    from user import proc_validate_second
    print("Second validation: ", proc_validate_second(qty_A, inv_a_agg_t))
    print("var 1: ", inv_a_agg_t)
    print ("var 2: ", qty_A)
    
    # PBFT Consensus
    proposal = {
        'qty': qty_A,
        'agg_t': inv_a_agg_t,
        's': sA  # from a_calc_partial_sig()
    }

    from inventory_B_server import pbft_vote_on_primary as vote_B
    from inventory_C_server import pbft_vote_on_primary as vote_C
    from inventory_D_server import pbft_vote_on_primary as vote_D

    vote_result_B = vote_B(proposal)
    vote_result_C = vote_C(proposal)
    vote_result_D = vote_D(proposal)

    votes = [vote_result_B, vote_result_C, vote_result_D]

    # Add A's own signature to the list
    votes.append(sA)

    # Simple consensus check: find majority result
    from collections import Counter
    vote_counts = Counter(votes)
    majority_result, count = vote_counts.most_common(1)[0]

    if count > 1:
        print("✔ PBFT consensus reached.")
    else:
        print("✘ PBFT consensus failed. Aborting signature.")
        return  # Stop the process here

    #UI--------------------------------------------------
#prompt to ask for an ID to search for 
tk.Label(m, text='Item ID: ').grid(row=0)
#inputbox
tk.Entry(m, textvariable = record_var).grid(row=0, column= 1)
#enter button
entBtn = tk.Button(m, text='Enter', command = submit).grid(row=2, column= 0)

m.mainloop()