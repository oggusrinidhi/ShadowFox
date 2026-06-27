def format_number(number, representation):
    return format(number, representation)

result = format_number(145, 'o')

print("Question 1:")
print("Formatted Result:", result)
print("Representation Used: Octal (Base 8)")
pi = 3.14
radius = 84

area = pi * radius * radius

water_per_square_meter = 1.4

total_water = area * water_per_square_meter

print("\nQuestion 2:")
print("Area of Pond =", area, "square meters")
print("Total Water =", int(total_water), "liters")
distance = 490      # meters
time_minutes = 7


time_seconds = time_minutes * 60

speed = distance / time_seconds

print("\nQuestion 3:")
print("Speed =", int(speed), "meters/second")
