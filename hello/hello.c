#include <stdio.h>
#include <cs50.h>

//ask for name
int main(void)
{
    string name = get_string("What's your name? ");

//print name
    printf("hello, %s\n", name);
}