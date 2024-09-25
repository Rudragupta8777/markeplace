import json

# Sample data storage
ITEMS_FILE = 'items.json'
CUSTOMERS_FILE = 'customers.json'

# Utility functions to load and save JSON data
def load_data(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Seller Class to manage inventory
class Seller:
    def __init__(self):
        self.items = load_data(ITEMS_FILE)
    
    def list_item(self, item_name, quantity, price):
        self.items[item_name] = {"quantity": quantity, "price": price}
        save_data(ITEMS_FILE, self.items)
        print(f"Item '{item_name}' listed with {quantity} units at {price} each.")
    
    def view_items(self):
        if not self.items:
            print("No items listed.")
        else:
            print("Items available:")
            for item, details in self.items.items():
                print(f"{item}: {details['quantity']} available at ${details['price']} each.")
    
    def update_quantity(self, item_name, quantity):
        if item_name in self.items:
            self.items[item_name]['quantity'] = quantity
            save_data(ITEMS_FILE, self.items)
            print(f"Updated '{item_name}' to {quantity} units.")
        else:
            print(f"Item '{item_name}' not found.")

# Customer Class to manage purchases
class Customer:
    def __init__(self, name):
        self.name = name
        self.balance = 100  # Starting balance for all customers
        self.purchases = []
        self.items = load_data(ITEMS_FILE)
        self.customers = load_data(CUSTOMERS_FILE)
    
    def view_items(self):
        if not self.items:
            print("No items available.")
        else:
            print("Items available for purchase:")
            for item, details in self.items.items():
                print(f"{item}: {details['quantity']} units available at ${details['price']} each.")
    
    def buy_item(self, item_name, quantity):
        if item_name not in self.items:
            print(f"Item '{item_name}' not available.")
            return
        item = self.items[item_name]
        total_price = item['price'] * quantity
        
        if item['quantity'] < quantity:
            print(f"Not enough '{item_name}' in stock.")
        elif self.balance < total_price:
            print("Insufficient balance.")
        else:
            # Update customer data
            self.balance -= total_price
            self.purchases.append({"item": item_name, "quantity": quantity, "total_price": total_price})
            self.items[item_name]['quantity'] -= quantity
            save_data(ITEMS_FILE, self.items)
            
            # Update in customers data file
            self.customers[self.name] = {"balance": self.balance, "purchases": self.purchases}
            save_data(CUSTOMERS_FILE, self.customers)
            
            print(f"Purchased {quantity} of '{item_name}' for ${total_price}.")
            print(f"Remaining balance: ${self.balance}")
    
    def view_purchases(self):
        print(f"Purchases for {self.name}:")
        if not self.purchases:
            print("No purchases yet.")
        else:
            for purchase in self.purchases:
                print(f"{purchase['item']} - {purchase['quantity']} units for ${purchase['total_price']}")
    
# Main CLI logic
def seller_cli():
    seller = Seller()
    while True:
        print("\n--- Seller Menu ---")
        print("1. List an item")
        print("2. View all items")
        print("3. Update item quantity")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            item = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            seller.list_item(item, quantity, price)
        elif choice == '2':
            seller.view_items()
        elif choice == '3':
            item = input("Enter item name: ")
            quantity = int(input("Enter new quantity: "))
            seller.update_quantity(item, quantity)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def customer_cli():
    name = input("Enter your name: ")
    customer = Customer(name)
    
    while True:
        print("\n--- Customer Menu ---")
        print("1. View items")
        print("2. Buy an item")
        print("3. View my purchases")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            customer.view_items()
        elif choice == '2':
            item = input("Enter item name: ")
            quantity = int(input(f"Enter quantity of '{item}': "))
            customer.buy_item(item, quantity)
        elif choice == '3':
            customer.view_purchases()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

# Main marketplace function
def main():
    while True:
        print("\n--- Marketplace ---")
        print("1. Seller CLI")
        print("2. Customer CLI")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            seller_cli()
        elif choice == '2':
            customer_cli()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
