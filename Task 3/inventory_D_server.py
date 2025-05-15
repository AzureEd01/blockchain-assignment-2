inventoryD_id = 129
randomD = 921
tD = ''


def inv_D_key_req():
    return inventoryD_id  

def calc_tD():
    from pkg_server import get_pkg_e
    from pkg_server import get_pkg_n
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tD = pow(randomD, pkg_e, pkg_n)
    return tD 

def calc_aggregated_t(tA, tB, tC, tD):
    from pkg_server import get_pkg_n
    pkg_n = get_pkg_n()
    t = (tA * tB * tC * tD) % pkg_n
    return t

def inventory_D_search(record_id):
     with open('D_inventory_db.txt') as f:
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
                tD = calc_tD()
                print("Inv D: tD is ", tD)

                #get the other ts 
                #Get tA
                from inventory_A_server import calc_tA
                tA = calc_tA()
                print("Inv D: Inv tA is: ", tA)

                #Get tB
                from inventory_B_server import calc_tB
                tB = calc_tB()
                print("Inv D: Inv tB is: ", tB)

                #Get tC
                from inventory_C_server import calc_tC
                tC = calc_tC()
                print("Inv D: Inv tC is: ", tC)

                #Calculate aggregated t
                t = calc_aggregated_t(tA, tB, tC, tD)
                print("Inv D: Aggregated t= ", t)