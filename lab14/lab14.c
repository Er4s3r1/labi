#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

void getMatrix (int size, int matrix [size] [size]) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            scanf("%d", &matrix [i] [j]);
        }
    }
}

void printWay (int size, int matrix [size] [size]) {
    int i = size - 1, j = 0, z;
    for (int k = (size * 2) - 1; k > 0; k--) {
        for (z = 0; z < (k / 2) + (k % 2); z++) {
            printf("%d ", matrix [i] [j]);
            if (k % 2 == 1) {
                i--;
                j++;
            }
            else {
                i++;
                j--;
            }
        }
        if (k % 2 == 1) {
            i += (((size * 2) - k) / 2) + (((size * 2) - k) % 2) + 1;
            j = size - 1;
        }
        else {
            i -= (((size * 2) - k) / 2) + (((size * 2) - k) % 2) + 1;
            j = 0;
        }
    }
    printf("\n");
}

int main () {
    int size;
    scanf("%d", &size);
    assert(size > 0);
    int matrix [size] [size];
    getMatrix(size, matrix);
    printWay(size, matrix);
    
    return 0;
}