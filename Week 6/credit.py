from cs50 import get_int
import sys

# Ask user to enter a credit card num.
cc = get_int("Number: ")

# And create a copy of cc to use it later.
ccn = cc

# Convert to string to know length.
l = len(str(cc))

if l != 13 and l != 15 and l != 16:
    print("INVALID")
    sys.exit(1)

basic_sum = 0
double_sum = 0

while cc > 0:
    # Isolate last number then calculate basic_sum.
    mod1 = cc % 10
    basic_sum += mod1

    # Delete last cc number.
    cc = cc // 10

    # Then isolate new last number.
    mod2 = cc % 10

    # Calculate double_sum.
    mod2 = mod2 * 2
    div1 = mod2 % 10
    div2 = mod2 // 10
    double_sum = double_sum + div1 + div2

    # Delete last cc number.
    cc = cc // 10

total = basic_sum + double_sum

# Check Luhn algorithm.
if total % 10 != 0:
    print("INVALID")
    sys.exit(1)

# Isolate two last first number of cc.
while ccn > 100:
    ccn = ccn // 10

if ccn == 37 or ccn == 34:
    print("AMEX")
elif ccn in range(51, 56):
    print("MASTERCARD")
elif ccn // 10 == 4:
    print("VISA")
else:
    print("INVALID")
    sys.exit(1)
