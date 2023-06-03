#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Starting Population: ");
    }
    while (start_size < 9);

    // TODO: Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("Ending Population: ");
    }
    while (end_size < start_size);

    // TODO: Calculate number of years until we reach threshold
    int n;
    int x = start_size;
    for (n = 0; x < end_size; n++)
    {
        x = x + x / 3 - x / 4;
    }

    // TODO: Print number of years
    printf("Years: %i\n", n);
}
