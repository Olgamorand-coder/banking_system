
from random import randint
import sqlite3
conn = sqlite3.connect('example.s3db')
cur=conn.cursor()
#cur.execute("CREATE TABLE card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT(16), pin TEXT(4), balance INT)")
#conn.commit()
class Account:
    #list_of_cards=[]
    def __init__(self):
        self.card_number=None
        self.pin=None
        self.balance=0
    def get_balance(self):
        print(f"Balance: {self.balance}\n")
    def print_menu(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

    def log_in_menu(self):

        print("1. Balance\n2. Log out\n0. Exit")
        choice=int(input())
        if choice==0:
            print("Bye!")
            return 'exit'
        elif choice==1:
            cur.execute("SELECT balance FROM card WHERE number=? ", (self.card_number,))

            print("Balance:", cur.fetchone()[0])
            #print("Balance: 0")
            return "balance"
        elif choice==2:
            print('You have successfully logged out!')
            self.print_menu()
            return 'log out'

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


    def main(self):
        self.print_menu()

        not_exit=True
        while not_exit:
            choice = int(input())
            if choice==1:
                c_n=self.create_card_num()
                print("Your card has been created\nYour card number:\n"+str(c_n))
                p_n=self.create_pin()
                print("Your card PIN:\n"+str(p_n)+"\n")
                new_card = (c_n, p_n, 0)
                cur.execute('INSERT INTO card (number, pin, balance) Values(?, ?, ?)', new_card)
                conn.commit()

                #self.list_of_cards.append([str(c_n), str(p_n)])
                self.print_menu()
            elif choice==2:

                card_num=str(input("Enter your card number:\n"))
                entered_pin=str(input("Enter your PIN:\n"))
                #if [str(card_num), str(pin)] in self.list_of_cards:
                cur.execute("SELECT pin FROM card WHERE number=? ", (card_num,))
                if (cur.fetchone()[0])==entered_pin:
                    self.card_number=card_num
                    self.pin=entered_pin
                    print("You have successfully logged in!")

                    not_quit=True
                    while not_quit==True:
                        choice=self.log_in_menu()
                        if choice =='exit':
                            not_quit=False
                            not_exit=False
                        elif choice=='log out':
                            not_quit=False


                else:
                    print("Wrong card number or PIN!")
                    self.print_menu()
            elif choice==0:
                print("Bye!")
                not_exit=False


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
        self.card_number=valid_num
        return valid_num
    def log_into(self, entered_num, entered_pin):
        if str(entered_num)==self.card_number and str(entered_pin)==self.pin:
            return True
        else:
            return False
first_account=Account()
first_account.main()
conn.close()