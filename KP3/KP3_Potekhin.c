#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <limits.h>
#include <assert.h> 

int main () {
    int n, count = 1;
    long double Taylor, fuction, left = 0.0, right = 0.5, x = left, eps = 1.0;
    while (1.0L + eps > 1.0L) {
        eps /= 2.0L;
    }
    printf("Machine epsilon for long double is %.16Le\n", eps);
    printf("Write n: ");
    scanf("%d", &n);
    assert(n >= 0);
    printf("Your n is %d\n", n);
    printf("Table of values for Taylor's Formula and f(x) = ln((1 + x) / (1 - x))\n");
    printf("|-------------------------------------------------------------------|\n");
    printf("|    x   |        Taylor        |          f(x)        | iterations |\n");
    printf("|-------------------------------------------------------------------|\n");
    for (int i = 1; i <= n + 1; i++) {
        Taylor = 2 * x;
        fuction = logl((1 + x) / (1 - x));
        count = 1;
        while (fabsl(Taylor - fuction) > eps && count <= 100) {
            Taylor += 2 * ((powl(x, (count * 2) + 1)) / ((count * 2) + 1));
            count++;
        }
        count--;
        if (count >= 0 && count <=9) {
            printf("| %.4Lf | %.18Lf | %.18Lf |     %d      |\n", x, Taylor, fuction, count);
        }
        if (count >= 10 && count <= 99) {
            printf("| %.4Lf | %.18Lf | %.18Lf |     %d     |\n", x, Taylor, fuction, count);
        }
        if (count == 100) {
            printf("| %.4Lf | %.18Lf | %.18Lf |     %d    |\n", x, Taylor, fuction, count);
        }
        printf("|-------------------------------------------------------------------|\n");
        x += (right - left) / n;
    }

    return 0;
}