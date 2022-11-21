#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int pairDifference (int size, int array [size]) {
    int a, b, summ = 0;
    for (int i = 0; i < size; i++) {
        scanf("%d%d", &a, &b);
        summ += fmax(a, b);
        array [i] = abs(a - b);
    }
    return summ;
}

void bubbleSort (int size, int array [size]) {
    for (int i = 0 ; i < size - 1; i++) {
       for (int j = 0 ; j < size - i - 1 ; j++) {  
           if (array [j] > array [j+1]) {           
              int tmp = array [j];
              array [j] = array [j+1];
              array [j+1] = tmp; 
            }
       }
    } 
}

int main () {
    int size;
    scanf("%d", &size);
    int array [size];
    int summ = pairDifference(size, array);
    bubbleSort(size, array);
    int i = 0;
    while (summ % 3 != 0) {
        if ((summ - array [i]) % 3 == 0) {
            summ -= array [i];
            break;
        }
        i++;
    }
    if(i >= size) {
        printf("Среди данных пар невозможно собрать число, делящиеся на 3");
        return 0;
    }
    printf("%d\n", summ);
    return 0;
}