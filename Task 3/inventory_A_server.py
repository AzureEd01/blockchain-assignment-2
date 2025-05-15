#imports ------------------------------------
from pkg_server import get_pkg_e 
from pkg_server import get_pkg_n 

#Variables----------------------------------
inventoryA_id = 126
randomA = 621
#-------------------------------------------

def inv_A_key_req():
    return inventoryA_id 

def calc_t():
    #Get the pkg e (part of public key)
    pkg_e = get_pkg_e()
    pkg_n = get_pkg_n()
    tA = pow(randomA, pkg_e, pkg_n)
    return tA


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
                tA = calc_t(qty)
                #exchange t 
        