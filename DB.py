
import sqlite3

conn=sqlite3.connect("example.s3db")
cur=conn.cursor()

class DB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT(16), pin TEXT(4), balance INT)")
        self.conn.commit()

    def insert(self, c_num, c_pin, c_bal):
        self.cur.execute('INSERT INTO card (number, pin, balance) Values(?, ?, ?)', (c_num, c_pin, c_bal))
        self.conn.commit()

    def select_card(self, card_num):
        self.cur.execute('SELECT * FROM card WHERE number=?',card_num)
        return cur.fetchone()[0]

    def exit(self):
        self.conn.close()

    def check_pin(self, card_num, entered_pin):
        cur.execute("SELECT pin FROM card WHERE number=? ", (card_num,))
        if (cur.fetchone()[0]) == entered_pin:
            return True
        else:
            return False
    def card_exist(self, card_num):
        cur.execute("SELECT number FROM card WHERE number=?", (card_num,))
        if cur.fetchone()==None:
            return False
        else:
            return True







