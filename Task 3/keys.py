import hashlib

#This stores all of the keypairs in one dictionary 

# pkg------------------------------------------------------------
pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

print("PKG calculation:")
# compute pkg n
pkg_n = pkg_p * pkg_q

# compute pkg phi(n)
pkg_phi_n = (pkg_p - 1) * (pkg_q - 1)

# pkg private key
pkg_d = pow(pkg_e, -1, pkg_phi_n)

#inventory ---------------------------------------------------------
# Identity for inventories
inventoryA_id = 126
inventoryB_id = 127
inventoryC_id = 128
inventoryD_id = 129

# Secret Key of A
gA = pow(inventoryA_id, pkg_d, pkg_n)
print("Inventory A: ", gA)

# Secret Key of B
gB = pow(inventoryB_id, pkg_d, pkg_n) 
print("Inventory B: ",gB)

# Secret Key of C
gC = pow(inventoryC_id, pkg_d, pkg_n) 
print("Inventory C: ",gC)

# Secret Key of D
gD = pow(inventoryD_id, pkg_d, pkg_n) 
print("Inventory D: ",gD)

# Random Interger Calculation
print()
print("Random Interger rj:")

# Random Value for Inventories
randomA = 621
randomB = 721
randomC = 821
randomD = 921

# Random Interger Signing
# Inventory A Signature
tA = pow(randomA, pkg_e, pkg_n)
print("Inventory A Signature: ", tA)

# Inventory B Signature
tB = pow(randomB, pkg_e, pkg_n)
print("Inventory B Signature: ", tB)

# Inventory C Signature
tC = pow(randomC, pkg_e, pkg_n)
print("Inventory C Signature: ", tC)

# Inventory D Signature
tD = pow(randomD, pkg_e, pkg_n) 
print("Inventory D Signature: ", tD)

# Aggregated t
t = (tA * tB * tC * tD) % pkg_n
print("Aggregated t: ", t)
#----------------------------------------------------------------


def gen_partial_sig(inv_name, m):
    hash_m = hashlib.md5(m.encode()).hexdigest()
    decimal_m = int(hash_m, 16)
    m = str(t) + m
    #Each signer also computes sj = gj*rj^H(t,m) mod n , this is then shared with eachother
    if inv_name == 'A':
        s1 = gA * randomA
        s1 = pow(s1, decimal_m, pkg_n)
        print("Signer A:", s1)
        return s1
    elif inv_name == 'B':
        s2 = gB * randomB
        s2 = pow(s2, decimal_m, pkg_n)
        print("Signer B:", s2)
        return s2
    elif inv_name == 'C':
        s3 = gC * randomC
        s3 = pow(s3, decimal_m, pkg_n)
        print("Signer C:", s3)
        return s3
    elif inv_name == 'D':
        s4 = gD * randomD
        s4 = pow(s4, decimal_m, pkg_n)
        print("Signer D:", s4)
        return s4

def gen_multi_sig(s1, s2, s3, s4):
    # Completing the Multi-signature component
    s = (s1 * s2 * s3 * s4) % pkg_n
    print("Signature: ", s)
    # Signature is s = (t, s)
    print("Final Signature:", s, ",", t)