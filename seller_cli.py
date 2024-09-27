import firebase_admin
from firebase_admin import credentials, firestore
from colorama import init, Fore, Style
from google.cloud.firestore import Query

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
    print(f"Buyer '{name}' updated with balance {balance} TOS.")

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
    print(f"Item '{item_name}' listed with {quantity} units at {price} TOS each.")

def view_items():
    items = db.collection('items').stream()
    if not items:
        print("No items listed.")
    else:
        print("Items available:")
        for item in items:
            item_data = item.to_dict()
            print(f"{item.id}: {item_data['quantity']} available at {item_data['price']} TOS each.")

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
        print(f"Team Name : {buyer.id}, \tBalance : {balance} TOS.")

def view_all_purchases():
    purchases = db.collection('purchases').stream()
    if not purchases:
        print_colored("No purchases found.", Fore.RED)
        return

    print("All purchases:")
    for purchase in purchases:
        purchase_data = purchase.to_dict()
        print(f"Customer: {purchase_data['customer']}, \tItem: {purchase_data['item']}, "
              f"\tQuantity: {purchase_data['quantity']}, \tTotal Price: {purchase_data['total_price']} TOS")

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def toggle_marketplace_status():
    # Get all approved buyers (teams)
    buyers_ref = db.collection('approved_buyers').stream()
    
    # Get the current global status
    global_status_ref = db.collection('marketplace_status').document('global')
    global_status_doc = global_status_ref.get()
    
    if global_status_doc.exists:
        current_status = global_status_doc.to_dict().get('is_active', True)
        new_status = not current_status
    else:
        new_status = False
    
    # Update global status
    global_status_ref.set({'is_active': new_status})
    
    # Update status for each team
    for buyer in buyers_ref:
        team_name = buyer.id
        team_status_ref = db.collection('marketplace_status').document(team_name)
        team_status_ref.set({'is_active': new_status})
    
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

def add_sabotage_option():
    name = input("Enter the sabotage option name: ")
    try:
        cost = float(input("Enter the cost of the sabotage option: "))
    except ValueError:
        print_colored("Invalid cost. Please enter a numeric value.", Fore.RED)
        return

    sabotage_ref = db.collection('sabotage_options').document(name)
    sabotage_ref.set({'name': name, 'cost': cost})
    print_colored(f"Sabotage option '{name}' added with cost {cost} TOS.", Fore.GREEN)

def view_sabotage_options():
    options = db.collection('sabotage_options').stream()
    if not options:
        print_colored("No sabotage options available.", Fore.YELLOW)
        return

    print_colored("Sabotage options:", Fore.CYAN)
    for option in options:
        option_data = option.to_dict()
        print(f"{option_data['name']} - Cost: {option_data['cost']} TOS")

def view_sabotage_attempts():
    attempts = db.collection('sabotage_attempts').order_by('timestamp', direction=Query.DESCENDING).stream()
    if not attempts:
        print_colored("No sabotage attempts found.", Fore.YELLOW)
        return

    print_colored("Sabotage attempts:", Fore.CYAN)
    for attempt in attempts:
        attempt_data = attempt.to_dict()
        # Ensure all keys are present before accessing
        customer = attempt_data.get('customer', 'N/A')
        target_team = attempt_data.get('target_team', 'N/A')
        sabotage_option = attempt_data.get('sabotage_option', 'N/A')
        cost = attempt_data.get('cost', 'N/A')
        timestamp = attempt_data.get('timestamp', 'N/A')
        status = attempt_data.get('status', 'N/A')

        print(f"Customer: {customer}, Target: {target_team}, Option: {sabotage_option}, "
              f"Cost: {cost} TOS, Time: {timestamp}, Status: {status}\n")

def remove_sabotage():
    target_team = input("Enter the team name to remove sabotage from: ")
    
    # Check if the target team exists
    target_team_ref = db.collection('approved_buyers').document(target_team)
    if not target_team_ref.get().exists:
        print_colored(f"Team '{target_team}' does not exist.", Fore.RED)
        return

    # Re-enable the target team's marketplace access
    db.collection('marketplace_status').document(target_team).set({'is_active': True})

    # Update all active sabotage attempts for this team to 'resolved'
    sabotage_query = db.collection('sabotage_attempts').where('target_team', '==', target_team).where('status', '==', 'active')
    for attempt in sabotage_query.stream():
        attempt.reference.update({'status': 'resolved'})

    print_colored(f"Sabotage removed from team '{target_team}'. Their marketplace access has been restored.", Fore.GREEN)

def toggle_team_marketplace_status():
    team_name = input("Enter the team name to toggle marketplace status: ")
    
    # Check if the team exists
    team_ref = db.collection('approved_buyers').document(team_name)
    if not team_ref.get().exists:
        print_colored(f"Team '{team_name}' does not exist.", Fore.RED)
        return

    status_ref = db.collection('marketplace_status').document(team_name)
    status_doc = status_ref.get()
    
    if status_doc.exists:
        current_status = status_doc.to_dict().get('is_active', True)
        new_status = not current_status
    else:
        new_status = False
    
    status_ref.set({'is_active': new_status})
    
    if new_status:
        print_colored(f"Marketplace access for team '{team_name}' has been enabled.", Fore.GREEN)
    else:
        print_colored(f"Marketplace access for team '{team_name}' has been disabled.", Fore.YELLOW)

def set_sabotage_cost():
    try:
        cost = float(input("Enter the cost for sabotage: "))
        if cost < 0:
            raise ValueError("Cost cannot be negative")
        
        # Set the sabotage cost in Firestore
        db.collection('game_settings').document('sabotage').set({'cost': cost})
        print_colored(f"Sabotage cost set to {cost} TOS.", Fore.GREEN)
    except ValueError as e:
        print_colored(f"Invalid input: {str(e)}", Fore.RED)


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
        print("8. Add Sabotage Option")
        print("9. View Sabotage Options")
        print("10. View Sabotage Attempts")
        print("11. Remove Sabotage")
        print("12. Toggle Team Marketplace Status")
        print("13. Set Sabotage Cost")  # New option
        print("14. Exit")
        
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
            add_sabotage_option()
        elif choice == '9':
            view_sabotage_options()
        elif choice == '10':
            view_sabotage_attempts()
        elif choice == '11':
            remove_sabotage()
        elif choice == '12':
            toggle_team_marketplace_status()
         # ... (previous options remain the same)
        elif choice == '13':
            set_sabotage_cost()
        elif choice == '14':
            break
        else:
            print_colored("Invalid choice, please try again.", Fore.RED)

if __name__ == "__main__":
    main()