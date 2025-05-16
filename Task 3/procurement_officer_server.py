#imports
from pkg_server import keygen
from inventory_A_server import calc_tA
import tkinter as tk
#-----------------------------------------------------

#create a widget (named m for master)-----------------
m= tk.Tk()
record_var = tk.StringVar()

# PKG makes the keys----------------------------------
keygen()
    
#function that will run everything when the submit button is clicked------------
def submit():
    #gets the users input (the id of the item that they want the qty of)
    record_id = record_var.get()

    #Inventory lookups----------------------------------------------------------
    from inventory_A_server import inventory_A_search
    qty_A = inventory_A_search(record_id)

    from inventory_B_server import inventory_B_search
    qty_B = inventory_B_search(record_id)

    from inventory_C_server import inventory_C_search
    qty_C = inventory_C_search(record_id)

    from inventory_D_server import inventory_D_search
    qty_D = inventory_D_search(record_id)

    #Sign with Harn Multi-Sign---------------------------------------------------
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
    print("Multi-sig A: ", a_multi_s)

    from inventory_B_server import b_calc_multisig
    b_multi_s = b_calc_multisig(sA, sB, sC, sD)
    print("Multi-sig B: ", b_multi_s)

    from inventory_C_server import c_calc_multisig
    c_multi_s = c_calc_multisig(sA, sB, sC, sD)
    print("Multi-sig C: ", c_multi_s)

    from inventory_D_server import d_calc_multisig
    d_multi_s = d_calc_multisig(sA, sB, sC, sD)
    print("Multi-sig D: ", d_multi_s)
    
    # PBFT Consensus----------------------
    proposal = {
        'qty': qty_A,
        'agg_t': inv_a_agg_t,
        'sA': sA,
        'sB': sB,
        'sC': sC,
        'sD': sD,
        'tA': tA,
        'tB': tB,
        'tC': tC,
        'tD': tD
    }

    from inventory_B_server import pbft_vote_on_primary as vote_B
    from inventory_C_server import pbft_vote_on_primary as vote_C
    from inventory_D_server import pbft_vote_on_primary as vote_D

    vote_result_B = vote_B(proposal)
    vote_result_C = vote_C(proposal)
    vote_result_D = vote_D(proposal)

    votes = [vote_result_B, vote_result_C, vote_result_D]

    print("Votes from replicas:", votes)

    # Simple consensus check: at least 2 of 3 must agree
    if votes.count(True) >= 2:
        print("✔ PBFT consensus reached.")

        # --- Now encrypt, decrypt, and validate AFTER consensus ---

        # Encrypt multi-signature
        from pkg_server import pkg_encrypt
        message, encrypted_s = pkg_encrypt(qty_A, a_multi_s)
        print("Message sent: ", message)
        print("Encrypted signature: ", encrypted_s)

        # Decrypt message
        from user import proc_off_decrypt
        response_qty, decrypted_s = proc_off_decrypt(qty_A, encrypted_s)
        print("Message recieved: ", response_qty)
        print("Decrypted signature: ", decrypted_s)

        # Validation checks
        from user import proc_validate_message
        from user import proc_validate_second
        first_validation_check = proc_validate_message(decrypted_s)
        second_validation_check = proc_validate_second(qty_A, inv_a_agg_t)
        print("First validation check result: ", first_validation_check)
        print("Second validation check result: ", second_validation_check)

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
