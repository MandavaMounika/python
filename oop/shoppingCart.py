
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"

    def __add__(self, other):
        return self.price + other.price


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_product(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        current = self.items.get(product.product_id, 0)

        if current + quantity > product.stock:
            raise ValueError("Insufficient stock")

        self.items[product.product_id] = current + quantity
        print("Product added to cart")

    def remove_product(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            print("Product removed")
        else:
            print("Product not found in cart")

    def calculate_total(self, inventory):
        total = 0

        for product_id, quantity in self.items.items():
            product = inventory[product_id]
            total += product.price * quantity

        return total

    def display(self, inventory):
        if not self.items:
            print("Cart is empty")
            return

        for product_id, quantity in self.items.items():
            product = inventory[product_id]

            print(
                product.name,
                "x", quantity,
                "=", product.price * quantity
            )

        print("Total:", self.calculate_total(inventory))


class Customer:
    def __init__(self, name):
        self.name = name
        self.cart = ShoppingCart()


class Store:
    def __init__(self):
        self.inventory = {}

    def add_product(self):
        try:
            pid = input("Product ID: ").strip()

            if not pid or pid in self.inventory:
                print("Invalid or duplicate product ID")
                return

            name = input("Product name: ").strip()

            if not name:
                print("Product name required")
                return

            price = float(input("Price: "))
            stock = int(input("Stock quantity: "))

            if price < 0 or stock < 0:
                raise ValueError("Price and stock cannot be negative")

            self.inventory[pid] = Product(
                pid, name, price, stock
            )

            print("Product added")

        except ValueError as error:
            print("Error:", error)

    def display_products(self):
        for product in self.inventory.values():
            print(product, "| Stock:", product.stock)

    def run(self):
        name = input("Enter customer name: ").strip()

        if not name:
            print("Customer name required")
            return

        customer = Customer(name)

        while True:
            print("\n--- SHOPPING SYSTEM ---")
            print("1. Add Product to Store")
            print("2. View Products")
            print("3. Add to Cart")
            print("4. Remove from Cart")
            print("5. View Cart")
            print("6. Checkout")
            print("7. Exit")

            choice = input("Enter choice: ")

            try:
                if choice == "1":
                    self.add_product()

                elif choice == "2":
                    self.display_products()

                elif choice == "3":
                    pid = input("Product ID: ").strip()
                    product = self.inventory.get(pid)

                    if not product:
                        print("Product not found")
                        continue

                    quantity = int(input("Quantity: "))
                    customer.cart.add_product(product, quantity)

                elif choice == "4":
                    pid = input("Product ID: ").strip()
                    customer.cart.remove_product(pid)

                elif choice == "5":
                    customer.cart.display(self.inventory)

                elif choice == "6":
                    total = customer.cart.calculate_total(
                        self.inventory
                    )

                    if not customer.cart.items:
                        print("Cart is empty")
                        continue

                    print("Order confirmed!")
                    print("Customer:", customer.name)
                    print("Total payment:", total)

                    for pid, quantity in customer.cart.items.items():
                        self.inventory[pid].stock -= quantity

                    customer.cart.items.clear()

                elif choice == "7":
                    break

                else:
                    print("Invalid choice")

            except ValueError as error:
                print("Error:", error)


if __name__ == "__main__":
    Store().run()
