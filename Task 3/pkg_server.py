#Imports -------------------------------------------------
from inventory_A_server import inventory_A_search
from inventory_A_server import inv_A_key_req

from inventory_B_server import inventory_B_search
from inventory_B_server import inv_B_key_req

from inventory_C_server import inventory_C_search
from inventory_C_server import inv_C_key_req

from inventory_D_server import inventory_D_search
from inventory_D_server import inv_D_key_req
#----------------------------------------------------------
#PKG key --------------------------------------------------
pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

# compute pkg n
pkg_n = pkg_p * pkg_q

# compute pkg phi(n)
pkg_phi_n = (pkg_p - 1) * (pkg_q - 1)

# pkg private key
pkg_d = pow(pkg_e, -1, pkg_phi_n)
#-------------------------------------------------------------
def get_pkg_e():
    return pkg_e

def get_pkg_n():
    return pkg_n

def keysign(id):
    gJ = pow(id, pkg_d, pkg_n)
    return gJ

def send_privkey(inv_name, privkey):
    filename = inv_name + "_privatekey.txt"
    with open(filename, 'r+') as f:
        #clear the file being opened
        f.truncate()
        #write the key into the file
        f.write(str(privkey))

def keygen():
    #get the each servers id 
    A_id = inv_A_key_req()
    B_id = inv_B_key_req()
    C_id = inv_C_key_req()
    D_id = inv_D_key_req()
    print("PKG: IDs recieved")

    #pkg signs the IDs 
    A_priv = keysign(A_id)
    B_priv = keysign(B_id)
    C_priv = keysign(C_id)
    D_priv = keysign(D_id)
    print("PKG: Private keys made- ID has been signed")

    #send the priv keys to the inventories 
    send_privkey('A', A_priv)
    send_privkey('B', B_priv)
    send_privkey('C', C_priv)
    send_privkey('D', D_priv)
    print("PKG: Private keys have been sent")


def pkg_search_qty(record_id):
    # send the request to the inventory servers
    #str_id = 
    qty_A = inventory_A_search(record_id)
    qty_B = inventory_B_search(record_id)
    qty_C = inventory_C_search(record_id)
    qty_D = inventory_D_search(record_id)
