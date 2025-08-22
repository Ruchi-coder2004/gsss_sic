#include<stdio.h>

void my_function(int n){
    //double arr[40] = {0.0};
    printf("Function call : %d\n",n);
    my_function(n+1);
}

void main(){
    my_function(1);
}