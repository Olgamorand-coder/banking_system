from DB import DB
from Account import Account

import sqlite3

conn=sqlite3.connect("example.s3db")
cur=conn.cursor()


def print_main_menu():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')

def print_account_menu():
    print('1. Balance')
    print('2. Log out')
    print('0. Exit')
def log_in_menu(db, account):


    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    try:
        choice = int(input())
        if choice == 0:
            print("Bye!")
            return 'exit'
        elif choice == 1:
            cur.execute("SELECT balance FROM card WHERE number=? ", (account.number,))
            print("Balance:", cur.fetchone()[0])
            return "balance"
        elif choice == 2:
            account.balance = account.get_balance()
            print("Enter income:")
            income = int(input())  # check this input
            new_balance = account.deposit(income)
            account.update_balance()
            print('Income was added!')
        elif choice == 3:
            account.balance = account.get_balance()
            print("Enter card number:")
            recipient = str(input())
            if account.luhn_check(recipient):
                if db.card_exist(recipient):
                    print('Enter how much money you want to transfer:')
                    amount = int(input())
                    if amount <= account.balance:
                        account.make_transfer(recipient, amount)
                        print('success!')
                    else:
                        print("Not enough money!")
                else:
                    print("Such a card does not exist.")
            else:
                print("Probably you made a mistake in the card number. Please try again!")
        elif choice == 4:
            account.remove_card()
            print('The account has been closed')
            print_main_menu()
            return 'log out'
        elif choice == 5:
            print('You have successfully logged out!')
            print_main_menu()
            return 'log out'
        else:
            print('you should choose num from 0-5')
    except ValueError:
        print('Incorrect input')

def main():
    db = DB("example.s3db")
    db.create_table()
    account = Account()
    print_main_menu()

    not_exit = True
    while not_exit:
        try:
            choice = int(input())
            if choice == 1:
                c_n = account.create_card_num()
                print("Your card has been created\nYour card number:\n" + str(c_n))
                p_n = account.create_pin()
                print("Your card PIN:\n" + str(p_n) + "\n")
                db.insert(c_n, p_n, 0)
                print_main_menu()
            elif choice == 2:
                try:
                    card_num = str(input("Enter your card number:\n"))
                    entered_pin = str(input("Enter your PIN:\n"))
                    if db.check_pin(card_num, entered_pin):
                        print("You have successfully logged in!")
                        account.number = card_num
                        account.pin = entered_pin
                        account.update_balance()

                        not_quit = True
                        while not_quit:
                            #print_account_menu()#print log_in menu
                            choice=log_in_menu(db, account)
                            if choice == 'exit':
                                not_quit = False
                                not_exit = False
                            elif choice == 'log out':
                                not_quit = False
                    else:
                        print("Wrong card number or PIN!")
                        print_main_menu()
                except TypeError:
                    print('Error')
                    print_main_menu()
            elif choice == 0:
                print("Bye!")
                not_exit = False
            else:
                print('Your number should be 0-2')

        except TypeError:
            print('Type Error')

main()
conn.close()
