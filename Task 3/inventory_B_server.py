import hashlib

inventoryB_id = 127
randomB = 721
tB = ''
sB = ''
node_name = 'B'

def inv_B_key_req():
    return inventoryB_id  

def get_privkey_B():
    from pkg_server import get_priv_key
    gB = get_priv_key('B')
    return gB

def calc_tB():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tB = pow(randomB, pkg_e, pkg_n)
    return tB 

def b_calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def b_calc_partial_sig(m, t, gJ):
    #get random number 
    randomJ = randomB
    #get pkg n
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    #append message to t
    m = str(t) + m
    #hash message
    hash_m = hashlib.md5(m.encode()).hexdigest()
    #convert message to int 
    decimal_m = int(hash_m, 16)
    rJ_exp = pow(randomJ, decimal_m, pkg_n)
    sJ = (gJ * rJ_exp) % pkg_n
    return sJ

def b_calc_multisig(sA, sB, sC, sD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    s = (sA * sB * sC * sD) % pkg_n
    return s 

def inventory_B_search(record_id):
     global sB
     with open('B_inventory_db.txt') as f:
        lines = f.readlines()
        item_qty = ''
        for row in lines:
            id = record_id
            if row.find(id) != -1:
                print(row.split(','))
                split_row = row.split(',')
                qty = split_row[1]
                return qty

# Consensus
# FAULTY = True

def pbft_vote_on_primary(data):
    from pkg_server import get_pkg_n, get_priv_key
    import hashlib
    # if FAULTY:
    #     return False
    qty = str(data['qty'])
    t = int(data['agg_t'])
    sB_from_proposal = int(data['sB'])  # Now expect node B’s partial sig

    gB = get_priv_key('B')
    rB = randomB
    pkg_n = get_pkg_n()

    m = str(t) + qty
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)

    r_exp = pow(rB, decimal_m, pkg_n)
    expected_sB = (gB * r_exp) % pkg_n

    print(f"[Node B] Expected signature: {expected_sB}")
    print(f"[Node B] Received signature from proposal: {sB_from_proposal}")

    return expected_sB == sB_from_proposal



