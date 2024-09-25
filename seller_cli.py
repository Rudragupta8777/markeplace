import firebase_admin
from firebase_admin import credentials, firestore

# Embed your Firebase credentials directly in the code
firebase_credentials = 

# Initialize Firebase
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_or_update_approved_buyer():
    name = input("Enter the buyer's name: ")
    try:
        balance = float(input("Enter the buyer's balance: "))
    except ValueError:
        print("Invalid balance. Please enter a numeric value.")
        return
    
    # Update or add buyer data in Firestore
    update_or_add_buyer(name, balance)
    print(f"Buyer '{name}' updated with balance ${balance}.")

def update_or_add_buyer(name, balance):
    buyer_ref = db.collection('approved_buyers').document(name)
    buyer_ref.set({'balance': balance}, merge=True)

def list_item():
    item_name = input("Enter item name: ")
    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
    except ValueError:
        print("Invalid quantity or price. Please enter numeric values.")
        return

    item_ref = db.collection('items').document(item_name)
    item_ref.set({'quantity': quantity, 'price': price}, merge=True)
    print(f"Item '{item_name}' listed with {quantity} units at ${price} each.")

def view_items():
    items = db.collection('items').stream()
    if not items:
        print("No items listed.")
    else:
        print("Items available:")
        for item in items:
            item_data = item.to_dict()
            print(f"{item.id}: {item_data['quantity']} available at ${item_data['price']} each.")

def update_quantity():
    item_name = input("Enter item name: ")
    try:
        quantity = int(input("Enter new quantity: "))
    except ValueError:
        print("Invalid quantity. Please enter a numeric value.")
        return

    item_ref = db.collection('items').document(item_name)
    item_ref.update({'quantity': quantity})
    print(f"Updated '{item_name}' to {quantity} units.")

def view_buyers():
    buyers = db.collection('approved_buyers').stream()
    if not buyers:
        print("No approved buyers found.")
        return

    print("Approved buyers:")
    for buyer in buyers:
        buyer_data = buyer.to_dict()
        balance = buyer_data.get('balance', 'N/A')
        print(f"{buyer.id}: Balance ${balance}.")

def main():
    while True:
        print("\nSeller CLI")
        print("1. Add/Update Approved Buyer")
        print("2. List Item")
        print("3. View Items")
        print("4. Update Quantity")
        print("5. View Approved Buyers")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_or_update_approved_buyer()
        elif choice == '2':
            list_item()
        elif choice == '3':
            view_items()
        elif choice == '4':
            update_quantity()
        elif choice == '5':
            view_buyers()
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()