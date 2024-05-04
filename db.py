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
# ("hana", "muhammed", "kurdistan", "erbil", "40 meter, erbil", "hano@gmail.com", "07503073718", "byaraty"),
#     
#   DATA= [("alice", "jones", "Canada", "Toronto", "456 Elm Street", "alice@example.com", "987-654-3210", "Designer"),
#     ("mohammed", "ali", "Egypt", "Cairo", "789 Nile Avenue", "mohammed@example.com", "555-123-4567", "Engineer"),
#     ("emma", "wang", "China", "Beijing", "321 Great Wall Road", "emma@example.com", "888-999-7777", "Manager"),
#     ("alex", "gonzalez", "Mexico", "Mexico City", "567 Revolution Avenue", "alex@example.com", "111-222-3333", "Sales"),
#     ("sophia", "kim", "South Korea", "Seoul", "987 Gangnam Boulevard", "sophia@example.com", "333-444-5555", "Marketing"),
#     ("ahmad", "ahmadi", "Iran", "Tehran", "654 Ferdowsi Street", "ahmad@example.com", "666-777-8888", "Researcher"),
#     ("lucia", "garcia", "Spain", "Madrid", "876 Prado Lane", "lucia@example.com", "999-000-1111", "Writer"),
#     ("marius", "jensen", "Norway", "Oslo", "234 Fjord Street", "marius@example.com", "222-333-4444", "Artist") I INSSER THOSE DATA TO THE DATABASE
# # db.insert(("john", "smith", "USA", "New York", "123 Main Street", "john@example.com", "123-456-7890", "Developer")]
# db.insert("john", "smith", "USA", "New York", "123 Main Street", "JOSNN@KCNEKN.COM", "123-456-7890", "Developer")
# db.insert("alice", "jones", "Canada", "Toronto", "456 Elm Street", "YAHOO.COM", "987-654-3210", "Designer")

#

