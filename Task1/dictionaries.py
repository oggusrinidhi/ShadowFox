friends = ["Srinidhi", "Anusha", "Rahul", "Kiran", "Priya"]

friend_tuples = []

for name in friends:
    friend_tuples.append((name, len(name)))

print("Question 1")
print("Friends List:")
print(friends)

print("\nList of Tuples (Name, Length):")
print(friend_tuples)

your_expenses = {
    "Hotel": 1200,
    "Food": 800,
    "Transportation": 500,
    "Attractions": 300,
    "Miscellaneous": 200
}

partner_expenses = {
    "Hotel": 1000,
    "Food": 900,
    "Transportation": 600,
    "Attractions": 400,
    "Miscellaneous": 150
}


your_total = sum(your_expenses.values())
partner_total = sum(partner_expenses.values())

print("\nQuestion 2")
print("Your Total Expenses =", your_total)
print("Partner's Total Expenses =", partner_total)

if your_total > partner_total:
    print("You spent more money.")
elif partner_total > your_total:
    print("Your partner spent more money.")
else:
    print("Both spent the same amount.")

max_difference = 0
difference_category = ""

for category in your_expenses:
    difference = abs(your_expenses[category] - partner_expenses[category])

    if difference > max_difference:
        max_difference = difference
        difference_category = category

print("\nExpense Category with Maximum Difference:")
print("Category:", difference_category)
print("Difference:", max_difference)
