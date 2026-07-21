import sqlite3

DB_FILE = 'passwords.db'


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        'CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, name TEXT UNIQUE, password TEXT)'
    )
    return conn


def view(conn):
    cursor = conn.execute('SELECT name, password FROM passwords ORDER BY name')
    rows = cursor.fetchall()

    if not rows:
        print('No passwords stored yet.')
        return

    print('\nSaved passwords:')
    print('-' * 20)
    for name, password in rows:
        print(f'Name    : {name}')
        print(f'Password: {password}')
        print('-' * 20)


def add(conn):
    name = input('Enter account name: ').strip()
    if not name:
        print('Account name cannot be empty.')
        return

    password = input('Enter password: ').strip()
    if not password:
        print('Password cannot be empty.')
        return

    conn.execute(
        'INSERT OR REPLACE INTO passwords (name, password) VALUES (?, ?)',
        (name, password)
    )
    conn.commit()
    print('Password saved.')


def main():
    conn = get_connection()

    while True:
        choice = input('\nChoose an action: view, add, quit: ').strip().lower()
        if choice in ('q', 'quit'):
            break
        elif choice == 'view':
            view(conn)
        elif choice == 'add':
            add(conn)
        else:
            print('Please type view, add, or quit.')

    conn.close()


if __name__ == '__main__':
    main()



    