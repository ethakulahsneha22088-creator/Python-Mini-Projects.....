#ATM MACHINE MINI PROJECT
balance = 10000
correct_pin = 1234
print("----------------------------------------------------------------------")
print("Welcome to ATM")
print("----------------------------------------------------------------------")
pin = int(input("Enter your PIN:"))
if pin == correct_pin:
    while True:
        print("\n------------------- ATM Menu --------------------------")
        print("1.Check Balance")
        print("2.Deposit Money")
        print("3.Withdraw Money")
        print("4.Exit")
        print("----------------------------------------------------------------------")
        choice = int(input("Enter your choice:"))
        if choice == 1:
            print("Your current balance is:" , balance)
        elif choice == 2:
            amount = float(input("Enter deposit amount:"))
            if amount > 0:
                balance = balance + amount
                print("Amount deposited successfully")
                print("Updated balance:" , balance)
            else:
                print("Invalid deposit amount")
        elif choice == 3:
                amount = float(input("Enter withdrawal amount:"))
                if amount <= 0:
                    print("Invalid withdrawal amount")
                elif amount > balance:
                    print("Insufficient balance")
                else:
                     balance = balance - amount
                     print("Please collect your cash")
                     print("Updated balance:" , balance)
        elif choice == 4:
            print("Thankyou for using the ATM")
            print("Please collect your card")
            break
        else:
            print("Invalid choice.Please select 1 to 4.")                 
else:    
    print("Incorrect PIN")
    print("Transaction canclled")
