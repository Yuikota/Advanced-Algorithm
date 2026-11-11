import time


class Medicine:
    """Stores information about one pharmacy product."""

    def __init__(self, product_id, name, category, price, quantity):
        # Save all the medicine details into the object variables
        self.product_id = str(product_id).strip()
        self.name = name.strip()
        self.category = category.strip()
        self.price = float(price)
        self.quantity = int(quantity)

    def __str__(self):
        # Format the item details nicely into a clean text line
        return (f"ID: {self.product_id} | Name: {self.name} | Category: {self.category} | "
                f"Price: RM{self.price:.2f} | Quantity: {self.quantity}")


class HashTable:
    """Hash table using open addressing and linear probing."""

    def __init__(self, size=11):
        # Create a list of fixed size filled with None (Empty spaces)
        self.size = size
        self.slots = [None] * size

    def _hash(self, product_id):
        # Turn the ID string into a slot number using math (ASCII sum % table size)
        return sum(ord(char) for char in str(product_id)) % self.size

    def insert(self, medicine):
        # Get the starting slot position from our hash calculation
        index = self._hash(medicine.product_id)

        # Loop through the table to find a slot if a collision happens
        for step in range(self.size):
            current = (index + step) % self.size

            # If slot is empty, put the medicine here and stop
            if self.slots[current] is None:
                self.slots[current] = medicine
                return True

            # If the ID already exists, update/overwrite its data here
            if self.slots[current].product_id == medicine.product_id:
                self.slots[current] = medicine
                return True
        return False  # Return False if the whole table is totally full

    def search(self, product_id):
        # Find where the item should theoretically start in the list
        index = self._hash(product_id)

        # Search step-by-step through the slots
        for step in range(self.size):
            current = (index + step) % self.size

            # If we hit an empty slot, it means the item was never added
            if self.slots[current] is None:
                return None

            # If we match the product ID, return the medicine object
            if self.slots[current].product_id == str(product_id):
                return self.slots[current]
        return None

    def display(self):
        # Loop through everything to show what is inside every single slot
        print("\n===== Hash Table Slots =====")
        for index, medicine in enumerate(self.slots):
            if medicine is None:
                print(f"Slot {index}: Empty")
            else:
                print(f"Slot {index}: {medicine.product_id} - {medicine.name}")


def create_sample_data():
    # Setup our basic dummy starting values for the app
    # IDs 1001 and 1010 create a hash collision to test our linear probing
    return [
        Medicine("1001", "Panadol", "Pain Relief", 5.50, 100),
        Medicine("1002", "Vitamin C", "Supplement", 12.00, 60),
        Medicine("1003", "Cough Syrup", "Cough and Cold", 8.90, 35),
        Medicine("1010", "Antacid", "Digestive", 6.20, 40),
        Medicine("1005", "Antiseptic Cream", "First Aid", 10.50, 25),
        Medicine("1006", "Allergy Tablets", "Allergy", 14.00, 50),
    ]


def compare_search_performance(records, target_id, repetitions=20000):
    """Compare average lookup time in the hash table and a one-dimensional list."""
    # Initialize the structures with our sample records
    table = HashTable(max(11, len(records) * 2 + 1))
    for item in records:
        table.insert(item)
    array = records.copy()

    # Time test 1: Check how fast the Hash Table does lookups
    start = time.perf_counter_ns()
    for _ in range(repetitions):
        table.search(target_id)
    hash_time = (time.perf_counter_ns() - start) / repetitions

    # Time test 2: Check how fast a standard list/array does lookups
    start = time.perf_counter_ns()
    for _ in range(repetitions):
        for item in array:
            if item.product_id == str(target_id):
                break
    array_time = (time.perf_counter_ns() - start) / repetitions

    # Print out our speed experiment calculations
    print("\n===== Search Performance Experiment =====")
    print(f"Records tested: {len(records)}")
    print(f"Search repetitions: {repetitions}")
    print(f"Average hash table search: {hash_time:.2f} ns")
    print(f"Average array search:      {array_time:.2f} ns")

    if hash_time < array_time:
        print("Result: Hash table was faster due to constant time lookup properties.")
    else:
        print("Result: Linear array was faster due to minimal element overhead.")


def main():
    inventory = HashTable(11)
    records = create_sample_data()
    for medicine in records:
        inventory.insert(medicine)

    while True:
        print("\n===== PHARMACY INVENTORY SYSTEM =====")
        print("1. Display inventory")
        print("2. Insert medicine")
        print("3. Search medicine")
        print("4. Compare search performance")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            inventory.display()
        elif choice == "2":
            product_id = input("Product ID: ").strip()
            name = input("Medicine name: ").strip()
            category = input("Category: ").strip()

            if not product_id or not name:
                print("Error: Product ID and Name cannot be left blank.")
                continue

            try:
                price = float(input("Price (RM): "))
                if price < 0:
                    print("Error: Price cannot be negative.")
                    continue
            except ValueError:
                print("Error: Price must be a valid number.")
                continue

            try:
                quantity = int(input("Quantity: "))
                if quantity < 0:
                    print("Error: Quantity cannot be negative.")
                    continue
            except ValueError:
                print("Error: Quantity must be a valid integer.")
                continue

            if inventory.insert(Medicine(product_id, name, category, price, quantity)):
                print("Medicine inserted successfully.")
            else:
                print("The hash table is full. Medicine was not inserted.")

        elif choice == "3":
            product_id = input("Enter product ID to search: ").strip()
            result = inventory.search(product_id)
            print(result if result else "Medicine not found.")
        elif choice == "4":
            compare_search_performance(records, records[-1].product_id)
        elif choice == "5":
            print("Thank you. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    main()
