#include <cs50.h>
#include <stdio.h>

// Store credit card number.
long credit_card;

int main(void)
{
    // Ask user to enter his credit card number.
    credit_card = get_long("Number: ");

    // Calculate length of card number.
    // Store result in variable "credit_card_length".
    int credit_card_length = 0;
    long temp_cc = credit_card;

    while (temp_cc > 0)
    {
        temp_cc = temp_cc / 10;
        credit_card_length++;
    }

    // Check if credit card length is valid.
    if (
        credit_card_length != 13 &&
        credit_card_length != 15 &&
        credit_card_length != 16)
    {
        printf("INVALID\n");
        return false;
    }

    // Checksum operations.
    int basic_sum = 0;
    int double_sum = 0;

    int mod1;
    int mod2;

    int div1;
    int div2;

    long cc = credit_card;

    do
    {
        // Isolate last number.
        // Then, calculate "basic" sum.
        mod1 = cc % 10;
        basic_sum += mod1;

        // Delete last credit card number.
        cc = cc / 10;

        // Then, isolate new last number.
        // (which is the second last number)
        mod2 = cc % 10;

        // Calculate "double" sum.
        mod2 = mod2 * 2;
        div1 = mod2 % 10;
        div2 = mod2 / 10;
        double_sum = double_sum + div1 + div2;

        // Delete last credit card number.
        cc = cc / 10;
    }
    while (cc > 0);

    int total = basic_sum + double_sum;

    // Check Luhn Algorithm.
    if (total % 10 != 0)
    {
        printf("INVALID\n");
        return false;
    }

    // Isolate two first numbers of credit card.
    long first_numbers = credit_card;

    do
    {
        first_numbers = first_numbers / 10;
    }
    while (first_numbers > 100);

    if (first_numbers == 34 ||
        first_numbers == 37)
    {
        printf("AMEX\n");
    }
    else if (first_numbers == 51 ||
             first_numbers == 52 ||
             first_numbers == 53 ||
             first_numbers == 54 ||
             first_numbers == 55)
    {
        printf("MASTERCARD\n");
    }
    else if (first_numbers / 10 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
