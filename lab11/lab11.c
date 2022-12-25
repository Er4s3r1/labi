#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include <stdlib.h>


typedef enum State {
    NewWord,
    Rubbish,
    Word
} State; 


bool is_NewWord (char symbol) {
    return (symbol == '\n' || symbol == '\t' || symbol == ',' || symbol == ' ') ? true : false;
}


bool is_Letter (char symbol) {
    return (symbol >= 'a' && symbol <= 'z') ? true : false;
}


void printWord (int size, char word [size]) {
    for (int i = 0; i < size; i++) {
        printf("%c", word [i]);
    }
    printf("\n");
}


void CaesarDecoder (int size, char word [size], int right_move) {
    if (right_move == 26) {
        printWord(size, word);
        return;
    }
    char alphabet [26] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    int letter_index;
    for (int i = 0; i < size; i++) {
        letter_index = (((word [i] - 'a') + right_move) > 25) ? 
        ((word [i] - 'a') + right_move) % 26 : ((word [i] - 'a') + right_move);
        word [i] = alphabet [letter_index];
    }
    printWord(size, word);
}


int main () {
    State state = NewWord;
    char symbol = '0', *word;
    int length = 0, max_length = 100, word_index = 1;
    word = (char *) malloc(max_length);
    assert(is_NewWord(' '));
    assert(!is_NewWord('a'));
    assert(is_Letter('a'));
    assert(!is_Letter('%'));
    while ((symbol = getchar()) != EOF) {
        switch (state) {
            case NewWord:
                if (is_NewWord(symbol)) {
                    length = 0;
                    break;
                }
                if (is_Letter(symbol)) {
                    word [length] = symbol;
                    length++;
                    state = Word;
                }
                else {
                    state = Rubbish;
                }
                break;
            case Rubbish:
                if (is_NewWord(symbol)) {
                    state = NewWord;
                }
                break;
            case Word:
                if (is_Letter(symbol)) {
                    if (length >= max_length) {
                        max_length *= 2;
                        word = (char *) realloc(word, max_length);
                    }
                    word [length] = symbol;
                    length++;
                    break;
                }
                if (is_NewWord(symbol)) {
                    if (word_index > 26) {
                        word_index = 1;
                    }
                    CaesarDecoder(length, word, word_index);
                    word_index++;
                    length = 0;
                    state = NewWord;
                    break;
                }
                state = Rubbish;
                length = 0;
                break;
            default:
                break;
        }
    }
    printf("\n");
    if (length != 0) {
        CaesarDecoder(length, word, word_index);
    }
    free(word);
    return 0;
}