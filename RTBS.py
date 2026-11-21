import random


class User:
    def __init__(self, name, phone, username, password):
        self.name = name
        self.phone = phone
        self.username = username
        self.password = password


class Train:
    def __init__(self, train_no, train_name, source, destination, seats, fare):
        self.train_no = train_no
        self.train_name = train_name
        self.source = source
        self.destination = destination
        self.available_seats = seats
        self.fare = fare

    def display(self):
        print(f"{self.train_no} | {self.train_name} | "
              f"{self.source} to {self.destination} | "
              f"Seats: {self.available_seats} | Fare: Rs.{self.fare}")


class Passenger:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Ticket:
    def __init__(self, pnr, user, train, passengers, total_fare):
        self.pnr = pnr
        self.user = user
        self.train = train
        self.passengers = passengers
        self.total_fare = total_fare

    def display_ticket(self):
        print("\n========== RAILWAY E-TICKET ==========")
        print("PNR Number:", self.pnr)
        print("Booked By:", self.user.name)
        print("Phone:", self.user.phone)
        print("Train:", self.train.train_name)
        print("Route:", self.train.source, "to", self.train.destination)

        print("\nPassenger Details:")
        for i, passenger in enumerate(self.passengers, 1):
            print(i, passenger.name, passenger.age, passenger.gender)

        print("Total Passengers:", len(self.passengers))
        print("Total Fare: Rs.", self.total_fare)
        print("Status: CONFIRMED")
        print("======================================")


class RailwaySystem:
    def __init__(self):
        self.users = {}
        self.tickets = []

        self.trains = [
            Train("12711", "Pinakini Express", "Vijayawada", "Chennai", 5, 350),
            Train("12706", "Intercity Express", "Vijayawada", "Hyderabad", 6, 280),
            Train("17225", "Amaravati Express", "Vijayawada", "Bangalore", 4, 450),
            Train("12805", "Janmabhoomi Express", "Vijayawada", "Visakhapatnam", 8, 220)
        ]

    def register(self):
        print("\n--- CREATE ACCOUNT ---")
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        username = input("Create username: ")

        if username in self.users:
            print("Username already exists!")
            return

        password = input("Create password: ")

        self.users[username] = User(name, phone, username, password)
        print("Account created successfully!")

    def login(self):
        print("\n--- LOGIN ---")
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = self.users.get(username)

        if user and user.password == password:
            print("Login successful!")
            return user

        print("Invalid username or password!")
        return None

    def display_trains(self):
        print("\n--- AVAILABLE TRAINS ---")
        for train in self.trains:
            train.display()

    def book_ticket(self, user):
        self.display_trains()

        train_no = input("\nEnter train number: ")

        train = None
        for t in self.trains:
            if t.train_no == train_no:
                train = t
                break

        if train is None:
            print("Train not found!")
            return

        try:
            count = int(input("Enter number of passengers: "))

            if count <= 0 or count > train.available_seats:
                print("Invalid passenger count or insufficient seats!")
                return

            passengers = []

            for i in range(count):
                print("\nPassenger", i + 1)
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                gender = input("Enter gender: ")

                if age <= 0:
                    print("Invalid age!")
                    return

                passengers.append(Passenger(name, age, gender))

            total_fare = count * train.fare
            pnr = str(random.randint(1000000000, 9999999999))

            ticket = Ticket(pnr, user, train, passengers, total_fare)

            train.available_seats -= count
            self.tickets.append(ticket)

            print("\nTicket booked successfully!")
            ticket.display_ticket()

        except ValueError:
            print("Please enter valid numerical values!")

    def view_bookings(self, user):
        found = False

        for ticket in self.tickets:
            if ticket.user.username == user.username:
                ticket.display_ticket()
                found = True

        if not found:
            print("No bookings found!")

    def search_ticket(self):
        pnr = input("Enter PNR number: ")

        for ticket in self.tickets:
            if ticket.pnr == pnr:
                ticket.display_ticket()
                return

        print("Ticket not found!")

    def user_menu(self, user):
        while True:
            print("\n--- RAILWAY MENU ---")
            print("1. View Trains")
            print("2. Book Ticket")
            print("3. View My Bookings")
            print("4. Search Ticket")
            print("5. Logout")

            choice = input("Enter choice: ")

            if choice == "1":
                self.display_trains()

            elif choice == "2":
                self.book_ticket(user)

            elif choice == "3":
                self.view_bookings(user)

            elif choice == "4":
                self.search_ticket()

            elif choice == "5":
                print("Logged out successfully!")
                break

            else:
                print("Invalid choice!")

    def run(self):
        while True:
            print("\n================================")
            print(" RAILWAY TICKET BOOKING SYSTEM")
            print("================================")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.register()

            elif choice == "2":
                user = self.login()
                if user:
                    self.user_menu(user)

            elif choice == "3":
                print("Thank you!")
                break

            else:
                print("Invalid choice!")


if __name__ == "__main__":
    railway = RailwaySystem()
    railway.run()