people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Newt", "house": "Hufflepuff"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"},
]

def f(person):
  return person["house"]

people.sort(key=f)

people.sort(key=lambda person: person["name"])

print(people)
