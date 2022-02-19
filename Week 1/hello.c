#include <stdio.h>
#include <cs50.h>

// Declare variable to set the name of user.
string name;

int main(void)
{
    name = get_string("What is your name?\n");
    printf("hello, %s\n", name);
}
