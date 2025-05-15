import hashlib
#The imports are done within the functions to avoid circular import issue
#Variables----------------------------------
inventoryA_id = 126
randomA = 621
tA = ''
sA = ''
#-------------------------------------------
#function to send the 
def inv_A_key_req():
    return inventoryA_id 

def inv_A_psig_req():
    return sA

def calc_tA():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tA = pow(randomA, pkg_e, pkg_n)
    return tA

def a_calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % int(pkg_n)
    return t

def calc_partial_sig(m, t, gJ):
    #get random number 
    randomJ = randomA
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

def a_calc_multisig(sA, sB, sC, sD):
    #get pkg n
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    #calc
    s = (sA * sB * sC * sD) % pkg_n
    return s 

def get_privkey_A():
    from pkg_server import get_priv_key
    gA = get_priv_key('A')
    return gA

def inventory_A_search(record_id):
     global sA
     with open('A_inventory_db.txt') as f:
        lines = f.readlines()
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
