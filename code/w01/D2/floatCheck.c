#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define EPSILON 1e-6f // 0.000001
int numberCheckFloat(float number){
    if(number>EPSILON){
        return 1;
    }else if(number<-EPSILON){
        return -1;
    }
    return 0;
}

int numberCheck(float number){
    if(number>0){
        return 1;
    }else if(number==0){
        return 0;
    }
    return -1;
}


int main(void){
    float number = 0.3f - 0.2f - 0.1f;
    printf("Calculation: %.15f\n", number);
    printf("Direct: %d\n", numberCheck(number));
    printf("Epsilon: %d\n\n", numberCheckFloat(number));

    float values[] = {-2e-6f, -EPSILON, -1e-7f, 0.0f,
                       1e-7f, EPSILON, 2e-6f};
    printf("%18s %10s %10s\n", "number", "direct", "epsilon");
    for(int i = 0; i < 7; i++){
        printf("%18.10f %10d %10d\n",
               values[i], numberCheck(values[i]),
               numberCheckFloat(values[i]));
    }
    return 0;
}
