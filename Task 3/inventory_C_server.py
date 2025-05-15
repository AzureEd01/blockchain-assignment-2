inventoryC_id = 128
randomC = 821
tC = ''


def inv_C_key_req():
    return inventoryC_id  

def calc_tC():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tC = pow(randomC, pkg_e, pkg_n)
    return tC

def calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def inventory_C_search(record_id):
     with open('C_inventory_db.txt') as f:
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
                tC = calc_tC()
                print("Inv C: tC is ", tC)
                #get the other ts 
                #Get tA
                from inventory_A_server import calc_tA
                tA = calc_tA()
                print("Inv C: Inv tA is: ", tA)

                #Get tB
                from inventory_B_server import calc_tB
                tB = calc_tB()
                print("Inv C: Inv tB is: ", tB)

                #Get tD
                from inventory_D_server import calc_tD
                tD = calc_tD()
                print("Inv C: Inv tD is: ", tD)

                #Calculate aggregated t
                t = calc_aggregated_t(tA, tB, tC, tD)
                print("Inv C: Aggregated t= ", t)