#include "helpers.h"
#include <math.h>

/*typedef struct
{
    BYTE  rgbtBlue;
    BYTE  rgbtGreen;
    BYTE  rgbtRed;
} __attribute__((__packed__))
RGBTRIPLE;*/

//definitions | s for surrounding pixels


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int h = 0;
    int hs = 0;
    int w = 0;
    int ws = 0;
    int average = 0;
    for (h = 0; h < height; h++)
    {
        for (w = 0; w < width; w++)
        {
            average = round((image[h][w].rgbtBlue + image[h][w].rgbtGreen + image[h][w].rgbtRed) / 3.0);
            image[h][w].rgbtBlue = average;
            image[h][w].rgbtGreen = average;
            image[h][w].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int h = 0; h < height; h++)
    {
        if (width % 2 == 0)
        {
            for (int w = 0; w < width / 2; w++)
            {
                temp = image[h][w];
                image[h][w] = image[h][width - (w + 1)];
                image[h][width - (w + 1)] = temp;
            }

        }
        else
        {
            for (int w = 0; w < width / 2; w++)
            {
                temp = image[h][w];
                image[h][w] = image[h][width - (w + 1)];
                image[h][width - (w + 1)] = temp;
            }
        }

    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    //Go through each pixel

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //Reset average value
            float blue = 0;
            float green = 0;
            float red = 0;
            float counter = 0;

            //Go through surrounding pixels of it.
            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {

                    //add values to temp
                    if ((h + i) < 0 || (h + i) >= height || (w + j) < 0 || (w + j) >= width)
                    {
                        continue;
                    }

                    blue += image[h + i][w + j].rgbtBlue;
                    green += image[h + i][w + j].rgbtGreen;
                    red += image[h + i][w + j].rgbtRed;
                    counter++;
                }
            }
            //find average RGB
            tmp[h][w].rgbtBlue = round(blue / counter);
            tmp[h][w].rgbtGreen = round(green / counter);
            tmp[h][w].rgbtRed = round(red / counter);
        }
    }

    //set RGB value to central pixel

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w].rgbtBlue = tmp[h][w].rgbtBlue;
            image[h][w].rgbtGreen = tmp[h][w].rgbtGreen;
            image[h][w].rgbtRed = tmp[h][w].rgbtRed;

        }
    }
    return;
}


// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int gxBlue = 0;
            int gyBlue = 0;
            int gxGreen = 0;
            int gyGreen = 0;
            int gxRed = 0;
            int gyRed = 0;

            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {
                    if ((h + i) < 0 || (h + i) >= height || (w + j) < 0 || (w + j) >= width)
                    {
                        continue;
                    }

                    gxBlue += image[h + i][w + j].rgbtBlue * gx[i + 1][j + 1];
                    gyBlue += image[h + i][w + j].rgbtBlue * gy[i + 1][j + 1];
                    gxGreen += image[h + i][w + j].rgbtGreen * gx[i + 1][j + 1];
                    gyGreen += image[h + i][w + j].rgbtGreen * gy[i + 1][j + 1];
                    gxRed += image[h + i][w + j].rgbtRed * gx[i + 1][j + 1];
                    gyRed += image[h + i][w + j].rgbtRed * gy[i + 1][j + 1];
                }
            }

            int aveblue = round(sqrt(gxBlue * gxBlue + gyBlue * gyBlue));
            int avegreen = round(sqrt(gxGreen * gxGreen + gyGreen * gyGreen));
            int avered = round(sqrt(gxRed * gxRed + gyRed * gyRed));

            temp[h][w].rgbtBlue = (aveblue > 255) ? 255 : aveblue;
            temp[h][w].rgbtGreen = (avegreen > 255) ? 255 : avegreen;
            temp[h][w].rgbtRed = (avered > 255) ? 255 : avered;
        }
    }

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w].rgbtBlue = temp[h][w].rgbtBlue;
            image[h][w].rgbtGreen = temp[h][w].rgbtGreen;
            image[h][w].rgbtRed = temp[h][w].rgbtRed;
        }
    }
    return;
}
