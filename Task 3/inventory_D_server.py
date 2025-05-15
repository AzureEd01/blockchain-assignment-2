inventoryD_id = 129

def inv_D_key_req():
    return inventoryD_id    

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
                return item_qty
        if not item_qty:
            print("Item doesnt exist.")
            return "not found"