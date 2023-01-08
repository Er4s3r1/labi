#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <stdbool.h>
#include <ctype.h>

bool is_NewWord (char symbol) {
    return (symbol == '\n' || symbol == '\t' || symbol == ',' || symbol == ' ') ? true : false;
}

int main () {
    char letter, previous_letter = '0';
    bool flag = true;
    int set1 = 0, set2 = 0;
    assert(is_NewWord('\n') == true);
    assert(is_NewWord('\t') == true);
    assert(is_NewWord('a') == false);
    while ((letter = getchar()) != EOF) {
        letter = tolower(letter);
        if (is_NewWord(letter)) {
            if ((set1 == 0 && set2 == 0) || is_NewWord(previous_letter)) {
                continue;
            }
            if (flag) {
                flag = false;
                continue;
            }
            if (set1 != set2) {
                printf("Yes\n");
                return 0;
            }
            if (set2 != 0) {
                set1 = set2;
                set2 = 0;
            }
            continue;
        }
        if (flag) {
            set1 |= 1 << (letter - 'a');
        }
        else {
            set2 |= 1 << (letter - 'a');
        }
        previous_letter = letter;
    }
    (set1 != set2 && set1 != 0 && set2 != 0) ? printf("\nYes\n") : printf("\nNo\n");
    return 0;
}