import time


class Medicine:
    """Stores information about one pharmacy product."""

    def __init__(self, product_id, name, category, price, quantity):
        self.product_id = str(product_id)
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity = int(quantity)

    def __str__(self):
        return (f"ID: {self.product_id} | Name: {self.name} | Category: {self.category} | "
                f"Price: RM{self.price:.2f} | Quantity: {self.quantity}")


class HashTable:
    """Hash table using open addressing and linear probing."""

    def __init__(self, size=11):
        self.size = size
        self.slots = [None] * size

    def _hash(self, product_id):
        # Add the digits/characters to create a simple hash index.
        return sum(ord(char) for char in str(product_id)) % self.size

    def insert(self, medicine):
        index = self._hash(medicine.product_id)

        # Check each following slot until an empty slot or same ID is found.
        for step in range(self.size):
            current = (index + step) % self.size
            if self.slots[current] is None:
                self.slots[current] = medicine
                return True
            if self.slots[current].product_id == medicine.product_id:
                self.slots[current] = medicine
                return True
        return False

    def search(self, product_id):
        index = self._hash(product_id)

        for step in range(self.size):
            current = (index + step) % self.size
            if self.slots[current] is None:
                return None
            if self.slots[current].product_id == str(product_id):
                return self.slots[current]
        return None

    def display(self):
        print("\n===== Hash Table Slots =====")
        for index, medicine in enumerate(self.slots):
            if medicine is None:
                print(f"Slot {index}: Empty")
            else:
                print(f"Slot {index}: {medicine.product_id} - {medicine.name}")


def create_sample_data():
    return [
        Medicine("1001", "Panadol", "Pain Relief", 5.50, 100),
        Medicine("1002", "Vitamin C", "Supplement", 12.00, 60),
        Medicine("1003", "Cough Syrup", "Cough and Cold", 8.90, 35),
        Medicine("1004", "Antacid", "Digestive", 6.20, 40),
        Medicine("1005", "Antiseptic Cream", "First Aid", 10.50, 25),
        Medicine("1006", "Allergy Tablets", "Allergy", 14.00, 50),
    ]


def compare_search_performance(records, target_id, repetitions=20000):
    """Compare average lookup time in the hash table and a one-dimensional list."""
    table = HashTable(max(11, len(records) * 2 + 1))
    for item in records:
        table.insert(item)
    array = records.copy()

    start = time.perf_counter_ns()
    for _ in range(repetitions):
        table.search(target_id)
    hash_time = (time.perf_counter_ns() - start) / repetitions

    start = time.perf_counter_ns()
    for _ in range(repetitions):
        for item in array:
            if item.product_id == str(target_id):
                break
    array_time = (time.perf_counter_ns() - start) / repetitions

    print("\n===== Search Performance Experiment =====")
    print(f"Records tested: {len(records)}")
    print(f"Search repetitions: {repetitions}")
    print(f"Average hash table search: {hash_time:.2f} ns")
    print(f"Average array search:      {array_time:.2f} ns")
    print("Note: timings depend on the computer and the selected record.")
    if hash_time < array_time:
        print("Result: The hash table was faster in this experiment.")
    elif hash_time > array_time:
        print("Result: The array was faster in this experiment.")
    else:
        print("Result: Both methods had almost equal measured time.")


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
            try:
                price = float(input("Price (RM): "))
                quantity = int(input("Quantity: "))
                if price < 0 or quantity < 0 or not product_id or not name:
                    raise ValueError
                if inventory.insert(Medicine(product_id, name, category, price, quantity)):
                    print("Medicine inserted successfully.")
                else:
                    print("The hash table is full. Medicine was not inserted.")
            except ValueError:
                print("Invalid input. Price and quantity must be valid non-negative numbers.")
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
