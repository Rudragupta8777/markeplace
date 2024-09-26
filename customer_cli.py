import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Query
from colorama import init, Fore, Style

import warnings
init(autoreset=True)
# Suppress UserWarning from Firestore's where() method
warnings.filterwarnings("ignore", category=UserWarning)

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
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

def check_marketplace_status():
    status_ref = db.collection('marketplace_status').document('status')
    status_doc = status_ref.get()
    
    if status_doc.exists:
        return status_doc.to_dict().get('is_active', True)
    return True  # Default to active if status document doesn't exist

def verify_customer(name):
    customer_ref = db.collection('approved_buyers').document(name)
    doc = customer_ref.get()
    if doc.exists:
        # Check if password exists
        password_ref = db.collection('buyer_passwords').document(name)
        password_doc = password_ref.get()
        if password_doc.exists:
            while True:
                password = input(Fore.CYAN + "Enter your password: " + Style.RESET_ALL)
                if password == password_doc.to_dict()['password']:
                    balance = doc.to_dict().get('balance', 0)
                    print(f"{Fore.GREEN}Customer{Style.RESET_ALL} {name} {Fore.GREEN}verified. Balance:{Style.RESET_ALL} {balance}TOS.")
                    return balance
                else:
                    print_colored("Invalid password. Please try again.", Fore.RED)
        else:
            # First-time login, create password
            password = input(Fore.CYAN + "Create a password: " + Style.RESET_ALL)
            password_ref.set({'password': password})
            balance = doc.to_dict().get('balance', 0)
            print(f"{Fore.GREEN}Customer{Style.RESET_ALL} {name} {Fore.GREEN}verified. Balance:{Style.RESET_ALL} {balance}TOS.")
            return balance
    else:
        print_colored(f"Customer '{name}' not found.", Fore.RED)
        return None
    
def view_items():
    if not check_marketplace_status():
        print_colored("The marketplace is currently closed. Please try again later.", Fore.YELLOW)
        return {}
    items = db.collection('items').stream()
    if not items:
        print_colored("No items available.", Fore.YELLOW)
        return {}
    else:
        print_colored("Items available:", Fore.CYAN, Style.BRIGHT)
        item_dict = {}
        for index, item in enumerate(items, start=1):
            item_data = item.to_dict()
            item_dict[index] = {
                'name': item.id,
                'quantity': item_data['quantity'],
                'price': item_data['price']
            }
            print_colored(f"{index}. {Fore.GREEN}\tItem name:{Style.RESET_ALL} {item.id}{Fore.GREEN},\tQuantity:{Style.RESET_ALL} {item_data['quantity']}{Fore.GREEN},\tPrice: {Style.RESET_ALL}{item_data['price']}TOS each.")
        return item_dict

def purchase_item(name):
    if not check_marketplace_status():
        print_colored("The marketplace is currently closed. Purchases are not allowed at this time.", Fore.YELLOW)
        return
    item_dict = view_items()
    if not item_dict:
        return

    while True:
        try:
            serial_no = int(input(Fore.CYAN + "Enter the serial number of the item you want to purchase: " + Style.RESET_ALL))
            if serial_no not in item_dict:
                print_colored("Invalid serial number. Please try again.", Fore.RED)
                continue
            break
        except ValueError:
            print_colored("Please enter a valid number.", Fore.RED)

    item_name = item_dict[serial_no]['name']
    quantity = 1  # Set quantity to 1

    customer_ref = db.collection('approved_buyers').document(name)
    item_ref = db.collection('items').document(item_name)
    
    customer_doc = customer_ref.get()
    item_doc = item_ref.get()
    
    if not customer_doc.exists:
        print_colored("Customer not found.", Fore.RED)
        return
    
    if not item_doc.exists:
        print_colored("Item not found.", Fore.RED)
        return

    customer_data = customer_doc.to_dict()
    item_data = item_doc.to_dict()
    
    if item_data['quantity'] < quantity:
        print_colored("Not enough quantity available.", Fore.RED)
        return
    
    total_price = item_data['price'] * quantity
    if customer_data['balance'] < total_price:
        print_colored("Insufficient balance.", Fore.RED)
        return

    # Update item quantity
    item_ref.update({'quantity': item_data['quantity'] - quantity})
    
    # Update customer balance
    customer_ref.update({'balance': customer_data['balance'] - total_price})

    # Record or update the purchase in Firestore
    purchase_ref = db.collection('purchases').where('customer', '==', name).where('item', '==', item_name).stream()
    
    purchase_exists = False
    for purchase in purchase_ref:
        purchase_data = purchase.to_dict()
        purchase_doc_ref = purchase.reference
        new_quantity = purchase_data['quantity'] + quantity
        new_total_price = purchase_data['total_price'] + total_price
        purchase_doc_ref.update({
            'quantity': new_quantity,
            'total_price': new_total_price
        })
        purchase_exists = True
        break

    if not purchase_exists:
        db.collection('purchases').add({
            'customer': name,
            'item': item_name,
            'quantity': quantity,
            'total_price': total_price
        })
    
    print_colored(f"{Fore.GREEN}Purchased 1 unit of{Style.RESET_ALL} '{item_name}' {Fore.GREEN}for{Style.RESET_ALL} {total_price}TOS.")
    print_colored(f"{Fore.YELLOW}Remaining balance:{Style.RESET_ALL} {customer_data['balance'] - total_price}TOS.")

def view_purchases(name):
    # Query Firestore for the customer's purchases

    purchase_ref = db.collection('purchases') \
                    .where(field_path='customer', op_string='==', value=name) \
                    .stream()
    
    purchases = list(purchase_ref)
    
    if not purchases:
        print_colored("No purchases found for this customer.", Fore.RED)
        return
    
    print_colored("Purchase history:", Fore.GREEN)
    for purchase in purchases:
        purchase_data = purchase.to_dict()
        print(f"{Fore.GREEN}Item:{Style.RESET_ALL} {purchase_data['item']}{Fore.GREEN},\tQuantity:{Style.RESET_ALL} {purchase_data['quantity']}{Fore.GREEN},\tTotal Price:{Style.RESET_ALL} {purchase_data['total_price']}TOS")

def check_balance(name):
    customer_ref = db.collection('approved_buyers').document(name)
    doc = customer_ref.get()
    if doc.exists:
        balance = doc.to_dict().get('balance', 0)
        print_colored(f"{Fore.GREEN}Your current balance is:{Style.RESET_ALL} {balance}TOS.")
    else:
        print_colored(f"Customer '{name}' not found.", Fore.RED)

# ... (rest of the code remains the same)
def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def marketplace_logo():
    print_colored('''
          
          ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗██████╗ ██╗      █████╗  ██████╗███████╗
          ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝
          ██╔████╔██║███████║██████╔╝█████╔╝ █████╗     ██║   ██████╔╝██║     ███████║██║     █████╗  
          ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝     ██║   ██╔═══╝ ██║     ██╔══██║██║     ██╔══╝  
          ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗   ██║   ██║     ███████╗██║  ██║╚██████╗███████╗
          ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝
                                                                                                      ''', Fore.YELLOW)

def main():
    marketplace_logo()
    customer_name = None
    balance = 0

    while True:
        if customer_name is None:
            # Ask for the name and verify it
            name = input(Fore.CYAN + "Enter your team name: " + Style.RESET_ALL)
            balance = verify_customer(name)
            if balance is not None:
                customer_name = name
            else:
                print_colored("Your team is not on the approved list. Contact admin for access.", Fore.RED)
                continue
        else:
            # Show the menu and perform actions
            print_colored("\nCustomer CLI", Fore.CYAN, Style.BRIGHT)
            print("1. View Items")
            print("2. Purchase Item")
            print("3. View Purchases")
            print("4. Check Balance")
            print("5. Exit\n")
            choice = input(Fore.CYAN + "Choose an option: " + Style.RESET_ALL)

            if choice == '1':
                view_items()
            elif choice == '2':
                purchase_item(customer_name)
            elif choice == '3':
                view_purchases(customer_name)
            elif choice == '4':
                check_balance(customer_name)
            elif choice == '5':
                break
            else:
                print_colored("Invalid choice, please try again.", Fore.RED)

if __name__ == "__main__":
    main()