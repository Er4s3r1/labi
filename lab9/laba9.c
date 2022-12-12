#include <stdio.h>
#include <stdbool.h>

int max (int a, int b) {
    return (a >= b) ? a : b;
}

int min (int a, int b) {
    return (a < b) ? a : b;
}

double abss (double a) {
    return (a >= 0) ? a : 0 - a;
}

int sgn(int x) {
    if (x == 0) {
        return 0;
    }
    return (x > 0) ? 1 : -1;
}

double sqrt (double n) { //упрощенная функция корня используя метод Ньютона
    double z = 1;
    double nz;
    for (;;) {
        nz = (z + n / z) / 2;
        if (abss(z - nz) < 1e-10) {
            break;
        }
        z = nz;
    }
    return nz;
}

bool success(int x, int y) {
    int ax = -10, ay = 20, bx = 0, by = 10, cx = -10, cy = 0;
    int pv1 = ((ax * y) - (ay * x));
    int pv2 = ((bx * y) - (by * x));
    int pv3 = ((cx * y) - (cy * x));
    if ((pv1 > 0 && pv2 > 0 && pv3 > 0) || (pv1 < 0 && pv2 < 0 && pv3 < 0)) {
        return true;
    }
    else if ((pv1 == 0 && pv2 * pv3 > 0) || (pv2 == 0 && pv1 * pv3 > 0) || (pv3 == 3 && pv2 * pv1 > 0)) {
        return true;
    }
    else {
        return false;
    }
}

int main() {
    int i = 20, j = 0, l = 11, previous_i, previous_j, previous_l;
    for (int k = 1; k < 50; k++) {
        if (success(i, j)) {
            printf("Óäà÷íî! %d\n", k);
            return 0;
        }
        previous_i = i; previous_j = j; previous_l = l;
        i = ((  ((previous_i - k) * max(previous_j, previous_l)) +
            ((previous_j - k) * min(previous_i, previous_l)) +
            ((previous_l - k) * max(previous_i, k))) % 23);
        j = (-((previous_i - k) * min(previous_j, previous_l)) +
            ((previous_j - k) * max(previous_i, previous_l)) +
            ((previous_l - k) * min(previous_i, previous_j)) % 27);
        l = abs(previous_i + previous_j - previous_l - k) *
            sign(previous_i - previous_j + previous_l - k);
    }
    printf("Íå ïîïàë\n");
    printf("Êîíñòàíòà i: %d\n", previous_i);
    printf("Êîíñòàíòà j: %d\n", previous_j);
    printf("Êîíñòàíòà l: %d\n", previous_l);
    return 0;
}
