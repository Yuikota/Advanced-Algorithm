class Graph:
    """A reusable directed graph. Vertices can be objects of any type."""

    def __init__(self):
        self.adjacency = {}

    def addVertex(self, vertex):
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []
            return True
        return False

    def addEdge(self, source, destination):
        if source not in self.adjacency or destination not in self.adjacency:
            return False
        if destination not in self.adjacency[source]:
            self.adjacency[source].append(destination)
        return True

    def listIncomingAdjacentVertex(self, vertex):
        incoming = []
        if vertex not in self.adjacency:
            return incoming
        for source, destinations in self.adjacency.items():
            if vertex in destinations:
                incoming.append(source)
        return incoming

    def listOutgoingAdjacentVertex(self, vertex):
        return self.adjacency.get(vertex, []).copy()

    def removeEdge(self, source, destination):
        if source in self.adjacency and destination in self.adjacency[source]:
            self.adjacency[source].remove(destination)
            return True
        return False

    def getVertices(self):
        return list(self.adjacency.keys())


class Course:
    """Stores the profile of one university course."""

    def __init__(self, course_code, course_name, credit_hours, level):
        self.course_code = course_code
        self.course_name = course_name
        self.credit_hours = int(credit_hours)
        self.level = level

    def __str__(self):
        return (f"Course Code: {self.course_code}\nCourse Name: {self.course_name}\n"
                f"Credit Hours: {self.credit_hours}\nLevel: {self.level}")


def build_course_system():
    courses = [
        Course("CS101", "Programming Fundamentals", 3, "Core"),
        Course("CS102", "Object-Oriented Programming", 3, "Core"),
        Course("CS103", "Data Structures", 4, "Core"),
        Course("CS104", "Database Systems", 3, "Core"),
        Course("CS105", "Web Development", 3, "Elective"),
        Course("CS106", "Advanced Algorithms", 4, "Core"),
    ]
    graph = Graph()
    for course in courses:
        graph.addVertex(course)

    # Edge direction: prerequisite course -> course that it unlocks.
    by_code = {course.course_code: course for course in courses}
    graph.addEdge(by_code["CS101"], by_code["CS102"])
    graph.addEdge(by_code["CS102"], by_code["CS103"])
    graph.addEdge(by_code["CS101"], by_code["CS104"])
    graph.addEdge(by_code["CS102"], by_code["CS105"])
    graph.addEdge(by_code["CS103"], by_code["CS106"])
    return graph, by_code


def choose_course(by_code):
    code = input("Enter course code: ").strip().upper()
    course = by_code.get(code)
    if course is None:
        print("Course not found.")
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
                prerequisites = graph.listIncomingAdjacentVertex(course)
                print(f"\nPrerequisites for {course.course_name}:")
                if prerequisites:
                    for item in prerequisites:
                        print(f"- {item.course_code}: {item.course_name}")
                else:
                    print("No prerequisites.")
        elif choice == "4":
            course = choose_course(by_code)
            if course:
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
            try:
                credits = int(input("Credit hours: "))
                level = input("Level (Core/Elective): ").strip().capitalize()
                if not code or not name or credits <= 0 or level not in ("Core", "Elective"):
                    raise ValueError
                if code in by_code:
                    print("That course code already exists.")
                else:
                    course = Course(code, name, credits, level)
                    graph.addVertex(course)
                    by_code[code] = course
                    print("Course added successfully.")
            except ValueError:
                print("Invalid details. Credit hours must be positive and level must be Core or Elective.")
        elif choice == "6":
            print("Select the prerequisite course first.")
            prerequisite = choose_course(by_code)
            print("Select the course that requires it.")
            target = choose_course(by_code)
            if prerequisite and target:
                if prerequisite == target:
                    print("A course cannot be its own prerequisite.")
                else:
                    graph.addEdge(prerequisite, target)
                    print("Prerequisite added.")
        elif choice == "7":
            print("Select the prerequisite course first.")
            prerequisite = choose_course(by_code)
            print("Select the course that requires it.")
            target = choose_course(by_code)
            if prerequisite and target:
                if graph.removeEdge(prerequisite, target):
                    print("Prerequisite removed.")
                else:
                    print("That prerequisite relationship does not exist.")
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 to 8.")


if __name__ == "__main__":
    main()
