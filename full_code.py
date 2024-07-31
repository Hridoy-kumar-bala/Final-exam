class Account:
    account_number =100
    account_Type = {
        'savings','current'
    }


    def __init__(self,name, email, address,account_Type) -> None:
        if account_Type not in Account.account_Type:
            raise ValueError(f"Invalid account type. Choose from {Account.account_Type}")
        self.account_number =Account.account_number+1
        self.name = name
        self.email =email
        self.address = address
        self.account_Type =account_Type
        self.balance =0
        # self.loans = 0
        self.loans=0
        self.transactions =[]
        

    def deposit(self,amount):
        if amount>0:
            self.balance +=amount
            self.transactions.append(
                {
                    'type': 'Deposit',
                    'amount':amount,
                    'balance': self.balance
                }
            )
            return f"{amount} deposited successful. New balance: {self.balance}"
        else:
            return f"Deposit amount must be positive."

    def withdraw(self,amount):    
        if amount<=0:
            return f"Withdrawal amount must be positive"
        elif amount>self.balance:
            return f"Withdrawal amount exceeded"
        else:
            self.balance -=amount
            self.transactions.append({
                'type': 'Withdrawal',
                'amount': amount,
                'balance': self.balance
            })

            return f"{amount} withdraw successfully.new balance is {self.balance}"


    def available_balance(self):
        return self.balance
    def transaction_history(self):
        if self.transactions:
            history =""
            for transaction in self.transactions:
                history += f"{transaction['type']}: {transaction['amount']}, Balance after transaction: {transaction['balance']}\n"
            return history
        else:
            return f"No transactions recorded"
        # return self.transactions


    def take_loan(self, amount):
        if self.loans < 2:
            # self.loan += amount
            self.balance += amount
            self.transactions.append({
                'type': 'Loan',
                'amount': amount,
                'balance': self.balance
            })
            # self.transactions.append(f"Loan taken {amount}")
            self.loans += 1
            return f"Loan of {amount} taken successfully.New balance {self.balance}"
        else:
            return f"Loan limit reached"


class Bank:
    def __init__(self):
        self.accounts = {}
        self.loan_feature = True

    def create_account(self, name, email, address, account_type):
        account = Account(name, email, address, account_type)
        self.accounts[account.account_number] = account
        return account.account_number

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f"Account {account_number} deleted."
        return f"Account does not exist."


    def user_accounts (self):
        return [account.account_number for account in self.accounts.values()]

    def total_balance(self):
        return sum(account.balance for account in self.accounts.values())


    # def total_loan_amount(self):
    #     if not self.loan_feature:
    #         return f"Loan feature is turned off."
    #     total_loan_amount = 0
    #     for account in self.accounts.values():
    #         for loans in account.loans:
    #             total_loan_amount += loans
    #     return f"your total loan amount is {total_loan_amount}"
    def total_loan_amount(self):
        if not self.loan_feature:
            return "Loan feature is turned off."
    
        total_loan_amount = 0
        for account in self.accounts.values():
            # total_loan_amount += sum(account.loans)
            total_loan_amount = sum(account.balance - account.transactions[0]['balance'] for account in self.accounts.values() if account.loans > 0)
    
        return f"Your total loan amount is {total_loan_amount}."


    def set_loan_feature(self, status):
        self.loan_feature = status
        if self.loan_feature:
            return "Loan enabled."
        else:
            return "Loan disabled."


    def transfer_amount(self, from_account, to_account, amount):
        if from_account not in self.accounts or to_account not in self.accounts:
            return "Account does not exist."
        if self.accounts[from_account].balance < amount:
            return "Insufficient funds."
        self.accounts[from_account].balance -= amount
        self.accounts[to_account].balance += amount
        self.accounts[from_account].transactions.append(f"Transferred {amount} to {to_account}")
        self.accounts[to_account].transactions.append(f"Received {amount} from {from_account}")
        return f"Transferred {amount} from {from_account} to {to_account}."



class User:
    def __init__(self, bank):
        self.bank = bank
        
    def create_account(self, name, email, address, account_type):
        return self.bank.create_account(name, email, address, account_type)

    def deposit(self, account_number, amount):
        if account_number in self.bank.accounts:
            return self.bank.accounts[account_number].deposit(amount)
        return "Account does not exist."


    def withdraw(self, account_number, amount):
        if account_number in self.bank.accounts:    
            return self.bank.accounts[account_number].withdraw(amount)
        return "Account does not exist."

    def available_balance(self, account_number):
        if account_number in self.bank.accounts:
            return self.bank.accounts[account_number].available_balance()
        return "Account does not exist."

    def transaction_history(self, account_number):
        if account_number in self.bank.accounts:
            return self.bank.accounts[account_number].transaction_history()
        return "Account does not exist."

    def take_loan(self, account_number,amount):
        if account_number in self.bank.accounts:
            # if amount>0 and amount<=self.bank.accounts[account_number].balance:
            #     self.bank.accounts[account_number].balance+=amount
            return self.bank.accounts[account_number].take_loan(amount)
        return "Account does not exist."

    def transfer_amount(self, from_account, to_account, amount):
        return self.bank.transfer_amount(from_account, to_account, amount)

    def __repr__(self) -> str:
        return f"Account Number: {self.account_number}\n Name:{self.name}\n Email: {self.email}\n Address: {self.address}\n Account Type Name: {self.account_Type} Balance:{self.balance}"
    



# from user import User
class Admin(User):
    def __init__(self, bank):
        super().__init__(bank)

    def delete_account(self, account_number):
        return self.bank.delete_account(account_number)

    def user_accounts(self):
        return self.bank.user_accounts()

    def total_balance(self):
        return self.bank.total_balance()

    def total_loan_amount(self):
        return self.bank.total_loan_amount()

    def set_loan_feature(self,status):
        return self.bank.set_loan_feature(status)


# from user import User
# from admin import Admin
# from account import Account,Bank

bank =Bank()
admin =Admin(bank)
user = User(bank)



# account_number = user.create_account("John Doe", "john@example.com", "123 Main St", "savings")
# print("Account created:", account_number)
# print(user.available_balance(account_number))
# print(user.deposit(account_number, 1000))
# print(user.available_balance(account_number))
# print(user.withdraw(account_number, 500))
# print(user.available_balance(account_number))
# print(user.take_loan(account_number, 400))
# print(user.available_balance(account_number))
# print(user.transaction_history(account_number))

# # Admin operations
# print(admin.user_accounts())
# print(admin.total_balance())
# print(admin.total_loan_amount())
# print(admin.set_loan_feature(False))
# print(admin.delete_account(account_number))
# print(admin.user_accounts())
# print(admin.set_loan_feature(True))
def user_operation():
    print("USER OPERATION:\n")
    print("1. CREATE ACCOUNT.")
    print("2. Deposit Balance")
    print("3.Withdraw Balance")
    print("4. Check balance")
    print("5. Take loan")
    print("6. Transaction history\n")
    # print("7. Exit")
    choice = int(input("Enter your choice:"))
    if choice == 1:
        print("CREATE AN ACCOUNT:\n")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        account_type = input("Enter account type (savings/checking): ")
        account_number = user.create_account(name,email,address,account_type)
        print("\nAccount create: ",account_number)
    elif choice ==2:
        print("Deposit Balance:\n")
        account_number = input("Enter your account number:")
        amount =float(input("Enter your amount:"))
        print(user.deposit(account_number, amount))

    elif choice ==3:
        print("Withdraw Balance:\n")
        account_number = input("Enter your account number:")
        amount =float(input("Enter your amount:"))
        print(user.withdraw(account_number, amount))
    elif choice ==4:
        print("Check balance:\n")
        account_number = input("Enter your account number:")
        print(user.available_balance(account_number))
    elif choice ==5:
        print("Take loan:\n")
        account_number = input("Enter your account number:")
        amount =float(input("Enter your amount:"))
        print(user.take_loan(account_number,amount))
    
    elif choice == 6:
        print("Transaction history:\n")
        account_number = input("Enter your account number:")
        print(user.transaction_history(account_number))
    else:
        print("Invalid choice")

def admin_panel():
    print("Admin Panel:")
    print("1.User accounts")
    print("2.Total balance")
    print("3.Total loan amount")
    print("4.Enable/disable loan feature")
    print("5.Delete account\n")


    choice = input("Choose an operation: ")

    if choice == '1':
        print(admin.user_accounts())
    elif choice == '2':
        print(admin.total_balance())
    elif choice == '3':
        print(admin.total_loan_amount())
    elif choice == '4':
        status = input("Enable loan feature(True/False): ")
        print(admin.set_loan_feature(status))
    elif choice == '5':
        account_number = input("Enter account number to delete: ")
        print(admin.delete_account(account_number))
    else:
        print("Invalid choice")

while(True):
    print("Main Menu:")
    print("1. User Operation")
    print("2. Admin panel")
    print("3. Exit\n")
    main_choice = input("Choose option: ")

    if main_choice == '1':
        user_operation()
    elif main_choice == '2':
        admin_panel()
    elif main_choice == '3':
        break
    else:
        print("Invalid choice")


