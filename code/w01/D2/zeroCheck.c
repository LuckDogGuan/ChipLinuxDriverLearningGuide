#include <stdio.h>
#include <string.h>

int main(void){
    int a = 0;
    char b = '0';
    char c[] = "0";
    char d = '\0';

    // Value, storage size and hexadecimal representation
    printf("0    : value=%d, sizeof=%zu, hex=0x%X\n", a, sizeof a, (unsigned)a);
    printf("'0'  : value=%d, sizeof=%zu, hex=0x%02X\n", b, sizeof b, (unsigned char)b);
    printf("\"0\"  : text=%s, sizeof=%zu, strlen=%zu\n", c, sizeof c, strlen(c));
    printf("       bytes: %02X %02X\n", (unsigned char)c[0], (unsigned char)c[1]);
    printf("'\\0' : value=%d, sizeof=%zu, hex=0x%02X\n", d, sizeof d, (unsigned char)d);

    // Character constants in C have type int
    printf("Literal sizes: 0=%zu, '0'=%zu, \"0\"=%zu, '\\0'=%zu\n",
           sizeof(0), sizeof('0'), sizeof("0"), sizeof('\0'));

    printf("0 == '\\0': %d\n", a == d);
    printf("0 == '0' : %d\n", a == b);
    printf("'0' - '0': %d\n", b - '0');

    char str[] = {'A', '\0', 'B', '\0'};
    printf("Embedded NUL: text=%s, sizeof=%zu, strlen=%zu\n",
           str, sizeof str, strlen(str));
    return 0;
}
