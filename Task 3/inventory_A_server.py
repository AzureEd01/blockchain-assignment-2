#The imports are done within the functions to avoid circular import issue
#Variables----------------------------------
inventoryA_id = 126
randomA = 621
tA = ''
#-------------------------------------------
#function to send the 
def inv_A_key_req():
    return inventoryA_id 

# def tA_req():
#     return tA

def calc_tA():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tA = pow(randomA, pkg_e, pkg_n)
    return tA

# def send_tJ(inv_name, tJ):
#     filename = inv_name + "_storage.txt"
#     with open(filename, 'r+') as f:
#         #write the key into the file
#         f.write('tA: ' + str(tJ))

def calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % int(pkg_n)
    return t

def inventory_A_search(record_id):
     with open('A_inventory_db.txt') as f:
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
                item_qty = qty
                #calculate t for signing 
                tA = calc_tA()
                print("INV A: tA is ", tA)

                #Get the other ts 
                #Get tB
                from inventory_B_server import calc_tB
                tB = calc_tB()
                print("Inv A: Inv tB is: ", tB)

                #Get tC
                from inventory_C_server import calc_tC
                tC = calc_tC()
                print("Inv A: Inv tC is: ", tC)

                #Get tD
                from inventory_D_server import calc_tD
                tD = calc_tD()
                print("Inv A: Inv tD is: ", tD)

                #Calculate aggregated t
                t = calc_aggregated_t(tA, tB, tC, tD)
                print("Inv A: Aggregated t= ", t)

