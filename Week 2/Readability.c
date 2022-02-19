#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// Declare functions.
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Store user text.
    string text = get_string("Text: ");

    // Count number of letters.
    int l = count_letters(text);

    // Count number of words.
    int w = count_words(text);

    // Count number of sentences;
    int s = count_sentences(text);

    // Average letters per 100 words.
    float L = (l / (float) w) * 100;

    // Average sentences per 100 words.
    float S = (s / (float) w) * 100;

    // Formula.
    int index = round(0.0588 * L - 0.296 * S - 15.8);


    // Final result.
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// Function letters.
int count_letters(string text)
{
    int letters = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    return letters;
}

// Function words.
int count_words(string text)
{
    // Text is starting with one word.
    int words = 1;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }

    return words;
}


// Function sentences.
int count_sentences(string text)
{
    int sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            sentences++;
        }
    }

    return sentences;
}
