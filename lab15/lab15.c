#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

void getSumm (int size, int matrix [size] [size]) {
    int max = 0, row_index = 0, result = 0;
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            scanf("%d", &matrix [i] [j]);
            if (matrix [i] [j] > max || (i == 0 && j ==0)) {
                max = matrix [i] [j];
                row_index = i;
            }
        }
    }
    for (int j = 0; j < size; j++) {
        result += matrix [row_index] [j];
    }
    printf("%d\n", result);
}

int main () {
    int size;
    scanf("%d", &size);
    assert(size > 0 && size < 9);
    int matrix [size] [size];
    getSumm(size, matrix);

    return 0;
}