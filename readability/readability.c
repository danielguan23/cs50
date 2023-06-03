#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //get text from user
    string text = get_string("Text: ");

    //find number of letters

    int letters = count_letters(text);
    printf("%i letters\n", letters);


    //find number of words
    int words = count_words(text);
    printf("%i words\n", words);

    //find number of sentences (or number of periods)
    int sentences = count_sentences(text);
    printf("%i sentences\n", sentences);

    //calculation
    float L = letters / (float) words * 100.0;
    float S = sentences / (float) words * 100.0;

    float index = 0.0588 * (float) L - 0.296 * (float) S - 15.8;
    int index_round = round((float) index);
    printf("%.5f, %i\n", index, index_round);

    //print output
    if (index_round < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index_round > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index_round);
    }
}


//functions space

int count_letters(string text)
{
    int letlen = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (islower(text[i]))
        {
            letlen++;
        }
        if (isupper(text[i]))
        {
            letlen++;
        }
    }
    return letlen;
}

int count_words(string text)
{
    int wordlen = 1;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] - ' ' == 0)
        {
            wordlen++;
        }

    }
    return wordlen;
}

int count_sentences(string text)
{
    int senlen = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == '.' | text[i] == '!' | text[i] == '?')
        {
            senlen++;
        }

    }
    return senlen;
}

