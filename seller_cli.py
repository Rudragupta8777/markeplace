import firebase_admin
from firebase_admin import credentials, firestore
from colorama import init, Fore, Style

# Embed your Firebase credentials directly in the code
firebase_credentials = {
  "type": "service_account",
  "project_id": "marketplace-bd8d7",
  "private_key_id": "8a135c8c37a65b77fe6d1d97e5b1b16d02658d61",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDKI4zG0OXPHEWW\naQnt/7o4G+d/PFuJoDx4/ee5aiuwhy018dUd5JuwhsRZ8G5+KORKJL2V/tFzvga9\n5cpKQ6AqYnTe7KikYbiyznUs+MoM3ESSE778GzKID3OwTIIs+doAkgAFH2n1GN0h\ntCAmxl5bcEvXUFXftLNgV3qeERiR2q2gVCToUcpWV1NAn4UFdJzjlQSP4YXay0z4\nEGDiG9ylqRCHW5blzGcIxo7IddzJNilVprnGBguo1cBtBjCjl2y1mibhb1RQ8VLw\nnwkTqhKuq5oqwcMqu5lhm/TfsHAExcyD0hYA/BnnLkOGIZ/XYJ0pgoL180FqqoqL\nhL9SqH41AgMBAAECggEABBx0n0AAxrhO2I6nzN0E/Xj4Lf80cn4gWdNuuLeU/Px/\n7OXbJ5eUVTo80wJeegWrQGptD/WNKP948/5T53oJuBL2vS5R7wR+g4jWVUIvMo2U\nrIj+RqznqOxmEzo4N+06yafRbb2bdStpMn7U/x2ec9mjkT2vCiktx69LbSJ8PfyX\ne00eDJA1u4Wr1reusmGpJmvatrxU2DxqWD16BEmyfOHkThY5yE9s/JdtJf5KVKO7\ngGW9/aV80UMGETfBU3O2qc9dCT1JCHmdLNb9Lc3gmorgOt/MbHra57otLDfSKaoW\nbgU1mwYAAKoncocyu1EMaE4Jx2mTosJXLpHMYSTWgQKBgQD7kln3JMiTyoOzhiJ3\ngZ8ICCsYhZ/m5ySJRk+XHiJJmPiNZpXHs+q8nLKdWr+iiaAoqkKC1coAkCDvxAFu\nxaqAtAHuj0qYI6MgJ2abbXGIgsziGFROk9UrlYi2q74O5blID+Sd1WX0XMQ9eE1S\nsQQ2PhybWQXs+phL+KeN3ZmR0QKBgQDNsnDtbqpCtwhfFhs20DS5Zxx15X5/YTLS\nlYl1yvGsU0KZjQc0gAuZqDxlTOy+3w3tKLnDrfOQjqmPWRXeVuYgDxqE9a7TuWu0\nCxVUdYx6udDY1xe4s0EPZplNqqjDqQFlCfG7T9/gKpAijrxHW+aiX4bjY263psLH\nAbjVZrd7JQKBgBLHTefg2wgNKd+Qt6nsBw72bSEbeGAoCNYmZXKGUVDlFkiXy75o\nc7E4kSylxYBAfbALZYOWqcl4+LxtCR5Xqu6IgUxpbcwFfPu9dS9M8BiciualokVr\nS5JBSz83eqxqAXabmRkfAMlI020zObJefE4APOprrsGNwyiImxk/3WLBAoGBAIvl\nPGB+z1UoXo0s371bxUADHJwiRPIlDQejpCV0rQDib303KRtPqpQKk2jh9HGsCjCt\nbgnjmK9MF43irLjWqRRMsWCUJx7gEJwWnZ8fgzdEgQG45+06HJl40fK8iqLnoocx\nSDJ4lG5FBFo8cVim7Ciqh3bG/VnyFK58QVUB0u/xAoGAKyWi88/AIZAFubkcCDH2\nf/lfnJxrv9MHUBYFheCRQmEeFm8AQ7tiZhEjPufpDQUZXt2cfRbCKpKqTMYTXbqo\nN81w/2aRaaOldxcIv2sSpwbnbNZo6MMiADj/ZoiZL75v+uOdOGvITs2Tdz2whlhQ\ndu6ybJz+agUEKZyr+gwFJqU=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-42f2x@marketplace-bd8d7.iam.gserviceaccount.com",
  "client_id": "108037531896044559929",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-42f2x%40marketplace-bd8d7.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase
init(autoreset=True)
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
    print(f"Buyer '{name}' updated with balance {balance}TOS.")

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
    print(f"Item '{item_name}' listed with {quantity} units at {price}TOS each.")

def view_items():
    items = db.collection('items').stream()
    if not items:
        print("No items listed.")
    else:
        print("Items available:")
        for item in items:
            item_data = item.to_dict()
            print(f"{item.id}: {item_data['quantity']} available at {item_data['price']}TOS each.")

def update_item():
    item_name = input("Enter item name: ")
    try:
        quantity = int(input("Enter new quantity: "))
    except ValueError:
        print_colored("Invalid quantity. Please enter a numeric value.", Fore.RED)
        return
    try:
        price = float(input(Fore.CYAN + "Enter new price: " + Style.RESET_ALL))
    except ValueError:
        print_colored("Invalid price. Please enter a numeric value.", Fore.RED)
        return
    
    item_ref = db.collection('items').document(item_name)
    item_ref.update({'quantity': quantity})
    item_ref.update({'price': price})
    print(f"Updated '{item_name}' to {quantity} units.")

def view_buyers():
    buyers = db.collection('approved_buyers').stream()
    if not buyers:
        print_colored("No approved buyers found.", Fore.RED)
        return

    print(Fore.CYAN + "Approved buyers:" + Style.RESET_ALL)
    for buyer in buyers:
        buyer_data = buyer.to_dict()
        balance = buyer_data.get('balance', 'N/A')
        print(f"Team Name : {buyer.id}, \tBalance : {balance}TOS.")

def view_all_purchases():
    purchases = db.collection('purchases').stream()
    if not purchases:
        print_colored("No purchases found.", Fore.RED)
        return

    print("All purchases:")
    for purchase in purchases:
        purchase_data = purchase.to_dict()
        print(f"Customer: {purchase_data['customer']}, \tItem: {purchase_data['item']}, "
              f"\tQuantity: {purchase_data['quantity']}, \tTotal Price: {purchase_data['total_price']}TOS")

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def toggle_marketplace_status():
    status_ref = db.collection('marketplace_status').document('status')
    status_doc = status_ref.get()
    
    if status_doc.exists:
        current_status = status_doc.to_dict().get('is_active', True)
        new_status = not current_status
    else:
        new_status = False
    
    status_ref.set({'is_active': new_status})
    
    if new_status:
        print_colored("Marketplace has been started. Customers can now make transactions.", Fore.GREEN)
    else:
        print_colored("Marketplace has been stopped. Customers cannot make transactions.", Fore.YELLOW)

def Iste_logo():
    print_colored('''
                ██╗ ███████╗ ████████╗ ███████╗
                ██║ ██╔════╝ ╚══██╔══╝ ██╔════╝
                ██║ ███████╗    ██║    █████╗  
                ██║ ╚════██║    ██║    ██╔══╝  
                ██║ ███████║    ██║    ███████╗
                ╚═╝ ╚══════╝    ╚═╝    ╚══════╝
                                             ''')

def main():
    Iste_logo()
    while True:
        print(Fore.CYAN + "\nSeller CLI" + Style.RESET_ALL)
        print("1. Add/Update Approved Buyer")
        print("2. List Item")
        print("3. View Items")
        print("4. Update Item")
        print("5. View Approved Buyers")
        print("6. View All Purchases")
        print("7. Toggle Marketplace Status")
        print("8. Exit")
        
        choice = input(Fore.CYAN + "Choose an option: " + Style.RESET_ALL)
        
        if choice == '1':
            add_or_update_approved_buyer()
        elif choice == '2':
            list_item()
        elif choice == '3':
            view_items()
        elif choice == '4':
            update_item()
        elif choice == '5':
            view_buyers()
        elif choice == '6':
            view_all_purchases()
        elif choice == '7':
            toggle_marketplace_status()
        elif choice == '8':
            break
        else:
            print_colored("Invalid choice, please try again.", Fore.RED)

if __name__ == "__main__":
    main()