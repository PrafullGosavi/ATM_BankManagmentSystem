import mysql.connector

class Atm:
    def __init__(self):
        self.pin = ''
        self.balance = 0

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pass@123",
            database="atm"
        )
        self.cursor = self.db.cursor()

        self.menu()

    def menu(self):
        user_input = input('''how would you like to proceed?
              1. Enter 1 to create a pin.
              2. Enter 2 to deposit.
              3. Enter 3 to withdraw.
              4. Enter 4 to check balance.
              5. Enter 5 to exit
''')

        if user_input == '1':
            self.create_pin()
        elif user_input == '2':
            self.authenticate_and_proceed(self.deposit)
        elif user_input == '3':
            self.authenticate_and_proceed(self.withdraw)
        elif user_input == '4':
            self.authenticate_and_proceed(self.check_balance)
        else:
            print("You Have EXIT")
            print("THANK YOU USER.....!",self.pin)

            self.db.close()

    def create_pin(self):
        self.pin = input("Enter The Pin: ")
        if len(self.pin) <= 10:
            print("Pin Set Successfully")
            self.cursor.execute("INSERT INTO users (pin, balance) VALUES (%s, %s)", (self.pin, self.balance))
            self.db.commit()
            user_input = input("You need to deposit money, so click 1. Otherwise, enter 2: ")
            if user_input == '1':
                self.deposit()
            else:
                print("You're Welcome.....!")
        else:
            print("Pin Length Should Be Smaller. Enter the pin again.")
            self.create_pin()

    def authenticate_and_proceed(self, action):
        self.pin = input("Enter The Pin: ")
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.pin,))
        result = self.cursor.fetchone()
        if result:
            self.balance = result[0]
            print("Pin Authentication Successful")
            action()
        else:
            print("The pin you have entered is invalid. Please try again.")
            self.menu()

    def deposit(self):
        amount = int(input("Enter the amount to deposit: "))
        self.balance += amount
        self.cursor.execute("UPDATE users SET balance = %s WHERE pin = %s", (self.balance, self.pin))
        self.db.commit()
        print("Deposit Successful")
        self.post_transaction_menu()

    def withdraw(self):
        amount = int(input("Enter the amount to withdraw: "))
        if amount <= self.balance:
            self.balance -= amount
            self.cursor.execute("UPDATE users SET balance = %s WHERE pin = %s", (self.balance, self.pin))
            self.db.commit()
            print("Operation Successful. Your Remaining Balance is", self.balance)
        else:
            print("Insufficient Balance. Try again.")
        self.post_transaction_menu()

    def check_balance(self):
        print("Your Balance is", self.balance)
        user_input = input("enter 1 to deposite enter 2 to withdraw enter 3 to for menu")
        if user_input == '1':
            self.deposit()
        elif user_input == '2':
            self.withdraw()
        else:
            self.menu()
        

    def post_transaction_menu(self):
        user_input = input('''If you want to check your balance, click 1. 
                              If you want to withdraw, click 2. 
                              If you don't want to do anything, click 3: ''')
        if user_input == '1':
            self.check_balance()
        elif user_input == '2':
            self.withdraw()
        else:
            print("Thank you.")
            self.menu()

# Replace 'your_host', 'your_username', 'your_password', and 'your_database' with your MySQL database credentials
sbi = Atm()
