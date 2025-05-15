inventoryB_id = 127
randomB = 721
tB = ''


def inv_B_key_req():
    return inventoryB_id  

def calc_tB():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tB = pow(randomB, pkg_e, pkg_n)
    return tB 

def calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def inventory_B_search(record_id):
     with open('B_inventory_db.txt') as f:
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
                tB = calc_tB()
                print("INV B: tB is ", tB)

                #get the other ts 
                #Get tA
                from inventory_A_server import calc_tA
                tA = calc_tA()
                print("Inv B: Inv tA is: ", tA)

                #Get tC
                from inventory_C_server import calc_tC
                tC = calc_tC()
                print("Inv B: Inv tC is: ", tC)

                #Get tD
                from inventory_D_server import calc_tD
                tD = calc_tD()
                print("Inv B: Inv tD is: ", tD)

                #Calculate aggregated t
                t = calc_aggregated_t(tA, tB, tC, tD)
                print("Inv B: Aggregated t= ", t)
