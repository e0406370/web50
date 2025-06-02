class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


point = Point(2, 8)
print(point.x)
print(point.y)


class Flight:
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, name):
        # Pythonic way of writing 'if self.open_seats() == 0'
        if not self.open_seats():
            return False

        self.passengers.append(name)
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)


flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]

for person in people:
    success = flight.add_passenger(person)

    if success:
        print(f"Added {person} to flight successfully.")

    else:
        print(f"No available seats for {person}!")
