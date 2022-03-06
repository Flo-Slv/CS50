#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Handle error if argc is not 2.
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the .raw file.
    FILE *raw_file = fopen(argv[1], "r");

    // Handle errors if file does not exist or not a file.
    if (raw_file == NULL)
    {
        printf("Can not open the file: %s\n", argv[1]);
        return 1;
    }

    // Declare variables.
    BYTE buffer[512]; // Store data of 512 bytes we found in card.raw.
    int counter = 0; // Number of jpg files.
    char filename[8]; // Store the name of new file (8 char): "***.jpg\0"
    FILE *new_file = NULL; // Address to new file we want to create.

    // Loop through until there is no more 512 bytes's block.
    while (fread(&buffer, 512, 1, raw_file) != 0)
    {
        // Check if it's a jpg file.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If a new_file already exist, close it.
            if (new_file != NULL)
            {
                fclose(new_file);
            }

            sprintf(filename, "%03i.jpg", counter);
            new_file = fopen(filename, "w");

            counter++;
        }

        if (new_file != NULL)
        {
            fwrite(&buffer, 512, 1, new_file);
        }
    }
    // Do not forget to close all files open.
    fclose(raw_file);
    fclose(new_file);

    return 0;
}
