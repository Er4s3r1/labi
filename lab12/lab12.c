#include <stdio.h>
#include <assert.h>
#include <stdbool.h>

bool bitEqual (int number) {
    int summ0 = 0, summ1 = 1;
    bool flag = false;
    for (int i = 31; i >= 0; i--) {
        if (!flag) {
            if ((number & (1 << i)) > 0) {
                flag = true;
            }
            continue;
        }
        else {
            ((number & (1 << i)) > 0) ? ++summ1 : ++summ0;
        }
    }
    return (summ0 == summ1) ? true : false;
}

int main() {
    assert(!bitEqual(65535));
    assert(!bitEqual(131070));
    assert(bitEqual(2));
    int number;
    scanf("%d", &number);
    (bitEqual(number)) ? printf("Yes\n") : printf("No\n");
    return 0;
}