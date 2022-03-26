# TODO

# Test user input
while True:
    try:
        height = int(input("Height: "))
        if height > 0 and height < 9:
            break
    except ValueError:
        print("That's not an integer !")

# Display
for i in range(height):
    # Left pyramid
    for j in range(height):
        if i + j < height - 1:
            print(" ", end="")
        else:
            print("#", end="")

    # Double space
    print("  ", end="")

    # Right pyramid
    for k in range(height):
        if i + k >= height - 1:
            print("#", end="")

    print()
