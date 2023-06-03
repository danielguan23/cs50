#include <cs50.h>
#include <stdio.h>

int main(void)
{
//length finder
    long n = get_long("Card Number: ");
    long div = n;

    int digits;
    for (digits = 0; div > 0; digits++)
    {
        div = div / 10;
    }

//basic length check
    if (digits != 13 && digits != 15 && digits != 16)
    {
        printf("INVALID\n");
        return 0;
    }

//algorithm checker
    long x = n;
    int firsttotal = 0;
    int secondtotal = 0;
    int total = 0;
    int mod1 = 0;
    int mod2 = 0;
    int firstdigit = 0;
    int seconddigit = 0;

    do
    {
        //first check and remove
        mod1 = x % 10;
        firsttotal = firsttotal + mod1;
        x = (x - mod1) / 10;

        //second check and remove
        mod2 = x % 10;
        x = (x - mod2) / 10;

        //double and split digits
        mod2 = mod2 * 2;
        firstdigit = mod2 % 10;
        seconddigit = (mod2 - firstdigit) / 10;
        secondtotal = secondtotal + firstdigit + seconddigit;
    }
    while (x > 0);
    total = firsttotal + secondtotal;

//check total for valid
    if (total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

//check card type
    long firstlong = n;
    do
    {
        firstlong = firstlong / 10;
    }
    while (firstlong > 100);

    if ((firstlong / 10 == 5) && (0 < firstlong % 10 && firstlong % 10 < 6))
    {
        printf("MASTERCARD\n");
    }
    else if ((firstlong / 10 == 3) && (firstlong % 10 == 4 || firstlong % 10 == 7))
    {
        printf("AMEX\n");
    }
    else if (firstlong / 10 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}