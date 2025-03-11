import os
from eth_account import Account

def generate_wallets(num_wallets):
    wallets = []
    for i in range(num_wallets):
        account = Account.create()
        private_key = account.key.hex()  # Correct way to get the private key
        public_address = account.address
        wallets.append((private_key, public_address))
        print(f"Wallet {i+1}:")
        print(f"Private Key: {private_key}")
        print(f"Public Address: {public_address}\n")
    return wallets

def save_wallets(wallets, folder="wallets"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "wallets.txt")
    with open(file_path, "w") as file:
        for private_key, public_address in wallets:
            file.write(f"Private Key: {private_key}\nPublic Address: {public_address}\n\n")
    print(f"✅ {len(wallets)} wallets saved in '{file_path}'")

def main():
    try:
        num_wallets = int(input("How many wallets do you want to generate? "))
        if num_wallets <= 0:
            print("⚠️ Enter a valid positive number.")
            return
        wallets = generate_wallets(num_wallets)
        save_wallets(wallets)
    except ValueError:
        print("❌ Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
