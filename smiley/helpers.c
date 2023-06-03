#include "helpers.h"
#include "stdio.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    //find all black pixels and loop
    int h;
    int w;
    //height loop
    for (h = 0; h < height; h++)
    {
        //width loop
        for (w = 0; w < width; w++)
        {
            //rgb(229, 253, 209) green colour
            if (image[h][w].rgbtBlue == 0)
            {
                image[h][w].rgbtRed = 229;
                image[h][w].rgbtGreen = 253;
                image[h][w].rgbtBlue = 209;
            }
        }
    }
}
