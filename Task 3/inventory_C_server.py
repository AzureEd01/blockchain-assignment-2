import hashlib

inventoryC_id = 128
randomC = 831
tC = ''
sC = ''
node_name = 'C'

def inv_C_key_req():
    return inventoryC_id  

def get_privkey_C():
    from pkg_server import get_priv_key
    gC = get_priv_key('C')
    return gC

def calc_tC():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tC = pow(randomC, pkg_e, pkg_n)
    return tC 

def c_calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def c_calc_partial_sig(m, t, gJ):
    randomJ = randomC
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    m = str(t) + m
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)
    rJ_exp = pow(randomJ, decimal_m, pkg_n)
    sJ = (gJ * rJ_exp) % pkg_n
    return sJ

def c_calc_multisig(sA, sB, sC, sD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    s = (sA * sB * sC * sD) % pkg_n
    return s 

def inventory_C_search(record_id):
     global sC
     with open('C_inventory_db.txt') as f:
        lines = f.readlines()
        for row in lines:
            if row.find(record_id) != -1:
                print(row.split(','))
                split_row = row.split(',')
                qty = split_row[1]
                return qty

def pbft_vote_on_primary(data):
    from pkg_server import get_pkg_n, get_priv_key
    import hashlib

    qty = str(data['qty'])
    t = int(data['agg_t'])
    sC_from_proposal = int(data['sC'])

    gC = get_priv_key('C')
    rC = randomC
    pkg_n = get_pkg_n()

    m = str(t) + qty
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)

    r_exp = pow(rC, decimal_m, pkg_n)
    expected_sC = (gC * r_exp) % pkg_n

    print(f"[Node C] Expected signature: {expected_sC}")
    print(f"[Node C] Received signature from proposal: {sC_from_proposal}")

    return expected_sC == sC_from_proposal


