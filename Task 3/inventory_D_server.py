import hashlib

inventoryD_id = 129
randomD = 941
tD = ''
sD = ''
node_name = 'D'

def inv_D_key_req():
    return inventoryD_id  

def get_privkey_D():
    from pkg_server import get_priv_key
    gD = get_priv_key('D')
    return gD

def calc_tD():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tD = pow(randomD, pkg_e, pkg_n)
    return tD 

def d_calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def d_calc_partial_sig(m, t, gJ):
    randomJ = randomD
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    m = str(t) + m
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)
    rJ_exp = pow(randomJ, decimal_m, pkg_n)
    sJ = (gJ * rJ_exp) % pkg_n
    return sJ

def d_calc_multisig(sA, sB, sC, sD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    s = (sA * sB * sC * sD) % pkg_n
    return s 

def inventory_D_search(record_id):
     global sD
     with open('D_inventory_db.txt') as f:
        lines = f.readlines()
        for row in lines:
            if row.find(record_id) != -1:
                print(row.split(','))
                split_row = row.split(',')
                qty = split_row[1]
                return qty

# Consensus
def pbft_vote_on_primary(data):
    from pkg_server import get_pkg_n, get_priv_key
    import hashlib

    qty = str(data['qty'])
    t = int(data['agg_t'])
    sD_from_proposal = int(data['sD'])

    gD = get_priv_key('D')
    rD = randomD
    pkg_n = get_pkg_n()

    m = str(t) + qty
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)

    r_exp = pow(rD, decimal_m, pkg_n)
    expected_sD = (gD * r_exp) % pkg_n

    print(f"[Node D] Expected signature: {expected_sD}")
    print(f"[Node D] Received signature from proposal: {sD_from_proposal}")

    return expected_sD == sD_from_proposal
