
from abc import ABC, abstractmethod
from datetime import date, timedelta


class Vehicle(ABC):
    def __init__(self, vehicle_id, model):
        self.vehicle_id = vehicle_id
        self.model = model
        self.__available = True

    @property
    def available(self):
        return self.__available

    def set_availability(self, status):
        self.__available = status

    @abstractmethod
    def calculate_rent(self, days):
        pass


class Car(Vehicle):
    def calculate_rent(self, days):
        return days * 1500


class Bike(Vehicle):
    def calculate_rent(self, days):
        return days * 500


class Truck(Vehicle):
    def calculate_rent(self, days):
        return days * 3000


class RentalSystem:
    def __init__(self):
        self.vehicles = {}
        self.rentals = {}

    def add_vehicle(self):
        vehicle_id = input("Vehicle ID: ").strip()

        if not vehicle_id or vehicle_id in self.vehicles:
            print("Invalid or duplicate vehicle ID")
            return

        model = input("Vehicle model: ").strip()

        if not model:
            print("Model cannot be empty")
            return

        print("1. Car")
        print("2. Bike")
        print("3. Truck")

        choice = input("Select type: ")

        vehicle_types = {
            "1": Car,
            "2": Bike,
            "3": Truck
        }

        vehicle_class = vehicle_types.get(choice)

        if vehicle_class is None:
            print("Invalid vehicle type")
            return

        self.vehicles[vehicle_id] = vehicle_class(
            vehicle_id, model
        )

        print("Vehicle added successfully")

    def rent_vehicle(self):
        vehicle_id = input("Vehicle ID: ").strip()

        vehicle = self.vehicles.get(vehicle_id)

        if not vehicle:
            print("Vehicle not found")
            return

        if not vehicle.available:
            print("Vehicle already rented")
            return

        try:
            days = int(input("Rental days: "))

            if days <= 0:
                raise ValueError("Days must be positive")

            customer = input("Customer name: ").strip()

            if not customer:
                print("Customer name is required")
                return

            amount = vehicle.calculate_rent(days)
            due_date = date.today() + timedelta(days=days)

            vehicle.set_availability(False)

            self.rentals[vehicle_id] = {
                "customer": customer,
                "days": days,
                "amount": amount,
                "due_date": due_date
            }

            print("Rental successful")
            print("Rental cost:", amount)
            print("Due date:", due_date)

        except ValueError as error:
            print("Error:", error)

    def return_vehicle(self):
        vehicle_id = input("Vehicle ID: ").strip()

        if vehicle_id not in self.rentals:
            print("No active rental found")
            return

        rental = self.rentals.pop(vehicle_id)
        vehicle = self.vehicles[vehicle_id]

        vehicle.set_availability(True)

        overdue = max(
            0, (date.today() - rental["due_date"]).days
        )

        fine = overdue * 200

        print("Vehicle returned")
        print("Overdue days:", overdue)
        print("Late fine:", fine)
        print("Total amount:", rental["amount"] + fine)

    def display_vehicles(self):
        for vehicle in self.vehicles.values():
            status = "Available" if vehicle.available else "Rented"

            print(
                vehicle.vehicle_id,
                vehicle.model,
                status
            )

    def menu(self):
        while True:
            print("\n--- VEHICLE RENTAL ---")
            print("1. Add Vehicle")
            print("2. Display Vehicles")
            print("3. Rent Vehicle")
            print("4. Return Vehicle")
            print("5. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_vehicle()
            elif choice == "2":
                self.display_vehicles()
            elif choice == "3":
                self.rent_vehicle()
            elif choice == "4":
                self.return_vehicle()
            elif choice == "5":
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    RentalSystem().menu()
