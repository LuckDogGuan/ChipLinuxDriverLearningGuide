#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    bool ready = true;

    printf("CHAR_BIT = %d\n", CHAR_BIT);
    printf("sizeof(char) = %zu\n", sizeof(char));
    printf("sizeof(int) = %zu\n", sizeof(int));
    printf("sizeof(long) = %zu\n", sizeof(long));
    printf("sizeof(long double) = %zu\n", sizeof(long double));
    printf("sizeof(uint32_t) = %zu\n", sizeof(uint32_t));
    printf("INT_MIN = %d, INT_MAX = %d\n", INT_MIN, INT_MAX);
    printf("ready = %d\n", ready);
    return 0;
}