#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    //get text from user
    string text = get_string("Message: ");

    //detect length and find ascii of each char
    int length = strlen(text);

    //store each ascii in asc array
    for (int i = 0; i < length; i++)
    {
        int dec = text[i];
        //printf("byte %i\n", dec);

        int binary[] = {0, 0, 0, 0, 0, 0, 0, 0};
        int j = 0;
        while (dec > 0)
        {
            binary[j] = dec % 2;
            dec = dec / 2;
            j++;
        }

        for (int k = 7; k >= 0; k--)
        {
            print_bulb(binary[k]);
        }
        printf("\n");
    }

    //check array

    //print bulb
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
