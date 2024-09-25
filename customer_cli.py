import firebase_admin
from firebase_admin import credentials, firestore

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

def view_items():
    items = db.collection('items').stream()
    if not items:
        print("No items available.")
    else:
        print("Items available for purchase:")
        for item in items:
            item_data = item.to_dict()
            print(f"{item.id}: {item_data['quantity']} units available at ${item_data['price']} each.")

def buy_item(item_name, quantity):
    global customer_balance  # Declare the use of the global variable
    item_ref = db.collection('items').document(item_name)
    item = item_ref.get()
    if not item.exists:
        print(f"Item '{item_name}' not available.")
        return

    item_data = item.to_dict()
    total_price = item_data['price'] * quantity
    
    if item_data['quantity'] < quantity:
        print(f"Not enough '{item_name}' in stock.")
    elif customer_balance < total_price:
        print("Insufficient balance.")
    else:
        # Update Firestore with purchase
        item_ref.update({'quantity': firestore.Increment(-quantity)})
        customer_balance -= total_price  # Deduct the total price from the customer's balance
        print(f"Purchased {quantity} of '{item_name}' for ${total_price}. Remaining balance: ${customer_balance:.2f}.")

def add_approved_buyer(name):
    approved_buyers_ref = db.collection('approved_buyers').document(name)
    approved_buyers_ref.set({
        'name': name
    })
    print(f"Added '{name}' to approved buyers list.")

def view_balance(name):
    approved_buyers_ref = db.collection('approved_buyers').document(name)
    buyer = approved_buyers_ref.get()
    if buyer.exists:
        data = buyer.to_dict()
        balance = data.get('balance')  # Safely get the balance field
        if balance is not None:
            print(f"Balance for '{name}': ${balance:.2f}")
        else:
            print(f"Balance field not found for '{name}'.")
    else:
        print(f"Approved buyer '{name}' not found.")


def main():
    name = input("Enter your name: ")
    add_approved_buyer(name)  # Ensure the customer is an approved buyer
    
    while True:
        print("\nCustomer CLI")
        print("1. View Items")
        print("2. Buy Item")
        print("3. View Balance")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            view_items()
        elif choice == '2':
            item_name = input("Enter item name to buy: ")
            quantity = int(input("Enter quantity to buy: "))
            buy_item(item_name, quantity)
        elif choice == '3':
            view_balance(name)
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()