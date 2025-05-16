#Imports -------------------------------------------------
from inventory_A_server import inv_A_key_req
from inventory_B_server import inv_B_key_req
from inventory_C_server import inv_C_key_req
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
#functions----------------------------------------------------
#sends the pkgs e value 
def get_pkg_e():
    return pkg_e

#sends the pkgs n value 
def get_pkg_n():
    return pkg_n

#create private key dictionary variable
private_keys = {}

#sends the private key to the corresponding inventory 
def get_priv_key(inv_name):
    priv_key = private_keys[inv_name]
    return priv_key

#signs the inventories id to create a private key
def keysign(id):
    print("Priv key calcs: ")
    print("id: ", id)
    print("pkg_d: ", pkg_d)
    print("pkg_n: ", pkg_n)
    gJ = pow(id, pkg_d, pkg_n)
    return gJ

#creates a list of each servers' private key 
def keygen():
    global private_keys
    #get the each servers id 
    A_id = inv_A_key_req()
    B_id = inv_B_key_req()
    C_id = inv_C_key_req()
    D_id = inv_D_key_req()
    print("PKG: IDs recieved")
    #pkg signs the IDs & stored in dictionary 
    private_keys = {
        'A' : keysign(A_id),
        'B' : keysign(B_id),
        'C' : keysign(C_id),
        'D' : keysign(D_id)
    }
    return private_keys

#encrypts the signature to send to the procurement officer
def pkg_encrypt(s):
    # import the officers public key 
    from user import proc_off_e
    from user import proc_off_n
    #calc encryption
    enc = pow(s, proc_off_e, proc_off_n)
    return enc


    
