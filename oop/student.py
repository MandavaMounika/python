
class Student:
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.__marks = marks

    @property
    def marks(self):
        return self.__marks.copy()

    def calculate_total(self):
        return sum(self.__marks.values())

    def calculate_average(self):
        return self.calculate_total() / len(self.__marks)

    def calculate_grade(self):
        avg = self.calculate_average()

        if avg >= 90:
            return "A"
        elif avg >= 75:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        return "Fail"

    def display(self):
        print("\nStudent ID:", self.student_id)
        print("Name:", self.name)
        print("Marks:", self.__marks)
        print("Total:", self.calculate_total())
        print("Average:", round(self.calculate_average(), 2))
        print("Grade:", self.calculate_grade())


class StudentManagement:
    def __init__(self):
        self.students = {}

    def add_student(self):
        try:
            sid = input("Enter student ID: ").strip()

            if not sid or sid in self.students:
                print("Invalid or duplicate ID!")
                return

            name = input("Enter student name: ").strip()

            if not name:
                print("Name cannot be empty")
                return

            subjects = {}

            count = int(input("Number of subjects: "))

            if count <= 0:
                print("Enter at least one subject")
                return

            for i in range(count):
                subject = input(f"Subject {i+1}: ").strip()

                if not subject or subject in subjects:
                    print("Invalid or duplicate subject")
                    return

                mark = float(input(f"Marks in {subject}: "))

                if not 0 <= mark <= 100:
                    print("Marks must be between 0 and 100")
                    return

                subjects[subject] = mark

            self.students[sid] = Student(sid, name, subjects)
            print("Student added successfully!")

        except ValueError:
            print("Please enter valid numerical values")

    def display_all(self):
        if not self.students:
            print("No student records found")
            return

        for student in self.students.values():
            student.display()

    def search_student(self):
        sid = input("Enter student ID to search: ").strip()

        student = self.students.get(sid)

        if student:
            student.display()
        else:
            print("Student not found")

    def delete_student(self):
        sid = input("Enter student ID to delete: ").strip()

        if self.students.pop(sid, None):
            print("Student deleted")
        else:
            print("Student not found")

    def show_topper(self):
        if not self.students:
            print("No records available")
            return

        topper = max(
            self.students.values(),
            key=lambda s: s.calculate_average()
        )

        print("Class Topper:")
        topper.display()

    def rank_students(self):
        ranked = sorted(
            self.students.values(),
            key=lambda s: s.calculate_average(),
            reverse=True
        )

        for rank, student in enumerate(ranked, start=1):
            print(rank, student.name,
                  round(student.calculate_average(), 2))

    def menu(self):
        while True:
            print("\n--- STUDENT MANAGEMENT ---")
            print("1. Add Student")
            print("2. Display All")
            print("3. Search Student")
            print("4. Delete Student")
            print("5. Find Topper")
            print("6. Rank Students")
            print("7. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.display_all()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                self.show_topper()
            elif choice == "6":
                self.rank_students()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice")


app = StudentManagement()
app.menu()
