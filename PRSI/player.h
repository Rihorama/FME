#pragma once
#include "card.h"
#include <vector>
#include <iostream>

enum playerType {
    HUMAN = 0,
    AI
};

class Player {
private:
    int                 id;                //player's id within the game
    std::vector<Card*>  hand;              //cards in player's hand
    playerType          type;              //is controled by human or AI
    Card*               cardToPlay = NULL; //card chosen to play or used for manipulation
    Card*               knave = NULL;      //if AI needs to keep Knave for a while
    int                 knaveIndex;

    //AI part
    bool      canPlayAI(cardType t, cardColor c);
    bool      playCardAI(cardType t, cardColor c);   //for surpassing seven/ace by AI
    cardColor pickColorAI();

    //HUMAN part
    bool      canPlayHuman(cardType t, cardColor c);
    bool      printHand(cardType t, cardColor c);
    int       askMove(cardType t, cardColor c);
    bool      playCardHuman(cardType t, cardColor c); //for surpassing seven/ace by player 
    cardColor pickColorHuman();
    
public:
    Player(int i, playerType t) : id(i), type(t) { };
    void        drawCard(Card* newCard);            //new card put in the hand
    bool        canPlay(cardType t, cardColor c);   //does player have playable card?
    Card*       discardCard();                      //cardToPlay returned
    void        printWin();                         //prints winning message
    int         handCount();                        //how many cards in hand
    bool        playCard(cardType t, cardColor c);  //for surpassing seven/ace
    cardColor   pickColor();                        //requests picking a color
    void        cardBackInHand();                   //cardToPlay put back in hand
                                                
};