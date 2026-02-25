import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, master_password):
        self.salt = b'\x14\x87\x9e\x1c\x9b\x8f\x8d\x8c\x8e\x8b\x8a\x89\x88\x87\x86\x85' # Fixed salt for simplicity in this demo
        self.key = self._generate_key(master_password)
        self.fernet = Fernet(self.key)
        self.db_file = 'passwords.json'
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)

    def _generate_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def add_password(self, service, username, password):
        with open(self.db_file, 'r') as f:
            data = json.load(f)
        
        encrypted_password = self.fernet.encrypt(password.encode()).decode()
        data[service] = {'username': username, 'password': encrypted_password}
        
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Password for {service} added successfully.")

    def get_password(self, service):
        with open(self.db_file, 'r') as f:
            data = json.load(f)
        
        if service in data:
            encrypted_password = data[service]['password']
            decrypted_password = self.fernet.decrypt(encrypted_password.encode()).decode()
            return data[service]['username'], decrypted_password
        else:
            return None

    def list_services(self):
        with open(self.db_file, 'r') as f:
            data = json.load(f)
        return list(data.keys())

def main():
    print("--- Professional Password Manager ---")
    master_pwd = input("Enter master password: ")
    pm = PasswordManager(master_pwd)

    while True:
        print("\n1. Add Password")
        print("2. Get Password")
        print("3. List Services")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            service = input("Service: ")
            username = input("Username: ")
            password = input("Password: ")
            pm.add_password(service, username, password)
        elif choice == '2':
            service = input("Service: ")
            result = pm.get_password(service)
            if result:
                print(f"Username: {result[0]}\nPassword: {result[1]}")
            else:
                print("Service not found.")
        elif choice == '3':
            services = pm.list_services()
            print("Services:", ", ".join(services))
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
