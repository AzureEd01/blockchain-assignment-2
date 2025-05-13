#key generation function    
def calc_n(p,q):
    n=p*q
    return n

def calc_phin(p, q):
    phin = (p-1)*(q-1)
    return phin
    

def calc_d(phin, e):
    #calc modular inverse (e^-1 mod phi(n))
    d = pow(e, -1, phin)
    return d
    
#Key pairs
#Inventory A
inv_a_p = 1210613765735147311106936311866593978079938707
inv_a_q = 1247842850282035753615951347964437248190231863
inv_a_e = 815459040813953176289801
#calculate n
inv_a_n = calc_n(inv_a_p, inv_a_q)
#calculate phi(n)
inv_a_phin = calc_phin(inv_a_p, inv_a_q)
#calculate d 
inv_a_d = calc_d(inv_a_phin, inv_a_e)

#storing the public key
a_pub_key = {'n': inv_a_n, 'e': inv_a_e}
#storing the private key
a_priv_key = {'n': inv_a_n, 'd': inv_a_d}


#Inventory B
inv_b_p = 787435686772982288169641922308628444877260947
inv_b_q = 1325305233886096053310340418467385397239375379
inv_b_e = 692450682143089563609787
#calculate n
inv_b_n = calc_n(inv_b_p, inv_b_q)
#calculate phi(n)
inv_b_phin = calc_phin(inv_b_p, inv_b_q)
#calculate d 
inv_b_d = calc_d(inv_b_phin, inv_b_e)

#storing the public key
b_pub_key = {'n': inv_b_n, 'e': inv_b_e}
#storing the private key
b_priv_key = {'n': inv_b_n, 'd': inv_b_d}

#Inventory C
inv_c_p = 1014247300991039444864201518275018240361205111
inv_c_q = 904030450302158058469475048755214591704639633
inv_c_e = 1158749422015035388438057
#calculate n
inv_c_n = calc_n(inv_c_p, inv_c_q)
#calculate phi(n)
inv_c_phin = calc_phin(inv_c_p, inv_c_q)
#calculate d 
inv_c_d = calc_d(inv_c_phin, inv_c_e)

#storing the public key
c_pub_key = {'n': inv_c_n, 'e': inv_c_e}
#storing the private key
c_priv_key = {'n': inv_c_n, 'd': inv_c_d}


#Inventory D
inv_d_p = 1287737200891425621338551020762858710281638317
inv_d_q = 1330909125725073469794953234151525201084537607
inv_d_e = 33981230465225879849295979
#calculate n
inv_d_n = calc_n(inv_d_p, inv_d_q)
#calculate phi(n)
inv_d_phin = calc_phin(inv_d_p, inv_d_q)
#calculate d 
inv_d_d = calc_d(inv_d_phin, inv_d_e)

#storing the public key
d_pub_key = {'n': inv_d_n, 'e': inv_d_e}
#storing the private key
d_priv_key = {'n': inv_d_n, 'd': inv_d_d}


#This stores all of the keypairs in one dictionary 
stored_key_pairs = {
    'inv_a_pub_key': a_pub_key,
    'inv_a_priv_key': a_priv_key,
    'inv_b_pub_key': b_pub_key,
    'inv_b_priv_key': b_priv_key,
    'inv_c_pub_key': c_pub_key,
    'inv_c_priv_key': c_priv_key,
    'inv_d_pub_key': d_pub_key,
    'inv_d_priv_key': d_priv_key,
}

