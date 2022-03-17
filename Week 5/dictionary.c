// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table.
const unsigned int N = 1000;

// Hash table
node *table[N];

int dictionary_size = 0;

// Returns true if word is in dictionary, else false.
bool check(const char *word)
{
    int hash_value = hash(word);

    node *n = table[hash_value];

    // Go through the node.
    while (n != NULL)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }

        n = n->next;
    }

    // If no word is find.
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary and check if we open properly.
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // Copy dictionary words into a buffer of char.
    char word[LENGTH + 1];

    // Copy words to our table + create hash.
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for each node (word).
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Could not allocate memory for *table.");
            return false;
        }

        // Copy word into our node thanks to strcpy.
        strcpy(n->word, word);

        // Use the hash function.
        int hash_value = hash(word);

        n->next = table[hash_value];
        table[hash_value] = n;

        dictionary_size++;
    }

    // We can now close dictionary file.
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        while (n != NULL)
        {
            // Set a temporary node to not broke our node.
            node *tmp = n;

            n = n->next;
            free(tmp);
        }

        // In case we cleaned all words in node.
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }

    return false;
}
