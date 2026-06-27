justice_league = [
    "Superman",
    "Batman",
    "Wonder Woman",
    "Flash",
    "Aquaman",
    "Green Lantern"
]

print("Original Justice League:")
print(justice_league)
print("\n1. Number of members:")
print(len(justice_league))
justice_league.append("Batgirl")
justice_league.append("Nightwing")

print("\n2. After adding Batgirl and Nightwing:")
print(justice_league)
justice_league.remove("Wonder Woman")
justice_league.insert(0, "Wonder Woman")

print("\n3. Wonder Woman becomes the leader:")
print(justice_league)
justice_league.remove("Green Lantern")

aquaman_index = justice_league.index("Aquaman")

justice_league.insert(aquaman_index + 1, "Green Lantern")

print("\n4. Green Lantern moved between Aquaman and Flash:")
print(justice_league)
justice_league = [
    "Cyborg",
    "Shazam",
    "Hawkgirl",
    "Martian Manhunter",
    "Green Arrow"
]

print("\n5. New Justice League:")
print(justice_league)
justice_league.sort()

print("\n6. Sorted Justice League:")
print(justice_league)

print("\nNew Leader:")
print(justice_league[0])
