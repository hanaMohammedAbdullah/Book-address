import sqlite3
import hashlib

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        
        # Create tables if not exists
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, is_superuser INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS addressbook (id INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT, state TEXT, city TEXT, address TEXT, email TEXT, phone TEXT, job TEXT)")
        self.conn.commit()

    # User Management Methods
    def create_user(self, username, password, is_superuser):
        # Hash the password
        password_hash = self._hash_password(password)
        try:
            self.cur.execute("INSERT INTO users (username, password_hash, is_superuser) VALUES (?, ?, ?)", (username, password_hash, is_superuser))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            self.conn.rollback()  # User already exists with the same username
    def update_user(self, user_id, new_username, new_password, is_superuser):
        # Implement SQL update statement here
        sql = "UPDATE users SET username=?, password_hash=?, is_superuser=? WHERE id=?"
        self.cur.execute(sql, (new_username, new_password, is_superuser, user_id))
        self.conn.commit()
    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id=?"
        self.cur.execute(sql, (user_id,))
        self.conn.commit()
    def login(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if user:
            password_hash = user[2]
            if self._verify_password(password, password_hash):
                return user
        return None

    def fetch_users(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    # Password Hashing and Verification
    def _hash_password(self, password):
        salt = b'secret_salt_for_password_hashing'  # Change this to a unique value
        return hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

    def _verify_password(self, password, password_hash):
        return password_hash == self._hash_password(password)

    # Address Book Methods
    def fetch_contacts(self):
        self.cur.execute("SELECT * FROM addressbook")
        rows = self.cur.fetchall()
        return rows

    def insert_contact(self, firstName, lastName, state, city, address, email, phone, job):
        self.cur.execute("INSERT INTO addressbook (id,firstName, lastName, state, city, address, email, phone, job) VALUES (NULL,?, ?, ?, ?, ?, ?, ?, ?)",
                         (firstName, lastName, state, city, address, email, phone, job))
        self.conn.commit()

    def remove_contact(self, contact_id):
        self.cur.execute("DELETE FROM addressbook WHERE id = ?", (contact_id,))
        self.conn.commit()

    def update_contact(self, contact_id, firstName, lastName, state, city, address, email, phone, job):
        self.cur.execute("UPDATE addressbook SET firstName = ?, lastName = ?, state = ?, city = ?, address = ?, email = ?, phone = ?, job = ? WHERE id = ?",
                         (firstName, lastName, state, city, address, email, phone, job, contact_id))
        self.conn.commit()

    def search_contacts(self, search_text):
        self.cur.execute("SELECT * FROM addressbook WHERE firstName LIKE ? OR lastName LIKE ? OR state LIKE ? OR city LIKE ? OR address LIKE ? OR email LIKE ? OR phone LIKE ? OR job LIKE ?",
                         (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()


db = Database('addressbook.db')
db.create_user("admin", "password", 1)  # Superuser
db.create_user("user", "password", 0)  # Regular user
