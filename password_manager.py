import base64
import hashlib
import os

from cryptography.fernet import Fernet


KEY_FILE = "key.key"
PASSWORD_FILE = "password.txt"


def generate_key(password):
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def load_key(password):
    if not os.path.exists(KEY_FILE):
        key = generate_key(password)
        with open(KEY_FILE, "wb") as file:
            file.write(key)
    else:
        with open(KEY_FILE, "rb") as file:
            key = file.read()
    return key


pswd = input("Enter your Master Password : ").strip()
fer = Fernet(load_key(pswd))


def view():
    if not os.path.exists(PASSWORD_FILE):
        print("No saved passwords yet.")
        return

    with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            name, password = line.strip().split("|", 1)
            try:
                decoded_password = fer.decrypt(password.encode()).decode()
            except Exception:
                decoded_password = password
            print(f"Name : {name}")
            print(f"Password : {decoded_password}")
            print("-" * 15)


def add():
    name = input("Enter Your Account Name : ")
    password = input("Enter your Password : ")

    with open(PASSWORD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name}|{fer.encrypt(password.encode()).decode()}\n")


while True:
    mode = input("Would you like to add new password or view existing password ones or Quit - Q : ").strip().lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid Code")
        continue



    