import os
import json
import csv
import argparse
import concurrent.futures
from cryptography.fernet import Fernet
from eth_account import Account
from eth_account.hdaccount import generate_mnemonic

# Encryption Key File (for security)
ENCRYPTION_KEY_FILE = "encryption_key.txt"

# Generate or Load Encryption Key
def get_encryption_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(ENCRYPTION_KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

cipher = get_encryption_key()

# Encrypt & Decrypt Functions
def encrypt_private_key(private_key):
    return cipher.encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted_key):
    return cipher.decrypt(encrypted_key.encode()).decode()

# Generate Wallet (Single Wallet)
def generate_wallet():
    account = Account.create()
    private_key = account.key.hex()
    public_address = account.address
    encrypted_key = encrypt_private_key(private_key)
    return encrypted_key, public_address

# Generate Multiple Wallets Using Multithreading
def generate_wallets(num_wallets):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        wallets = list(executor.map(lambda _: generate_wallet(), range(num_wallets)))
    return wallets

# Generate Wallets from Mnemonic
def generate_wallets_from_mnemonic(mnemonic, num_wallets):
    wallets = []
    for i in range(num_wallets):
        account = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/{i}")
        encrypted_key = encrypt_private_key(account.key.hex())
        wallets.append((encrypted_key, account.address))
    return wallets

# Save Wallets in Different Formats
def save_wallets(wallets, folder="wallets", format="txt"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"wallets.{format}")

    if format == "txt":
        with open(file_path, "w") as file:
            for private_key, public_address in wallets:
                file.write(f"Encrypted Private Key: {private_key}\nPublic Address: {public_address}\n\n")

    elif format == "csv":
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Encrypted Private Key", "Public Address"])
            writer.writerows(wallets)

    elif format == "json":
        with open(file_path, "w") as file:
            json.dump([{"encrypted_private_key": pk, "public_address": pa} for pk, pa in wallets], file, indent=4)

    print(f"✅  {len(wallets)} wallets saved in '{file_path}'")

# CLI Interface
def main():
    parser = argparse.ArgumentParser(description="Generate EVM wallets securely.")
    parser.add_argument("-n", "--num", type=int, default=1, help="Number of wallets to generate")
    parser.add_argument("-f", "--format", type=str, choices=["txt", "csv", "json"], default="txt", help="Output format")
    parser.add_argument("-m", "--mnemonic", type=str, help="Use a mnemonic to generate wallets instead of random keys")
    
    args = parser.parse_args()

    if args.num <= 0:
        print("⚠️ Enter a valid positive number.")
        return

    if args.mnemonic:
        wallets = generate_wallets_from_mnemonic(args.mnemonic, args.num)
        print("📌 Wallets generated from mnemonic.")
    else:
        wallets = generate_wallets(args.num)
        print("📌 Random wallets generated.")

    save_wallets(wallets, format=args.format)

if __name__ == "__main__":
    main()

