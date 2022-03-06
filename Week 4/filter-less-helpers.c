#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average.
            // Round to the nearest integer.
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            // Set average to every pixel.
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            // Calculate sepia colors.
            int newRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int newGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int newBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            image[i][j].rgbtRed = newRed > 255 ? 255 : newRed;
            image[i][j].rgbtGreen = newGreen > 255 ? 255 : newGreen;
            image[i][j].rgbtBlue = newBlue > 255 ? 255 : newBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // First: create a copy of image.
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // Second: blur image.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sum_blue = 0;
            int sum_green = 0;
            int sum_red = 0;
            float counter = 0.0;

            // Iterate through columns, from -1 to +1.
            for (int h = -1; h <= 1; h++)
            {
                // Iterate through rows.
                for (int w = -1; w <= 1; w++)
                {
                    // If pixel is outside the image (column).
                    if (i + h < 0 || i + h > (height - 1))
                    {
                        continue;
                    }
                    // If pixel is outside the image (row).
                    if (j + w  < 0 || j + w > (width - 1))
                    {
                        continue;
                    }

                    // Sum values of all pixels.
                    sum_red += temp[i + h][j + w].rgbtRed;
                    sum_green += temp[i + h][j + w].rgbtGreen;
                    sum_blue += temp[i + h][j + w].rgbtBlue;

                    counter++;
                }
            }

            // Average colour values.
            image[i][j].rgbtRed = round(sum_red / counter);
            image[i][j].rgbtGreen = round(sum_green / counter);
            image[i][j].rgbtBlue = round(sum_blue / counter);
        }
    }
    return;
}
