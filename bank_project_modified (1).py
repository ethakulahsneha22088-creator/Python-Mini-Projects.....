"""
PYTHON BANKING SYSTEM - OOP MINI PROJECT
Features:
- Create an account with a unique account number
- Login using username and password
- Deposit and withdraw with input validation
- Check balance
- View recent transaction history
- Logout and exit

Note: This is an educational demo. It stores data only while the program runs
and does not use secure password storage or a real banking service.
"""

from datetime import datetime
import random


class Account:
    def __init__(self, username, password, account_number):
        self.username = username
        self.password = password
        self.account_number = account_number
        self.balance = 0.0
        self.transactions = []
        self._record_transaction("Account created", 0.0)

    def _record_transaction(self, transaction_type, amount):
        self.transactions.append({
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance,
        })

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        self.balance += amount
        self._record_transaction("Deposit", amount)
        print(f"Successfully deposited: ₹{amount:.2f}")
        print(f"Available balance: ₹{self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self._record_transaction("Withdrawal", amount)
            print(f"Successfully withdrawn: ₹{amount:.2f}")
            print(f"Available balance: ₹{self.balance:.2f}")

    def show_balance(self):
        print(f"Account number: {self.account_number}")
        print(f"Account holder: {self.username}")
        print(f"Available balance: ₹{self.balance:.2f}")

    def show_mini_statement(self, limit=5):
        print("\n----------- MINI STATEMENT -----------")
        print(f"Account holder: {self.username}")
        print(f"Account number: {self.account_number}")
        print(f"Current balance: ₹{self.balance:.2f}")
        print("Recent transactions:")

        for item in self.transactions[-limit:][::-1]:
            print(
                f"{item['date']} | {item['type']} | "
                f"Amount: ₹{item['amount']:.2f} | "
                f"Balance: ₹{item['balance']:.2f}"
            )
        print("--------------------------------------")


class BankingSystem:
    def __init__(self):
        # Username is the key and Account object is the value.
        self.accounts = {}

    def _generate_account_number(self):
        existing_numbers = {
            account.account_number for account in self.accounts.values()
        }
        while True:
            number = str(random.randint(1000000000, 9999999999))
            if number not in existing_numbers:
                return number

    def create_account(self):
        username = input("Create username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return

        if username in self.accounts:
            print("That username already exists. Please choose another.")
            return

        password = input("Create password: ").strip()
        if len(password) < 4:
            print("For this demo, use a password of at least 4 characters.")
            return

        account_number = self._generate_account_number()
        self.accounts[username] = Account(username, password, account_number)

        print("\nAccount created successfully!")
        print(f"Your account number is: {account_number}")
        print("Please keep your account number safe.")

    def login(self):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        account = self.accounts.get(username)
        if account is None or account.password != password:
            print("Invalid username or password.")
            return

        print(f"\nWelcome, {account.username}!")
        self.account_menu(account)

    def account_menu(self, account):
        while True:
            print("\n---------- PYTHON BANK ----------")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check balance")
            print("4. Mini statement")
            print("5. Logout")

            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                amount = self._read_amount("Enter amount to deposit: ₹")
                if amount is not None:
                    account.deposit(amount)
            elif choice == "2":
                amount = self._read_amount("Enter amount to withdraw: ₹")
                if amount is not None:
                    account.withdraw(amount)
            elif choice == "3":
                account.show_balance()
            elif choice == "4":
                account.show_mini_statement()
            elif choice == "5":
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")

    @staticmethod
    def _read_amount(prompt):
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                print("Enter an amount greater than zero.")
                return None
            return amount
        except ValueError:
            print("Invalid amount. Enter a number, for example 250 or 250.50.")
            return None

    def run(self):
        while True:
            print("\n========== WELCOME TO PYTHON BANK ==========")
            print("1. Create account")
            print("2. Login")
            print("3. Exit")

            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Thank you for using Python Bank. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    bank = BankingSystem()
    bank.run()
