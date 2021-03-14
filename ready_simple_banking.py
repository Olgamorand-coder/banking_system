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
        #if self.card_number!=None:
         #   self.balance=self.get_balance_by_num()
       # else:
        self.balance=0
    def get_balance(self):
        print(f"Balance: {self.balance}\n")
    def print_menu(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
##########################################################
    def log_in_menu(self):

        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        try:
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
                self.balance = self.get_balance_by_num()
                print("Enter income:")
                income = int(input())  # check this input
                new_balance=self.enter_income(income)
                self.balance=new_balance
                print('Income was added!')
            elif choice==3:
                self.balance = self.get_balance_by_num()
                print("Enter card number:")
                recipient=str(input())
                if self.luhn_check(recipient):
                    if self.card_exist(recipient):
                        print('Enter how much money you want to transfer:')
                        amount=int(input())
                        if amount<=self.balance:
                            self.make_transfer(recipient, amount)
                        else:
                            print("Not enough money!")
                    else:
                        print("Such a card does not exist.")
                else:
                    print("Probably you made a mistake in the card number. Please try again!")
            elif choice==4:
                self.remove_card()
                self.print_menu()
                return 'log out'
            elif choice==5:
                print('You have successfully logged out!')
                self.print_menu()
                return 'log out'
            else:
                print('you should choose num from 0-5')
        except ValueError:
            print('Incorrect input')
################################################################################
    def remove_card(self):
        with conn:
            cur.execute("""Delete from card WHERE number=:number AND pin=:pin""",
                      {'number': self.card_number, 'pin': self.pin})
            print('The account has been closed')
    def card_exist(self, card_num):

        cur.execute("SELECT number FROM card WHERE number=?", (card_num,))
        if cur.fetchone()==None:
            return False
        else:
            return True
    def make_transfer(self, recip, amount):
        if recip==self.card_number:
            print("That's your card!")
        else:
            cur.execute("UPDATE card SET balance=:balance WHERE number=:number ", {'number':self.card_number, 'balance':(self.balance-amount)})
            conn.commit()
            cur.execute("SELECT balance FROM card WHERE number=?", (recip,))
            recip_balance=cur.fetchone()[0]
            cur.execute("UPDATE card SET balance=:balance WHERE number=:number",{'number':recip, 'balance':recip_balance+amount})
            conn.commit()
            print("Success!")
    def enter_income(self, number):
        cur.execute("UPDATE card SET balance=:balance WHERE number=:number AND pin=:pin", {'number':self.card_number, 'pin':self.pin, 'balance':self.balance+number})
        conn.commit()
        cur.execute("SELECT balance FROM card WHERE number=?",(self.card_number,))
        print('Income was added!')
        return cur.fetchone()[0]
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

    def main(self):
        self.print_menu()

        not_exit=True
        while not_exit:
            try:
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
                    try:
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
                    except TypeError:
                        print ('Error')
                        self.print_menu()
                elif choice==0:
                    print("Bye!")
                    not_exit=False
                else:
                    print('Your number should be 0-2')

            except TypeError:
                print('Type Error')

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

    def deposit(self, money):
        new_bal = self.balance + money
        with conn:
            cur.execute("""UPDATE card SET balance=:balance
            WHERE number=:number AND pin=:pin""",
                      {'balance': new_bal, 'number': self.card_number, 'pin': self.pin})
        return new_bal

    def get_balance_by_num(self):
        cur.execute("Select balance FROM card WHERE number=?", (self.card_number,))
        return cur.fetchone()[0]
first_account=Account()
first_account.main()
conn.close()