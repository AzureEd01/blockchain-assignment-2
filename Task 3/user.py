import hashlib
from inventory_A_server import inv_A_key_req
from inventory_B_server import inv_B_key_req
from inventory_C_server import inv_C_key_req
from inventory_D_server import inv_D_key_req
from pkg_server import pkg_n
from pkg_server import pkg_e

# # procurement officer
# Use this for rsa
proc_off_p = 1080954735722463992988394149602856332100628417
proc_off_q = 1158106283320086444890911863299879973542293243
proc_off_e = 106506253943651610547613

proc_off_n = proc_off_p * proc_off_q

#validation stuff for later 
def proc_validate_message(s):
    #compute: s ^ e mod n 
    result = pow(s, proc_off_e, proc_off_n)
    return result

def proc_validate_second(m, t):
    #get the each servers id 
    A_id = inv_A_key_req()
    B_id = inv_B_key_req()
    C_id = inv_C_key_req()
    D_id = inv_D_key_req()
    #append message to t
    m = str(t) + str(m)
    #hash message
    hash_m = hashlib.md5(m.encode()).hexdigest()
    #convert message to int 
    decimal_m = int(hash_m, 16)
    #using the PKG public key compute: (i_1 * i_2 * i_3) * t ^ Hash(t, m) mod n
    new_t = pow(int(t), decimal_m, pkg_n)
    result_2 = A_id * B_id * C_id * D_id * new_t % pkg_n
    return result_2

