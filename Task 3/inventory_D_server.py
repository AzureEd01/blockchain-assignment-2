import hashlib

inventoryD_id = 129
randomD = 921
tD = ''

def inv_D_key_req():
    return inventoryD_id  

def get_privkey_D():
    from pkg_server import get_priv_key
    gD = get_priv_key('D')
    return gD

def calc_tD():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
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
    #get random number 
    randomJ = randomD
    #get pkg n
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    #append message to t
    m = str(t) + m
    #hash message
    hash_m = hashlib.md5(m.encode()).hexdigest()
    #convert message to int 
    decimal_m = int(hash_m, 16)
    #Each signer also computes sj = gj*rj^H(t,m) mod n , this is then shared with eachother
    # sJ = gJ * randomJ
    # sJ = pow(sJ, decimal_m, pkg_n)
    rJ_exp = pow(randomJ, decimal_m, pkg_n)
    sJ = (gJ * rJ_exp) % pkg_n
    return sJ

def d_calc_multisig(sA, sB, sC, sD):
    #get pkg n
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    #calc
    s = (sA * sB * sC * sD) % pkg_n
    return s 

def inventory_D_search(record_id):
     with open('D_inventory_db.txt') as f:
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
                return qty