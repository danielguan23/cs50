#include <cs50.h>
#include <stdio.h>

int main(void)
{

//ask for height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 | height > 8);


//counter and vertical generator
    for (int printno = 1; printno - 1 < height; printno++)
    {
        //space generator
        for (int x = 0; x < height - printno; x++)
        {
            printf(" ");
        }
        //horizontal hash generator
        for (int x = 0; x < printno; x++)
        {
            printf("#");
        }

        printf("\n");
    }
}