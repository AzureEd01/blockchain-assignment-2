from inventory_A_server import inventory_A_search
from inventory_B_server import inventory_B_search
from inventory_C_server import inventory_C_search
from inventory_D_server import inventory_D_search

def pkg_search_qty(record_id):
    # send the request to the inventory servers
    #str_id = 
    qty_A = inventory_A_search(record_id)
    qty_B = inventory_B_search(record_id)
    qty_C = inventory_C_search(record_id)
    qty_D = inventory_D_search(record_id)


    return 'YUP'
