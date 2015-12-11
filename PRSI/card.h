#pragma once
#include <iostream>
#include <string>

enum cardType { SEVEN = 0,
                EIGHT,
                NINE,
                TEN,
                KNAVE,
                QUEEN,
                KING,
                ACE,
                IGNORE_T
};

enum cardColor {
    HEARTS = 0,
    DIAMONDS,
    CLUBS,
    SPADES,
    IGNORE_C
};

enum colorGroups {
    RED = 0,
    BLACK
};


class Card {
private:
    cardType    type;
    cardColor   color;
public:
    Card(cardType t, cardColor c) : type(t), color(c) { }
    cardType    getType();
    cardColor   getColor();
    void        printCard();
    bool        printCard(cardType t, cardColor c);
    bool        isPlayable(cardType t, cardColor c);
};