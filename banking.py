# Write your code here
import sqlite3
from random import sample, randint



class Card:
    id = 0
    number = ''
    pin = ''
    balance = 0

class Account(Card):
    def __init__(self):
        self.id = randint(100000000, 999999999) * 10
        self.number = self.luhn(str(4000000000000000 + self.id))
        self.pin = ''.join(map(str, sample(range(1, 9), 4)))
    @staticmethod
    def luhn(num):
        num = num[:-1]
        list_num = []
        for c, n in enumerate(num, 1):
            n = int(n)
            if c % 2:
                n *= 2
            list_num.append(n-9 if n > 9 else n)
        n = sum(list_num) % 10
        return num + str(10 - n if n else n)
class Menu:
    def __init__(self):
        self.__choice = '0'
    def __repr__(self):
        return self.__choice
    def __eq__(self, other):
        return True if self.__choice == other else False
    @staticmethod
    def __show_main_menu():
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
    @staticmethod
    def __show_account_menu():
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

    def show_and_get_choice(self):
        if self.__choice.startswith('2'):
            self.__show_account_menu()
            self.__choice = f'{self.__choice[0]}.{input()}'
        else:
            self.__show_main_menu()
            self.__choice = input()
    def back_to_main(self):
        self.__choice = '0'
class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("card.s3db")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS card 
            (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
    #def __del__(self):
        #self.conn.close()

    def add(self, account):
        self.cursor.execute(f'INSERT INTO card VALUES ({account.id}, {account.number}, {account.pin}, "0")''')
        self.conn.commit()
        self.cursor.execute(f'INSERT INTO card VALUES ({account.id}, {account.number}, {account.pin}, "0")')
        self.conn.commit()


    def get(self, number):
        acc = self.cursor.execute(f'SELECT * FROM card WHERE number={number}').fetchone()
        self.conn.commit()
        if acc:
            account = Account()
            account.id, account.number, account.pin, account.balance = acc
            return account
        return None
    def get_all(self):
        return self.cursor.execute(f'SELECT * FROM card')



    def set_balance(self, number, balance):
        self.cursor.execute(f'UPDATE card SET balance = {balance} WHERE number = {number}')
        self.conn.commit()


    def delete(self, number):
        self.cursor.execute(f'DELETE FROM card WHERE number = {number}')
        self.conn.commit()
        self.conn.close()


class Banking:
    def __init__(self):
        self.menu = Menu()
        self.db = DataBase()
        self.current_account = None
    def create_account(self):
        account = Account()
        self.db.add(account)
        print('\nYour card has been created')
        print('Your card number:')
        print(f'{account.number}')
        print('Your card PIN:')
        print(f'{account.pin}\n')

    def login(self):
        print('\nEnter your card number:')
        number = input()
        print('Enter your PIN:')
        pin = input()
        account = self.db.get(number)
        if account:
            if account.pin == pin:
                print('\nYou have successfully logged in!\n')
                self.current_account = account
                return
        print('\nWrong card number or PIN!\n')
        self.menu.back_to_main()
    def show_balance(self):
        print(f'\nBalance: {self.current_account.balance}\n')

    def add_income(self):
        print('\nEnter income:')
        income = int(input())
        self.current_account.balance += income
        self.db.set_balance(self.current_account.number, self.current_account.balance)
        print('Income was added!\n')

    def transfer(self):
        print('\nTransfer\nEnter card number:')
        number = input()
        if number == Account.number:
            print("You can't transfer money to the same account!")
        elif number == Account.luhn(number):
            account = self.db.get(number)
            if account:
                print('Enter how much money you want to transfer:')
                transfer = int(input())
                if self.current_account.balance >= transfer:
                    self.db.set_balance(number, account.balance + transfer)
                    print(f'>>> num: {self.current_account.number} bal: {self.current_account.balance}')
                    self.current_account.balance -= transfer
                    self.db.set_balance(self.current_account.number, self.current_account.balance)
                    print(f'>>> num: {self.current_account.number} bal: {self.current_account.balance}')
                    print('Success!\n')
                else:
                    print('Not enough money!\n')
            else:
                print('Such a card does not exist.\n')
        else:
            print('Probably you made mistake in the card number. Please try again!\n')

    def close_account(self):
        self.db.delete(self.current_account.number)
        self.db.conn.commit()
        self.db.conn.close()
        print('\nThe account has been closed!\n')

    def log_out(self):
        print('\nYou have successfully logged out!\n')
        self.menu.back_to_main()
    def run(self):
        while True:
            self.menu.show_and_get_choice()
            if self.menu == '1':
                self.create_account()
            elif self.menu == '2':
                self.login()
            elif self.menu == '2.1':
                self.show_balance()
            elif self.menu == '2.2':
                self.add_income()
            elif self.menu == '2.3':
                self.transfer()
            elif self.menu == '2.4':
                self.close_account()
            elif self.menu == '2.5':
                self.log_out()
            else:
                print('\nBye!')
                break
if __name__ == '__main__':
    banking = Banking()
    banking.run()



