#libraries
import hashlib
import json
# ==========================================================================================================================
# Signature
# ==========================================================================================================================

# pkg
pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

# # procurement officer
# No idea where to use this
p = 1080954735722463992988394149602856332100628417
q = 1158106283320086444890911863299879973542293243
e = 106506253943651610547613

print("PKG calculation:")
# compute pkg n
pkg_n = pkg_p * pkg_q
print("pkg n = ", pkg_n)

# compute pkg phi(n)
pkg_phi_n = (pkg_p - 1) * (pkg_q - 1)
print("pkg phi(n) = ", pkg_phi_n)

# # pkg public key
# print("pkg public key(",pkg_e, pkg_phi_n,")")

# pkg private key
pkg_d = pow(pkg_e, -1, pkg_phi_n) % pkg_phi_n
print("pkg private key(",pkg_d, pkg_n,")")

# Inventory Calculation
print()
print("Inventory Calculation:")

# Identity for inventories
inventoryA_id = 126
inventoryB_id = 127
inventoryC_id = 128
inventoryD_id = 129

# Secret Key of A
gA = pow(inventoryA_id, pkg_d, pkg_n) % pkg_n
print("Inventory A: ", gA)

# Secret Key of B
gB = pow(inventoryB_id, pkg_d, pkg_n) % pkg_n
print("Inventory B: ",gB)

# Secret Key of C
gC = pow(inventoryC_id, pkg_d, pkg_n) % pkg_n
print("Inventory C: ",gC)

# Secret Key of D
gD = pow(inventoryD_id, pkg_d, pkg_n) % pkg_n
print("Inventory D: ",gD)

# Random Interger Calculation
print()
print("Random Interger rj:")

# Random Value of Inventories
randomA = 621
randomB = 721
randomC = 821
randomD = 921

# Random Interger Signing
# Inventory A Signature
tA = pow(randomA, pkg_e, pkg_n) % pkg_n
print("Inventory A Signature: ", tA)

# Inventory B Signature
tB = pow(randomB, pkg_e, pkg_n) % pkg_n
print("Inventory B Signature: ", tB)

# Inventory C Signature
tC = pow(randomC, pkg_e, pkg_n) % pkg_n
print("Inventory C Signature: ", tC)

# Inventory D Signature
tD = pow(randomD, pkg_e, pkg_n) % pkg_n
print("Inventory D Signature: ", tD)

# Aggregated t
t = (tA * tB * tC * tD) % pkg_n
print("Aggregated t: ", t)

# Appending the Message
# This needs to be changed to be a user input that searches through an inventory node
print()
print("Appending the Message:")


# Load inventory data from a .txt file
with open('inventory.txt', 'r') as file:
    inventory_data = json.load(file)

def item_exists(item_id, data):
    for inventory in data.values():
        for item in inventory:
            if item['ItemID'] == item_id:
                return True
    return False

# Ask for input and check if item exists
while True:
    msg = input("Enter ItemID: ").strip()
    if item_exists(msg, inventory_data):
        print(f"ItemID {msg} found. Continuing...")
        break  # Exit loop if found
    else:
        print(f"ItemID {msg} not found. Please try again.")

# Inventory A needs to be replaced with an input selection. will do later
m = str(t) + msg
print(m)

hash_m = hashlib.md5(m.encode()).hexdigest()
print("MD5:", hash_m)

decimal_m = int(hash_m, 16)
print("Decimal Value:", decimal_m)

# No idea if i accidentally did ur par1t
# Inventory A Signatures
s1 = gA * randomA
s1 = pow(s1, decimal_m, pkg_n) % pkg_n
print("Signer A:", s1)

# Inventory B Signatures
s2 = gB * randomB
s2 = pow(s2, decimal_m, pkg_n) % pkg_n
print("Signer B:", s2)

# Inventory C Signatures
s3 = gC * randomC
s3 = pow(s3, decimal_m, pkg_n) % pkg_n
print("Signer C:", s3)

# Inventory D Signatures
s4 = gD * randomD
s4 = pow(s4, decimal_m, pkg_n) % pkg_n
print("Signer D:", s4)

# Completing the Multi-signature component
s = (s1 * s2 * s3 * s4) % pkg_n
print("Signature: ", s)
# Signature is s = (t, s)
print("Final Signature:", t, ",", s)
print("Sending to user: ", msg, ",", s, ",", t)


# ==========================================================================================================================
# Verification
# ==========================================================================================================================


n = p * q
temp = t % n
print("temp: ", temp)

#compute individual
result = pow(s, e, n)
print("power1: ", power1)

result = (temp * power1) % n
print("result: ", result)

result2 = (t * pow(s, e, n)) % n
print("result2: ", result2)


