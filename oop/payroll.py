
class Employee:
    company = "Tech Solutions"

    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name

    def calculate_salary(self):
        raise NotImplementedError

    def display(self):
        print("\nEmployee ID:", self.emp_id)
        print("Name:", self.name)
        print("Salary:", self.calculate_salary())


class FullTimeEmployee(Employee):
    def __init__(self, emp_id, name, basic, bonus):
        super().__init__(emp_id, name)
        self.basic = basic
        self.bonus = bonus

    def calculate_salary(self):
        return self.basic + self.bonus


class Manager(FullTimeEmployee):
    def __init__(self, emp_id, name, basic, bonus, allowance):
        super().__init__(emp_id, name, basic, bonus)
        self.allowance = allowance

    def calculate_salary(self):
        return super().calculate_salary() + self.allowance


class ContractEmployee(Employee):
    def __init__(self, emp_id, name, hours, hourly_rate):
        super().__init__(emp_id, name)
        self.hours = hours
        self.hourly_rate = hourly_rate

    def calculate_salary(self):
        return self.hours * self.hourly_rate


class Payroll:
    def __init__(self):
        self.employees = []

    def add_employee(self):
        try:
            emp_id = input("Employee ID: ").strip()

            if any(e.emp_id == emp_id for e in self.employees):
                print("Employee ID already exists")
                return

            name = input("Employee name: ").strip()

            if not emp_id or not name:
                print("ID and name are required")
                return

            print("1. Full Time")
            print("2. Manager")
            print("3. Contract")

            choice = input("Employee type: ")

            if choice == "1":
                basic = float(input("Basic salary: "))
                bonus = float(input("Bonus: "))

                employee = FullTimeEmployee(
                    emp_id, name, basic, bonus
                )

            elif choice == "2":
                basic = float(input("Basic salary: "))
                bonus = float(input("Bonus: "))
                allowance = float(input("Allowance: "))

                employee = Manager(
                    emp_id, name, basic, bonus, allowance
                )

            elif choice == "3":
                hours = float(input("Working hours: "))
                rate = float(input("Hourly rate: "))

                if hours < 0 or rate < 0:
                    raise ValueError("Values cannot be negative")

                employee = ContractEmployee(
                    emp_id, name, hours, rate
                )

            else:
                print("Invalid employee type")
                return

            self.employees.append(employee)
            print("Employee added!")

        except ValueError as error:
            print("Invalid input:", error)

    def generate_payroll(self):
        if not self.employees:
            print("No employees found")
            return

        total = 0

        for employee in self.employees:
            employee.display()
            total += employee.calculate_salary()

        print("\nTotal Payroll:", total)

    def search_employee(self):
        emp_id = input("Enter employee ID: ")

        for employee in self.employees:
            if employee.emp_id == emp_id:
                employee.display()
                return

        print("Employee not found")

    def sort_by_salary(self):
        ranked = sorted(
            self.employees,
            key=lambda e: e.calculate_salary(),
            reverse=True
        )

        for employee in ranked:
            print(employee.name, employee.calculate_salary())

    def menu(self):
        while True:
            print("\n--- EMPLOYEE PAYROLL ---")
            print("1. Add Employee")
            print("2. Generate Payroll")
            print("3. Search Employee")
            print("4. Sort By Salary")
            print("5. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.generate_payroll()
            elif choice == "3":
                self.search_employee()
            elif choice == "4":
                self.sort_by_salary()
            elif choice == "5":
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    Payroll().menu()
