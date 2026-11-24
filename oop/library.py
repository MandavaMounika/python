
from abc import ABC, abstractmethod
from datetime import date, timedelta


class LibraryItem(ABC):
    total_items = 0

    def __init__(self, item_id, title, author):
        self.item_id = item_id
        self.title = title
        self.author = author
        self.__available = True

        LibraryItem.total_items += 1

    @property
    def available(self):
        return self.__available

    def set_availability(self, status):
        self.__available = status

    @abstractmethod
    def loan_period(self):
        pass

    @staticmethod
    def validate_title(title):
        return bool(title.strip())


class Book(LibraryItem):
    def loan_period(self):
        return 14


class Magazine(LibraryItem):
    def loan_period(self):
        return 7


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_items = {}


class Library:
    def __init__(self):
        self.items = {}
        self.members = {}

    @classmethod
    def total_items_added(cls):
        return LibraryItem.total_items

    def add_item(self):
        item_id = input("Item ID: ").strip()

        if not item_id or item_id in self.items:
            print("Invalid or duplicate item ID")
            return

        title = input("Title: ").strip()
        author = input("Author: ").strip()

        if not LibraryItem.validate_title(title) or not author:
            print("Title and author are required")
            return

        print("1. Book")
        print("2. Magazine")

        choice = input("Select type: ")

        if choice == "1":
            item = Book(item_id, title, author)
        elif choice == "2":
            item = Magazine(item_id, title, author)
        else:
            print("Invalid choice")
            return

        self.items[item_id] = item
        print("Item added successfully")

    def register_member(self):
        member_id = input("Member ID: ").strip()

        if not member_id or member_id in self.members:
            print("Invalid or duplicate member ID")
            return

        name = input("Member name: ").strip()

        if not name:
            print("Name is required")
            return

        self.members[member_id] = Member(member_id, name)
        print("Member registered")

    def borrow_item(self):
        member_id = input("Member ID: ").strip()
        item_id = input("Item ID: ").strip()

        member = self.members.get(member_id)
        item = self.items.get(item_id)

        if not member or not item:
            print("Member or item not found")
            return

        if not item.available:
            print("Item is unavailable")
            return

        if len(member.borrowed_items) >= 3:
            print("Maximum borrowing limit reached")
            return

        due_date = date.today() + timedelta(
            days=item.loan_period()
        )

        item.set_availability(False)
        member.borrowed_items[item_id] = due_date

        print("Borrowing successful")
        print("Due date:", due_date)

    def return_item(self):
        member_id = input("Member ID: ").strip()
        item_id = input("Item ID: ").strip()

        member = self.members.get(member_id)

        if not member or item_id not in member.borrowed_items:
            print("Borrowing record not found")
            return

        due_date = member.borrowed_items.pop(item_id)
        item = self.items[item_id]

        item.set_availability(True)

        overdue_days = max(
            0, (date.today() - due_date).days
        )

        fine = overdue_days * 5

        print("Book returned successfully")
        print("Overdue days:", overdue_days)
        print("Fine: Rs.", fine)

    def display_items(self):
        if not self.items:
            print("No library items available")
            return

        for item in self.items.values():
            status = "Available" if item.available else "Borrowed"

            print(
                item.item_id,
                item.title,
                item.author,
                status
            )

    def menu(self):
        while True:
            print("\n--- LIBRARY MANAGEMENT ---")
            print("1. Add Book/Magazine")
            print("2. Register Member")
            print("3. Borrow Item")
            print("4. Return Item")
            print("5. Display Items")
            print("6. Total Items")
            print("7. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.register_member()
            elif choice == "3":
                self.borrow_item()
            elif choice == "4":
                self.return_item()
            elif choice == "5":
                self.display_items()
            elif choice == "6":
                print("Total items:", self.total_items_added())
            elif choice == "7":
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    Library().menu()
