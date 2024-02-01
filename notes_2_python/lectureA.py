name = input("What is your name?\n")
print(f"Hello, {name}!")

# int
a = 28

# float
b = 1.5

# str
c = "Hello!"

# bool
d = True

# NoneType
e = None

n = int(input("Provide a number: "))

if n > 0:
    print("n is positive.")
elif n < 0:
    print("n is negative.")
else:
    print("n is zero.")

strawhat_members = [
    "Monkey D. Luffy",
    "Roronoa Zoro",
    "Nami",
    "Usopp",
    "Sanji",
    "Tony Tony Chopper",
    "Nico Robin",
    "Franky",
    "Brook",
    "Jinbe",
]

print(strawhat_members)
print(strawhat_members[0])
print(strawhat_members[0][7])

coordinateX = 10.0
coordinateY = 20.0
coordinate = (coordinateX, coordinateY)

print(coordinate)

# Data Structures
# list - sequence of MUTABLE values
# ordered: yes
# mutable: yes

# tuple - sequence of IMMUTABLE values
# ordered: yes
# mutable: no

# set - collection of UNIQUE values
# ordered: no
# mutable: N/A

# dict - collection of K-V pairs
# ordered: no
# mutable: yes

strawhat_members.append("Vivi")
strawhat_members.sort()
print(strawhat_members)

strawhat_roles = set()

strawhat_roles.add("Captain")
strawhat_roles.add("Captain")
strawhat_roles.add("Swordsman")
strawhat_roles.add("Navigator")
strawhat_roles.add("Sniper")
strawhat_roles.add("Chef")
strawhat_roles.add("Doctor")
strawhat_roles.add("Archaeologist")
strawhat_roles.add("Shipwright")
strawhat_roles.add("Musician")
strawhat_roles.add("Helmsman")

print(strawhat_roles)

print(f"The list of 'strawhat_members' has {len(strawhat_members)} elements.")
print(f"The set of 'strawhat_roles' has {len(strawhat_roles)} elements")

for strawhat in strawhat_members:
    print(f"Strawhat Pirate Member: {strawhat}")

# Start defaults to 0!
for i in range(1, len(strawhat_members) + 1):
    print(i, end=" ")
print()

for char in strawhat_members[0]:
    print(char, end=" ")
print()

strawhat_roles_dict = {
    "Monkey D. Luffy": "Captain",
    "Roronoa Zoro": "Swordsman",
    "Nami": "Navigator",
    "Usopp": "Sniper",
    "Sanji": "Chef",
    "Tony Tony Chopper": "Doctor",
    "Nico Robin": "Archaeologist",
    "Franky": "Shipwright",
    "Brook": "Musician",
    "Jinbe": "Helmsman",
}
strawhat_roles_dict["Vivi"] = "Honorary Member"

print(strawhat_roles_dict)
print(strawhat_roles_dict["Monkey D. Luffy"])
print(strawhat_roles_dict["Vivi"])
