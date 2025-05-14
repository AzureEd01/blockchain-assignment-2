import json
import os

INVENTORY_FILE = "inventory.txt"
AUTHORIZED_USERS = {"admin001", "manager002", "auditor003"}
CLONES = ["Inventory1", "Inventory2", "Inventory3", "Inventory4"]

# Initial shared inventory data
initial_inventory = [
    {"ItemID": "001", "ItemQTY": 32, "ItemPrice": 12, "Location": "D"},
    {"ItemID": "002", "ItemQTY": 20, "ItemPrice": 14, "Location": "C"},
    {"ItemID": "003", "ItemQTY": 22, "ItemPrice": 16, "Location": "B"},
    {"ItemID": "004", "ItemQTY": 12, "ItemPrice": 18, "Location": "A"},
]

def initialize_inventory():
    data = {clone: initial_inventory.copy() for clone in CLONES}
    save_inventory(data)
    return data

def load_inventory() -> dict:
    if not os.path.exists(INVENTORY_FILE):
        return initialize_inventory()
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(inventory: dict):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=2)

def add_item(item_id: str, item_qty: int, item_price: int, location: str, authority_id: str):
    if authority_id not in AUTHORIZED_USERS:
        raise PermissionError("You are not authorized to add items.")

    inventory_data = load_inventory()
    base_inventory = inventory_data["Inventory1"]

    if any(item["ItemID"] == item_id for item in base_inventory):
        raise ValueError(f"ItemID '{item_id}' already exists.")

    new_item = {
        "ItemID": item_id,
        "ItemQTY": item_qty,
        "ItemPrice": item_price,
        "Location": location
    }

    updated_inventory = base_inventory + [new_item]

    # Propagate to all clones
    for clone in CLONES:
        inventory_data[clone] = updated_inventory.copy()

    save_inventory(inventory_data)

    print(f"\n✅ Authority '{authority_id}' verified.")
    print(f"📦 New item added: {new_item}")
    print(f"🔁 All {len(CLONES)} inventories updated.")

def main():
    print("=== Inventory Management ===")
    try:
        item_id = input("Enter ItemID: ").strip()
        item_qty = int(input("Enter ItemQTY: "))
        item_price = int(input("Enter ItemPrice: "))
        location = input("Enter Location: ").stripx()
        authority_id = input("Enter Authority ID: ").strip()

        add_item(item_id, item_qty, item_price, location, authority_id)

    except ValueError as ve:
        print(f"❌ Input Error: {ve}")
    except PermissionError as pe:
        print(f"🚫 Authorization Error: {pe}")
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")

if __name__ == "__main__":
    main()
