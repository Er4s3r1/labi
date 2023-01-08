#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <limits.h>

long double func(long double x) {
    return (x * tanl(x)) - (1.0L / 3.0L);
}

long double func1(long double x) {
    return (cosl(x) * sinl(x) + x) / powl(cosl(x), 2.0L);
}

long double Newton(long double left, long double right) {
    long double x = (left + right) / 2.0L, eps = 1.0L, previous_x;
    while (1.0L + eps > 1.0L) {
        eps /= 2.0L;
    }
    do {
        previous_x = x;
        x -= func(x) / func1(x);
    }
    while (fabsl(x - previous_x) > eps);
    return x;
}

long double g(long double x) {
    return tanl(x / 2.0L) - (1.0L / tanl(x / 2.0L)) + x;
}

long double dichotomy(long double left, long double right) {
    long double eps = 1.0;
    while (1.0L + eps > 1.0L) {
        eps /= 2.0L;
    }
    while (fabsl(right - left) > eps) {
        if ((g(left) * g(left + right) / 2.0L) > 0.0L) {
            left = (left + right) / 2.0L;
            continue;
        }
        right = (left + right) / 2.0L;
    }
    return left + right;
}

int main () {
    printf("Variant 13: %.4Lf\n", Newton(0.2L, 1.0L));
    printf("Variant 14: %.4Lf\n", dichotomy(0.0L, 2.0L));
    return 0;
}