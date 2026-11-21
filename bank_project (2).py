from datetime import datetime
from decimal import Decimal, InvalidOperation
import secrets


class Account:
    """One customer's bank account."""

    def __init__(self, account_holder, pin, opening_balance=Decimal("0.00")):
        self.account_holder = account_holder
        self.pin = pin
        self.account_number = self._generate_account_number()
        self.balance = Decimal(opening_balance).quantize(Decimal("0.01"))
        self.transactions = []
        self._record_transaction("Account created", self.balance)

    @staticmethod
    def _generate_account_number():
        # Demo-only account number generation.
        return str(secrets.randbelow(9_000_000_000) + 1_000_000_000)

    def _record_transaction(self, transaction_type, amount):
        timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        self.transactions.append({
            "time": timestamp,
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance,
        })

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return False
        self.balance += amount
        self._record_transaction("Deposit", amount)
        print(f"Rs. {amount:.2f} deposited successfully.")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return False
        if amount > self.balance:
            print("Insufficient balance.")
            return False
        self.balance -= amount
        self._record_transaction("Withdrawal", amount)
        print(f"Rs. {amount:.2f} withdrawn successfully.")
        return True

    def show_mini_statement(self, limit=5):
        print("\n" + "=" * 76)
        print(f"MINI STATEMENT — {self.account_holder} | A/C: {self.account_number}")
        print("-" * 76)
        for item in self.transactions[-limit:]:
            print(
                f"{item['time']} | {item['type']} | "
                f"Rs. {item['amount']:.2f} | Balance: Rs. {item['balance']:.2f}"
            )
        print("=" * 76)


class BankingSystem:
    """Simple menu-driven banking system for Python practice."""

    def __init__(self):
        self.accounts = {}
        self.create_demo_account()

    def create_demo_account(self):
        account = Account("Demo User", "1234", Decimal("5000.00"))
        self.accounts[account.account_number] = account
        print("\nDEMO ACCOUNT CREATED")
        print(f"Account holder : {account.account_holder}")
        print(f"Account number : {account.account_number}")
        print("Demo PIN       : 1234")
        print(f"Opening balance: Rs. {account.balance:.2f}")
        print("Keep this account number for this run of the program.")

    @staticmethod
    def read_amount(prompt):
        raw_value = input(prompt).strip()
        try:
            amount = Decimal(raw_value)
            if not amount.is_finite():
                raise InvalidOperation
            return amount.quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            print("Invalid amount. Enter a number such as 250 or 250.50.")
            return None

    def login(self):
        account_number = input("Enter account number: ").strip()
        account = self.accounts.get(account_number)
        if account is None:
            print("Account not found.")
            return None

        pin = input("Enter PIN: ").strip()
        if pin != account.pin:
            print("Incorrect PIN.")
            return None

        print(f"\nLogin successful. Welcome, {account.account_holder}!")
        return account

    @staticmethod
    def show_balance(account):
        print(f"Available balance: Rs. {account.balance:.2f}")

    def account_menu(self, account):
        while True:
            print("\n" + "=" * 34)
            print("           BANK MENU")
            print("=" * 34)
            print("1. Check balance")
            print("2. Deposit money")
            print("3. Withdraw money")
            print("4. Mini statement")
            print("5. Logout")
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self.show_balance(account)
            elif choice == "2":
                amount = self.read_amount("Enter deposit amount (Rs.): ")
                if amount is not None:
                    account.deposit(amount)
            elif choice == "3":
                amount = self.read_amount("Enter withdrawal amount (Rs.): ")
                if amount is not None:
                    account.withdraw(amount)
            elif choice == "4":
                account.show_mini_statement()
            elif choice == "5":
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please select 1 to 5.")

    def run(self):
        print("\n*** PYTHON BANKING SYSTEM ***")
        while True:
            print("\n1. Login")
            print("2. Exit")
            choice = input("Enter your choice (1-2): ").strip()

            if choice == "1":
                account = self.login()
                if account is not None:
                    self.account_menu(account)
            elif choice == "2":
                print("Thank you for using the Banking System.")
                break
            else:
                print("Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    BankingSystem().run()
