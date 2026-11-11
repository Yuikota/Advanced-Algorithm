class Graph:
    """A reusable directed graph structure using an adjacency list."""

    def __init__(self):
        # dictionary where keys are nodes and values are lists of connections
        self.adjacency = {}

    def addVertex(self, vertex):
        # If the course object doesn't exist in our map, add it with an empty list
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []
            return True
        return False

    def addEdge(self, source, destination):
        # Verify both courses exist before linking them
        if source not in self.adjacency or destination not in self.adjacency:
            return False
        # Link source course pointing towards the destination course
        if destination not in self.adjacency[source]:
            self.adjacency[source].append(destination)
        return True

    def listIncomingAdjacentVertex(self, vertex):
        incoming = []
        if vertex not in self.adjacency:
            return incoming
        # Look at every course connection list to see who points to our target vertex
        for source, destinations in self.adjacency.items():
            if vertex in destinations:
                incoming.append(source)
        return incoming

    def listOutgoingAdjacentVertex(self, vertex):
        # Return a copy of the list containing the courses this course unlocks
        return self.adjacency.get(vertex, []).copy()

    def removeEdge(self, source, destination):
        # Disconnect a specific prerequisite link if it exists
        if source in self.adjacency and destination in self.adjacency[source]:
            self.adjacency[source].remove(destination)
            return True
        return False

    def getVertices(self):
        # Return a list of all course objects registered inside our graph nodes
        return list(self.adjacency.keys())


class Course:
    """Stores the profile of one university course."""

    def __init__(self, course_code, course_name, credit_hours, level):
        # Set attributes cleanly for a single specific class track
        self.course_code = str(course_code).strip().upper()
        self.course_name = course_name.strip()
        self.credit_hours = int(credit_hours)
        self.level = level.strip().capitalize()

    def __str__(self):
        # print object properties when displayed as text string
        return (f"Course Code: {self.course_code}\nCourse Name: {self.course_name}\n"
                f"Credit Hours: {self.credit_hours}\nLevel: {self.level}")


def build_course_system():
    # Setup default array list of courses
    courses = [
        Course("CS101", "Programming Fundamentals", 3, "Core"),
        Course("CS210", "Object-Oriented Programming", 3, "Core"),
        Course("CS220", "Data Structures", 4, "Core"),
        Course("CS312", "Database Management Systems", 3, "Core"),
        Course("CS335", "Web Application Development", 3, "Elective"),
        Course("CS410", "Advanced Algorithms", 4, "Core"),
    ]
    graph = Graph()
    for course in courses:
        graph.addVertex(course)

    # Quickly map unique keys directly back to their primary objects
    by_code = {course.course_code: course for course in courses}

    # Connect connections together (Prerequisite Course -> Unlocked Target Course)
    graph.addEdge(by_code["CS101"], by_code["CS210"])
    graph.addEdge(by_code["CS210"], by_code["CS220"])
    graph.addEdge(by_code["CS101"], by_code["CS312"])
    graph.addEdge(by_code["CS210"], by_code["CS335"])
    graph.addEdge(by_code["CS220"], by_code["CS410"])
    return graph, by_code


def choose_course(by_code):
    # prompt user for input and match back the course object
    code = input("Enter course code: ").strip().upper()
    course = by_code.get(code)
    if course is None:
        print("Error: Course code not found.")
    return course


def main():
    graph, by_code = build_course_system()

    while True:
        print("\n===== UNIVERSITY COURSE PREREQUISITE SYSTEM =====")
        print("1. Display all course names")
        print("2. View course details")
        print("3. View prerequisites for a course")
        print("4. View courses unlocked by a course")
        print("5. Add a new course")
        print("6. Add a prerequisite")
        print("7. Remove a prerequisite")
        print("8. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\n--- Course List ---")
            for course in graph.getVertices():
                print(f"{course.course_code} - {course.course_name}")

        elif choice == "2":
            course = choose_course(by_code)
            if course:
                print("\n" + str(course))

        elif choice == "3":
            course = choose_course(by_code)
            if course:
                # Prerequisites point into our course (Incoming arrows)
                prerequisites = graph.listIncomingAdjacentVertex(course)
                print(f"\nPrerequisites for {course.course_name}:")
                if prerequisites:
                    for item in prerequisites:
                        print(f"- {item.course_code}: {item.course_name}")
                else:
                    print("No prerequisites required.")

        elif choice == "4":
            course = choose_course(by_code)
            if course:
                # Unlocked targets are paths pointing outwards (Outgoing arrows)
                unlocked = graph.listOutgoingAdjacentVertex(course)
                print(f"\nCourses unlocked by {course.course_name}:")
                if unlocked:
                    for item in unlocked:
                        print(f"- {item.course_code}: {item.course_name}")
                else:
                    print("This course does not unlock another course.")

        elif choice == "5":
            code = input("New course code: ").strip().upper()
            name = input("Course name: ").strip()

            if not code or not name:
                print("Input Error: Code and Name cannot be blank.")
                continue

            if code in by_code:
                print("Error: That course code already exists in the system.")
                continue

            try:
                credits = int(input("Credit hours: "))
                if credits <= 0:
                    print("Input Error: Credit hours must be greater than zero.")
                    continue
            except ValueError:
                print("Input Error: Credit hours must be a valid whole number.")
                continue

            level = input("Level (Core/Elective): ").strip().capitalize()
            if level not in ("Core", "Elective"):
                print("Input Error: Level must be exactly 'Core' or 'Elective'.")
                continue

            course = Course(code, name, credits, level)
            graph.addVertex(course)
            by_code[code] = course
            print(f"Success: {code} added successfully.")

        elif choice == "6":
            print("Select the prerequisite course first.")
            prerequisite = choose_course(by_code)
            if not prerequisite:
                continue

            print("Select the course that requires it.")
            target = choose_course(by_code)
            if not target:
                continue

            if prerequisite == target:
                print("Validation Error: A course cannot be its own prerequisite.")
            else:
                graph.addEdge(prerequisite, target)
                print("Success: Prerequisite relationship established.")

        elif choice == "7":
            print("Select the prerequisite course first.")
            prerequisite = choose_course(by_code)
            if not prerequisite:
                continue

            print("Select the course that requires it.")
            target = choose_course(by_code)
            if not target:
                continue

            if graph.removeEdge(prerequisite, target):
                print("Success: Prerequisite relationship removed.")
            else:
                print("Error: That prerequisite relationship does not exist.")

        elif choice == "8":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose an option from 1 to 8.")


if __name__ == "__main__":
    main()
