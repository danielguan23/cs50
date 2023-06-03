// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <strings.h>
#include <string.h>

#include "dictionary.h"

int dictnum;
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
// Size of hash table is double of data and nearest prime
const unsigned int N = 286181;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int wordhash = hash(word);

    node *n = table[wordhash];
    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //Referenced DJB2 hash function
    unsigned long hash = 5381;
    int c;
    //takes every char in word until NULL reached
    while ((c = tolower(*word++)))
    {
        //bitwise function *33 + c
        hash = ((hash << 5) + hash) + c;
        hash = hash % 286181;
    }

    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
//need to unload after!!!!!!
{
    FILE *dpoint = fopen(dictionary, "r");
    char wpoint[LENGTH + 1];
    node *n;
    if (dpoint == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }

    //set pointer for new word one at a time
    while (fscanf(dpoint, "%s", wpoint) != EOF)
    {
        n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Memory problem");
            return false;
        }
        strcpy(n->word, wpoint);

        //insert word to hash table
        int hashv = hash(wpoint);
        n->next = table[hashv];
        table[hashv] = n;
        dictnum++;
    }
    fclose(dpoint);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictnum;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *n;
    int i;
    for (i = 0; i < N; i++)
    {
        n = table[i];
        while (n != NULL)
        {
            node *temp = n;
            n = n->next;
            free(temp);
        }
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }

    return false;
}
