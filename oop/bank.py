
class BankAccount:
    bank_name = "Python National Bank"

    def __init__(self, holder, account_number, balance=0):
        if balance < 0:
            raise ValueError("Balance cannot be negative")

        self.holder = holder
        self.account_number = account_number
        self.__balance = balance
        self.transactions = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Enter a positive amount")

        self.__balance += amount
        self.transactions.append(
            f"Deposited: Rs.{amount:.2f}"
        )
        print("Deposit successful!")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Enter a positive amount")

        if amount > self.__balance:
            raise ValueError("Insufficient balance")

        self.__balance -= amount
        self.transactions.append(
            f"Withdrawn: Rs.{amount:.2f}"
        )
        print("Withdrawal successful!")

    def transfer(self, receiver, amount):
        if self.account_number == receiver.account_number:
            raise ValueError("Cannot transfer to same account")

        self.withdraw(amount)
        receiver.deposit(amount)

        self.transactions.append(
            f"Transferred Rs.{amount:.2f} to {receiver.holder}"
        )

    def show_transactions(self):
        if not self.transactions:
            print("No transactions available")
            return

        for transaction in self.transactions:
            print(transaction)

    def display(self):
        print("\nAccount Holder:", self.holder)
        print("Account Number:", self.account_number)
        print("Balance:", self.balance)


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Account holder name: ").strip()
        acc_no = input("Account number: ").strip()

        if not name or not acc_no:
            print("Name and account number are required")
            return

        if acc_no in self.accounts:
            print("Account already exists")
            return

        try:
            balance = float(input("Initial deposit: Rs."))

            account = BankAccount(name, acc_no, balance)
            self.accounts[acc_no] = account

            print("Account created successfully!")

        except ValueError as error:
            print("Error:", error)

    def get_account(self):
        acc_no = input("Enter account number: ").strip()
        account = self.accounts.get(acc_no)

        if account is None:
            print("Account not found")

        return account

    def deposit_money(self):
        account = self.get_account()

        if account:
            try:
                amount = float(input("Deposit amount: "))
                account.deposit(amount)
            except ValueError as error:
                print("Error:", error)

    def withdraw_money(self):
        account = self.get_account()

        if account:
            try:
                amount = float(input("Withdrawal amount: "))
                account.withdraw(amount)
            except ValueError as error:
                print("Error:", error)

    def transfer_money(self):
        sender = self.get_account()

        if not sender:
            return

        receiver_no = input("Receiver account number: ").strip()
        receiver = self.accounts.get(receiver_no)

        if not receiver:
            print("Receiver account not found")
            return

        try:
            amount = float(input("Transfer amount: Rs."))
            sender.transfer(receiver, amount)
            print("Transfer successful!")

        except ValueError as error:
            print("Transfer failed:", error)

    def menu(self):
        while True:
            print("\n--- BANK MANAGEMENT ---")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. Check Balance")
            print("6. Transactions")
            print("7. Exit")

            choice = input("Choose option: ")

            if choice == "1":
                self.create_account()

            elif choice == "2":
                self.deposit_money()

            elif choice == "3":
                self.withdraw_money()

            elif choice == "4":
                self.transfer_money()

            elif choice == "5":
                account = self.get_account()
                if account:
                    account.display()

            elif choice == "6":
                account = self.get_account()
                if account:
                    account.show_transactions()

            elif choice == "7":
                break

            else:
                print("Invalid option")


if __name__ == "__main__":
    Bank().menu()
