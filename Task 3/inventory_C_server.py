import hashlib

inventoryC_id = 128
randomC = 821
tC = ''

def inv_C_key_req():
    return inventoryC_id  

def inv_C_psig_req():
    return calc_partial_sig

def get_privkey_C():
    from pkg_server import get_priv_key
    gC = get_priv_key('C')
    return gC

def calc_tC():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tC = pow(randomC, pkg_e, pkg_n)
    return tC

def c_calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def calc_partial_sig(m, t, gJ):
    #get random number 
    randomJ = randomC
    #get pkg n
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    #hash message
    hash_m = hashlib.md5(m.encode()).hexdigest()
    #convert message to int 
    decimal_m = int(hash_m, 16)
    #append message to t
    m = str(t) + m
    #Each signer also computes sj = gj*rj^H(t,m) mod n , this is then shared with eachother
    sJ = gJ * randomJ
    sJ = pow(sJ, decimal_m, pkg_n)
    return sJ

def c_calc_multisig(sA, sB, sC, sD):
    #get pkg n
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    #calc
    s = (sA * sB * sC * sD) % pkg_n
    return s 

def inventory_C_search(record_id):
     with open('C_inventory_db.txt') as f:
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