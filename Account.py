
import sqlite3

conn=sqlite3.connect("example.s3db")
cur=conn.cursor()
from random import randint
class Account:
    def __init__(self):
        self.number=None
        self.pin=None

        self.balance=0
    def get_number(self):
        return self.number
    def get_pin(self):
        return self.pin
    def get_balance(self):
        return self.balance
    def set_balance(self, balance):
        cur.execute("SELECT balance FROM card WHERE number=? ", (self.number,))
        self.balance=cur.fetchone()[0]
    def update_balance(self):
        cur.execute("SELECT balance FROM card WHERE number=? ", (self.number,))
        self.balance = cur.fetchone()[0]


    def create_pin(self):
        pin=''
        for i in range(4):
            pin+=str(randint(0, 9))
        self.pin=pin
        return pin
    def create_card_num(self):
        num='400000'

        for i in range(10):
            num+=str(randint(0,9))
        valid_num=self.luhn(num)
        self.number=valid_num
        return valid_num

    def luhn(self, number):
        number_list = [int(i) for i in str(number)]

        for i in range(0, len(number_list) - 1):
            if i % 2 == 0:
                number_list[i] *= 2
        for i in range(0, len(number_list) - 1):
            if number_list[i] > 9:
                number_list[i] -= 9
        number_sum = sum(number_list[0:-1])
        if number_sum % 10 == 0:
            last_num = 0
        else:
            last_num = 10 - (number_sum % 10)
        result = number[0: -1] + str(last_num)
        return str(result)

    def luhn_check(self, number):
        try:
            number_list=[int(i)for i in str(number)]
            for i in range(0, len(number_list)):
                if i % 2 == 0:
                    number_list[i] *= 2
            for i in range(0, len(number_list)):
                if number_list[i] > 9:
                    number_list[i] -= 9
            num_sum=sum(number_list[0:])
            if num_sum%10==0:
                return True
            else:
                return False
        except ValueError:
            return True

    def log_into(self, entered_num, entered_pin):
        if str(entered_num)==self.number and str(entered_pin)==self.pin:
            return True
        else:
            return False

    def deposit(self, money):
        new_bal = self.balance + money
        with conn:
            cur.execute("""UPDATE card SET balance=:balance
            WHERE number=:number AND pin=:pin""",
                      {'balance': new_bal, 'number': self.number, 'pin': self.pin})
        return new_bal

    def make_transfer(self, recip, amount):
        if recip==self.number:
            print("That's your card!")
        else:
            cur.execute("UPDATE card SET balance=:balance WHERE number=:number ", {'number':self.number, 'balance':(self.balance-amount)})
            self.set_balance(self.balance-amount)
            conn.commit()

            cur.execute("SELECT balance FROM card WHERE number=?", (recip,))
            recip_balance=cur.fetchone()[0]
            cur.execute("UPDATE card SET balance=:balance WHERE number=:number",{'number':recip, 'balance':recip_balance+amount})
            conn.commit()


    def remove_card(self):
        with conn:
            cur.execute("""Delete from card WHERE number=:number AND pin=:pin""",
                      {'number': self.number, 'pin': self.pin})







