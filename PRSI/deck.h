#pragma once
#include "card.h"
#include <vector>
#include <algorithm>

class Deck {
private:
    void shuffle();
public:
    std::vector<Card> playingCards;  //where the objects are stored
    std::vector<Card*> deck;        //deck size of 32 cards
    Deck();
    bool isEmpty();
    int getSize();
    Card *drawCard();
    void reassign(std::vector<Card*>);
};