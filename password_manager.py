import sqlite3
from cryptography.fernet import Fernet


# only once to generate key

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# if key not empty
with open("key.key", "rb") as file:
        key = file.read()
        if key is None:
            write_key()

def load_key():
    with open("key.key", "rb") as file:
        key = file.read()
    return key


# Master Password
pswd = input("Enter your Master Password: ")

# Encryption 
key = load_key() + pswd.encode()
fer = Fernet(key)

# SQLite Database

conn = sqlite3.connect("password.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_name TEXT NOT NULL,
    encrypted_password TEXT NOT NULL
)
""")

conn.commit()


def add():
    name = input("Enter Your Account Name : ")
    password = input("Enter Your Password : ")

    encrypted = fer.encrypt(password.encode()).decode()

    # Store in SQLite Database
    cursor.execute(
        "INSERT INTO passwords(account_name, encrypted_password) VALUES(?, ?)",
        (name, encrypted)
    )

    conn.commit()

    print("Password saved successfully")


# View from Database

def view_db():
    cursor.execute("SELECT account_name, encrypted_password FROM passwords")

    data = cursor.fetchall()

    if not data:
        print("Database is empty.")
        return

    for name, password in data:
        print(f"\nName : {name}")
        print(f"Password : {fer.decrypt(password.encode()).decode()}")
        print("-" * 25)

def delete():
    name = input("Enter the you want to delete : ")
    cursor.execute("DELETE FROM passwords WHERE account_name = ?",(name,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Password updated successfully.")
    else:
        print("Account not found.")


def update():
    name = input("Enter Your Account Name : ")
    password = input("Enter Your New Password : ")
    encrypted = fer.encrypt(password.encode()).decode()
    cursor.execute("""
        UPDATE passwords
        SET encrypted_password = ?
        WHERE account_name = ?
        """,(encrypted, name))
    conn.commit()
    if cursor.rowcount == 0:
        print("Name Not Found")
    else:
        print("Password Updated successfully")

conn.commit()


# Main Program


while True:

    mode = input(
        "\nChoose Option\n"
        "1 - Add Password\n"
        "2 - View From Database\n"
        "3 - Update Password\n"
        "4 - Delete Data\n"
        "5 - Quit\n\n"
        "Enter Choice : "
    ).lower()

    if mode == "5":
        break

    elif mode == "1":
        add()

    elif mode == "2":
        view_db()

    elif mode == "3":
        update()

    elif mode == "4":
        delete()
    else:
        print("Invalid Option")


conn.close()