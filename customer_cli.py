import firebase_admin
from firebase_admin import credentials, firestore

# Embed your Firebase credentials directly in the code
firebase_credentials = 

# Initialize Firebase
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

def verify_customer(name):
    customer_ref = db.collection('approved_buyers').document(name)
    doc = customer_ref.get()
    if doc.exists:
        balance = doc.to_dict().get('balance', 0)
        print(f"Customer '{name}' verified. Balance: ${balance}.")
        return balance
    else:
        print(f"Customer '{name}' not found.")
        return None

def view_items():
    items = db.collection('items').stream()
    if not items:
        print("No items available.")
    else:
        print("Items available:")
        for item in items:
            item_data = item.to_dict()
            print(f"{item.id}: {item_data['quantity']} available at ${item_data['price']} each.")

def purchase_item(name):
    item_name = input("Enter item name: ")
    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid quantity. Please enter a numeric value.")
        return

    customer_ref = db.collection('approved_buyers').document(name)
    item_ref = db.collection('items').document(item_name)
    
    customer_doc = customer_ref.get()
    item_doc = item_ref.get()
    
    if not customer_doc.exists:
        print("Customer not found.")
        return
    
    if not item_doc.exists:
        print("Item not found.")
        return

    customer_data = customer_doc.to_dict()
    item_data = item_doc.to_dict()
    
    if item_data['quantity'] < quantity:
        print("Not enough quantity available.")
        return
    
    total_price = item_data['price'] * quantity
    if customer_data['balance'] < total_price:
        print("Insufficient balance.")
        return

    # Update item quantity
    item_ref.update({'quantity': item_data['quantity'] - quantity})
    
    # Update customer balance
    customer_ref.update({'balance': customer_data['balance'] - total_price})
    
    print(f"Purchased {quantity} of '{item_name}' for ${total_price}.")
    print(f"Remaining balance: ${customer_data['balance'] - total_price}.")

def view_purchases(name):
    print("Viewing purchases is not implemented yet.")

def main():
    customer_name = None
    balance = 0

    while True:
        if customer_name is None:
            # Ask for the name and verify it
            name = input("Enter your name: ")
            balance = verify_customer(name)
            if balance is not None:
                customer_name = name
            else:
                print("Invalid customer name. Exiting.")
                break
        else:
            # Show the menu and perform actions
            print("\nCustomer CLI")
            print("1. View Items")
            print("2. Purchase Item")
            print("3. View Purchases")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                view_items()
            elif choice == '2':
                purchase_item(customer_name)
            elif choice == '3':
                view_purchases(customer_name)
            elif choice == '4':
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()