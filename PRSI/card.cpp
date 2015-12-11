#include "card.h"
#include <vector>

std::vector<std::string> typeSymbols { "7", "8", "9", "10", "J", "Q", "K", "A", "-" };

std::vector<char> colorSymbols { 'H', 'D', 'C', 'S', '-' };


cardType Card::getType() {
    return type;
}


cardColor Card::getColor() {
    return color;
}


void    Card::printCard() {
    std::cout << typeSymbols[int(type)] << '[' << colorSymbols[int(color)] << ']';
}


//arguments: color and type of top card on the desk
//true if playable card present in hand
//prints the hand either way
bool    Card::printCard(cardType t, cardColor c) {

    //if card can be played, it is displayed with a star
    if (c != IGNORE_C && (t == type || c == color || type == KNAVE)) {
        std::cout << '*' << typeSymbols[int(type)] << '[' << colorSymbols[int(color)] << ']';
        return true;
    }
    //ace and seven surpass option must not allow knave
    else if (c == IGNORE_C && t == type) {
        std::cout << '*' << typeSymbols[int(type)] << '[' << colorSymbols[int(color)] << ']';
        return true;
    }
    else {
        std::cout << typeSymbols[int(type)] << '[' << colorSymbols[int(color)] << ']';
    }

    return false;
}


//true if this card is compatible with top card on the desk
bool    Card::isPlayable(cardType t, cardColor c) {

    if (t == type || c == color || type == KNAVE) {
        return true;
    }
    return false;
}