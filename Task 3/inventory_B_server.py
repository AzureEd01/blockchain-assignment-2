import hashlib

inventoryB_id = 127
randomB = 721
tB = ''
sB = ''

def inv_B_key_req():
    return inventoryB_id  

def inv_B_psig_req():
    return sB

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

# def calc_aggregated_t(tA, tB, tC, tD):
#     from pkg_server import get_pkg_n
#     pkg_n = get_pkg_n()
#     t = (tA * tB * tC * tD) % pkg_n
#     return t

def calc_partial_sig(m, t, gJ):
    #get random number 
    randomJ = randomB
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

# def calc_multisig(sA, sB, sC, sD):
#     #get pkg n
#     from pkg_server import get_pkg_n
#     pkg_n = get_pkg_n()
#     #calc
#     s = (sA * sB * sC * sD) % pkg_n
#     return s 

def inventory_B_search(record_id):
     global sB
     with open('B_inventory_db.txt') as f:
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

