#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


// Declare our functions.
void substitute(string key);
void formula(char pos, string key);

// Main function.
int main(int argc, string argv[])
{
    // Handle error: number of argc.
    if (argc == 1 || argc > 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Handle error: length of argv[1].
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Handle error: characters of argv[1].
    int letters[26];

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain alphabetical character.\n");
            return 1;
        }

        // Check for repeated letters.
        for (int j = 0; j < strlen(argv[1]); j++)
        {
            if (argv[1][i] == letters[j])
            {
                printf("Key must not contain repeated letters\n");
                return 1;
            }
        }

        letters[i] = argv[1][i];
    }

    // Call substitute function.
    substitute(argv[1]);

    // At the end, returning 0;
    return 0;
}

void substitute(string key)
{
    // Ask user for plaintext.
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        // Check if it's not a space or punctuation.
        if (isalpha(plaintext[i]))
        {
            // Call formula function.
            formula(plaintext[i], key);
        }
        // Display if it's a space or punctuation.
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}

void formula(char pos, string key)
{
    string abc = "abcdefghijklmnopqrstuvwxyz";

    for (int i = 0; i < strlen(abc); i++)
    {
        if (islower(pos))
        {
            if (pos == abc[i])
            {
                printf("%c", tolower(key[i]));
            }
        }
        else
        {
            if (pos == toupper(abc[i]))
            {
                printf("%c", toupper(key[i]));
            }
        }
    }
}
