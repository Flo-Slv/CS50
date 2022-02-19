#include <cs50.h>
#include <stdio.h>

// Declare variable "height" to store number of row.
int height;

int main(void)
{
    // Check if user enter correct number.
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Declare variables to store hashtag, space and double space, as strings.
    string hashtag = "#";
    string space = " ";
    string double_space = "  ";

    for (int i = 0; i < height; i++)
    {
        // Create left pyramide.
        for (int j = 0; j < height; j++)
        {
            if (i + j < height - 1)
            {
                printf("%s", space);
            }
            else
            {
                printf("%s", hashtag);
            }
        }

        printf("%s", double_space);

        // Create right pyramide.
        for (int k = 0; k < height; k++)
        {
            if (i + k >= height - 1)
            {
                printf("%s", hashtag);
            }
        }

        printf("\n");
    }
}
