#include "player.h"
#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

//for comparing cardColor variables for RED/BLACK
std::vector<char> colorAffinity{ 'R', 'R', 'B', 'B', '-' };


//a new card added to player's hand
void    Player::drawCard(Card *newCard) {
    hand.push_back(newCard);
}


//called as a deciding method, if the player has a suitable
//card to discard, that meets the requirements given by
//the card that is on top of the discard pile
//
//the chosen card is removed from hand and put separately
//in the variable "cardToPlay"
bool    Player::canPlay(cardType t, cardColor c) {
    if (type == AI) {
        return canPlayAI(t, c);
    }
    else {
        return canPlayHuman(t, c);
    }
}


//returns card prepared in cardToPlay variable
//!!CAN BE CALLED IMMEDIATELY AND ONLY AFTER canPlay() RETURNS TRUE!!
//(else unexpected behavior, possible duplication of cards in game etc)
Card    *Player::discardCard() {
    return cardToPlay;
}


void    Player::printWin() {
    if (type == HUMAN) {
        std::cout << "\n\n\nYOU WIN!\n";
    }
    else {
        std::cout << "\n\n\nPLAYER " << id << " WINS!\n";
    }
}

//returns number of cards in hand
int     Player::handCount() {
    return hand.size();
}


//gives player a chance to beat seven on discarded deck by own seven
//true if can play
bool    Player::playCard(cardType t, cardColor c) {
    //playCardAI also used to automaticaly play red7 from human hand
    if (type == AI || t == IGNORE_T) {
        return playCardAI(t, c);
    }
    else {
        return playCardHuman(t, c);
    }
}

//asks for color change
cardColor Player::pickColor() {
    if (type == AI) {
        return pickColorAI();
    }
    else {
        return pickColorHuman();
    }
}


//when player with one card skipped during Last Round (his only card
//must be moved from CardToPlay back in hand
void        Player::cardBackInHand() {
    
    drawCard(cardToPlay);
    cardToPlay == NULL;
}



/////////////////////////////////////////////////////////////////////////////////
///////////////////// ARTIFICIAL INTELLIGENCE PART //////////////////////////////

//represents the Artificial Intelligence for a player
//      --plays first playable card
//        from the xMatchIndex vector
//        with greater cardinality
//      --Seven, Knave or Ace kept as last resort
bool    Player::canPlayAI(cardType t, cardColor c) {

    int             typeMatch = 0;      //how many cards in hand match the given type
    int             colorMatch = 0;     //how many cards match the given color
    std::vector<int>typeMatchIndex;     //indexes of cards matching type
    std::vector<int>colorMatchIndex;    //indexes of cards matching color
    int             knaveIndex = -1;    //index of last Knave in hand
    int             specialIndex = -1;  //index of last Seven/Ace in hand
                                        //will be used if no not special card in hand
          

    //checking for typeMatch (seven, knave and ace excepted)
    if (t != SEVEN && t != ACE && t != KNAVE) {
        for (int i = 0; i < hand.size(); i++) {
            if (hand[i]->getType() == t) {
                //std::cout << "t : cardType " << t << " : " << hand[i]->getType() << "\n";
                typeMatch++;                    //increase counter
                typeMatchIndex.push_back(i);    //store index
            }
        }
    }

    //checking for colorMatch (seven, knave and ace excepted)
    for (int i = 0; i < hand.size(); i++) {

        if (hand[i]->getColor() == c){
            cardType cType = hand[i]->getType();
            
            if (cType == KNAVE) {
                knaveIndex = i;
            }
            else if (cType == SEVEN || cType == ACE) {
                specialIndex = i;
            }
            else {
                colorMatch++;                    //increase counter
                colorMatchIndex.push_back(i);    //store index
            }
        }
    }

    //no normal match found
    if (typeMatch + colorMatch == 0) {
        //we check for Ace/Seven
        if (specialIndex != -1){
            cardToPlay = hand[specialIndex];         //ace/seven present, let's play it
            hand.erase(hand.begin() + specialIndex); //and remove from hand
            return true;
        }
        //last resort: do we have any knave?
        else if (knaveIndex != -1) {
            cardToPlay = hand[knaveIndex];         //knave present, let's play it
            hand.erase(hand.begin() + knaveIndex); //and remove from hand
            return true;
        }
        //nothing to play, too bad
        else {
            return false;
        }
    }


    //non-special match found
    int i;
    if (typeMatch >= colorMatch) {
        i = typeMatchIndex.front();  //first playable card index
    }
    else {                           //(colorMatch > typeMatch)
        i = colorMatchIndex.front(); //first playable card index
    }

    cardToPlay = hand[i];
    hand.erase(hand.begin() + i);    //and remove from hand
    return true;
}


//managing SEVEN/ACE surpassing situation for AI
//true if seven/ace in hand
//seven/ace -> cardToPlay
bool    Player::playCardAI(cardType t, cardColor c) {
    for (int i = 0; i < hand.size(); i++) {

        cardType cType = hand[i]->getType();
        cardColor cColor = hand[i]->getColor();

        //we don't care about color
        if (c == IGNORE_C && cType == t) {
            cardToPlay = hand[i];
            hand.erase(hand.begin() + i);   //removes from hand
            return true;
        }
        //for red seven option, same color as c requested
        else if (c != IGNORE_C && cType == t && \
                 colorAffinity[cColor] == colorAffinity[c]) {
            cardToPlay = hand[i];
            hand.erase(hand.begin() + i);   //removes from hand
            return true;
        }
    }
    return false;
}


//AI picks a color after playing Knave
//picks randomly because who knows what cards will be played next
cardColor Player::pickColorAI() {

    std::srand(std::time(NULL));
    int random = rand() % int(SPADES);

    return cardColor(random);
}




/////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// HUMAN PART /////////////////////////////////////

bool    Player::canPlayHuman(cardType t, cardColor c) {

    bool can = printHand(t, c);
    int i;

    if (!can) {
        return false;
    }

    i = askMove(t, c);              //get index of player-picked card
    cardToPlay = hand[i];           //update cardsToPlay
    hand.erase(hand.begin() + i);   //removes from hand
    
    return true;
}


//prints cards in hand for human player to know the situation
//
bool    Player::printHand(cardType t, cardColor c) {

    bool can = false;
    std::cout << "YOUR HAND:";

    for (int i = 0; i < hand.size(); i++) {

        std::cout << " " << i << ". ";
        can = can | hand[i]->printCard(t,c);   //once we get true -> true till the end
        std::cout << " |";
    }
    std::cout << "\n\n";
    return can;
}


//waits for player's keyboard input
//accepts only number that can be valid Hand index, which is returned
int     Player::askMove(cardType t, cardColor c) {

    std::string input;
    int i;
    bool ok = false;

    std::cout << "Please enter index of card to play...\n";
    std::cin >> input;
    i = int(input[0]) - int('0');  //in case of more than one character, takes the first

    while (!ok) {
        while (i < 0 || i > hand.size() - 1) {
            std::cout << "Wrong input.\n";
            std::cout << "Please enter index of card to play...\n";
            std::cin >> input;
            i = int(input[0]) - int('0'); //first char of string 'inted'
        }

        ok = hand[i]->isPlayable(t, c); //can the picked card be played

        if (!ok) {
            std::cout << "\nSelected card cannot be played, choose another.\n";
            std::cout << "Please enter index of card to play...\n";
            std::cin >> input;
            i = int(input[0]) - int('0'); //first char of string 'inted'
        }
    }
    std::cout << "\n";
    return i;
}

//managing SEVEN/ACE surpassing situation for human
bool    Player::playCardHuman(cardType t, cardColor c) {

    for (int i = 0; i < hand.size(); i++) {
        if (hand[i]->getType() == t && c == IGNORE_C) {
            return canPlayHuman(t, c);
        }
    }
    return false;
}


//asks the human player to set new color
cardColor Player::pickColorHuman() {

    std::string input;
    int i;
    bool ok = false;

    std::cout << "PICK COLOR: 0. H - Hearts | 1. D - Diamonds" <<\
                 " | 2. C - Crosses | 3. S - Spades\n\n";

    std::cout << "Please enter index of color to set...\n";
    std::cin >> input;

    i = int(input[0]) - int('0');  //in case of more than one character, takes the first

    while (i < 0 || i > int(SPADES)) {
        std::cout << "Wrong input.\n";
        std::cout << "Please enter index of color to set...\n";
        std::cin >> input;
        i = int(input[0]) - int('0'); //first char of string 'inted'
    }
    std::cout << "\n";
    return cardColor(i);
}
