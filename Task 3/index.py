#libraries
import hashlib

# ==========================================================================================================================
# Signature
# ==========================================================================================================================

# pkg
pkg_p = 1004162036461488639338597000466705179253226703
pkg_q = 950133741151267522116252385927940618264103623
pkg_e = 973028207197278907211

# # procurement officer
# No idea where to use this
# p = 1080954735722463992988394149602856332100628417
# q = 1158106283320086444890911863299879973542293243
# e = 106506253943651610547613

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

# THE T
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
inventoryA = "0013212D"
inventoryB = "0022014C"
inventoryC = "0032216B"
inventoryD = "0041218A"

# Need to adapt, will do later.
# # Initial shared inventory data
# initial_inventory = [
#     {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
#     {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
#     {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
#     {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
# ]

# # Each node starts with the same inventory
# inventories = {
#     "Node1": initial_inventory.copy(),
#     "Node2": initial_inventory.copy(),
#     "Node3": initial_inventory.copy(),
#     "Node4": initial_inventory.copy()
# }

# Inventory A needs to be replaced with an input selection. will do later
m = str(t) + inventoryA
print(m)

hash_m = hashlib.md5(m.encode()).hexdigest()
print("MD5:", hash_m)

decimal_m = int(hash_m, 16)
print("Decimal Value:", decimal_m)

# No idea if i accidentally did ur part
# Inventory A Signatures
s1 = gA * randomA
s1 = pow(s1, decimal_m, pkg_n) % pkg_n
print("Signer A:", s1)

s2 = gB * randomB
s2 = pow(s2, decimal_m, pkg_n) % pkg_n
print("Signer B:", s2)

s3 = gC * randomC
s3 = pow(s3, decimal_m, pkg_n) % pkg_n
print("Signer C:", s3)

s4 = gD * randomD
s4 = pow(s4, decimal_m, pkg_n) % pkg_n
print("Signer D:", s4)

# Completing the Multi-signature component
s = (s1 * s2 * s3 * s4) % pkg_n
print("Signature: ", s)
# Signature is s = (t, s)
print("Final Signature:", s, ",", t)

# ==========================================================================================================================
# Verification
# ==========================================================================================================================
import tkinter as tk
#create a widget (named m for master)
m= tk.Tk()
record_var = tk.StringVar()

#function for submit button
def submit():
    record_id = record_var.get()
    print(record_id)
    
    #inv A search 
    # string to search in file
    # with open(r'A_inventory_db.txt', 'r') as fp:
    #     # read all lines using readline()
    #     lines = fp.readlines()
    #     for row in lines:
    #         # check if string present on a current line
    #         word = record_id
    #         #print(row.find(word))
    #         # find() method returns -1 if the value is not found,
    #         # if found it returns index of the first occurrence of the substring
    #         if row.find(word) != -1:
    #             print('string exists in file')
    #             print('line Number:', lines.index(row))


    #f is now the file object 
    f = open("A_inventory_db.txt")
    print(f.read())

    #inv B search 

    #inv C search 

    #inv D search 



#UI
#prompt to ask for an ID to search for 
tk.Label(m, text='Item ID: ').grid(row=0)
#inputbox
tk.Entry(m, textvariable = record_var).grid(row=0, column= 1)
#enter button
entBtn = tk.Button(m, text='Enter', command = submit).grid(row=2, column= 0)

m.mainloop()