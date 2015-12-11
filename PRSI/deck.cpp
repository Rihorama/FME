#include "deck.h"
#include <cstdlib>
#include <ctime>


//creates a deck of 32 different cards
Deck::Deck() {
    for (int c = HEARTS; c <= SPADES; c++) {
        for (int t = SEVEN; t <= ACE; t++) {
            //creates "physical" Card object
            playingCards.push_back(Card(cardType(t), cardColor(c)));     
        }
    }
    //deck filled with card pointers
    for (int i = 0; i < playingCards.size(); i++) {
        deck.push_back(&playingCards[i]);
    }
    //and shuffled
    shuffle();
}

//empty-checking
bool Deck::isEmpty() {
    return deck.empty();
}


int Deck::getSize() {
    return deck.size();
}


//removes card from the deck and returns it
//must be checked for being empty before!
Card *Deck::drawCard() {
    Card *c = deck.back();
    deck.pop_back();
    return c;
}


//replaces deck with the given one and shuffles
void Deck::reassign(std::vector<Card*> d) {
    deck = d;
    shuffle();
}


//shuffles the deck (x-times where x is 1-20)
void Deck::shuffle() {
    std::srand(std::time(NULL));
    int random = rand() % 20 + 1;
    std::cout << "EVENT: Deck shuffled " << random << " times.\n";

    for (int i = 0; i < random; i++) {
        std::random_shuffle(deck.begin(), deck.end());
    }
}