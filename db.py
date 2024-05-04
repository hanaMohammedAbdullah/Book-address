import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # first_name.get(), lastName_text.get(),
            #   state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS addressbook (id INTEGER PRIMARY KEY, firstName text, lastName text, state text , city text, address text, email text, phone text, street text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM addressbook")
        rows = self.cur.fetchall()
        return rows

    def insert(self, firstName, lastName, state, city, address, email, phone, street):  
        self.cur.execute("INSERT INTO addressbook VALUES (NULL, ?, ?, ?, ? , ? , ? ,? , ?)",
                         (firstName, lastName, state, city, address, email, phone, street))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM addressbook WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, firstName, lastName, state, city, address, email, phone, street):
        self.cur.execute("UPDATE addressbook SET firstName = ?, lastName = ?,  state= ?, city = ? , address = ? , email = ?,phone = ? , street = ? WHERE id = ?",
                         (firstName, lastName, state, city, address, email, phone, street , id))
        self.conn.commit()

    def search(self, search_text):
        self.cur.execute("SELECT * FROM addressbook WHERE firstName LIKE '%"+search_text+"%' OR lastName LIKE '%"+search_text+"% 'OR state LIKE  '%"+search_text+"%' OR city LIKE '%"+search_text+"%' OR address LIKE '%"+search_text+"%' OR email LIKE '%"+search_text+"%' OR phone LIKE '%"+search_text+"%' OR street LIKE '%"+search_text+"%'")       
        rows = self.cur.fetchall()
        return rows
        

    def __del__(self):
        self.conn.close()


# db = Database('addressbook.db')
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")
# db.insert("hana", "muhammed", "kurdistan", "erbil", "40 meter ,erbil", "hano@gmail.com", "07503073718", "byaraty")

