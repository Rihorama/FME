#pragma once
#include "player.h"
#include "card.h"
#include "deck.h"
#include <vector>


class Game {
private:
    //std::vector<Player> players
    Deck                deck;       //deck of playing cards
    std::vector<Card*>  discarded;  //pile of discarded cards
    cardType            topType;    //type of top discarded card
    cardColor           topColor;   //color of top discarded card
    std::vector<Player> players;    //participants of the game
    int                 turn;       //number of current turn

    void    dealCards();            //each player gets 4 cards from the deck
    void    updateTop();            //updates topType and topColor with actual values
    Card    *drawFromDeck();        //draws a card / if deck empty, discarded pile = new deck
    bool    checkWin(int i);        //check player i for empty hand
    void    proceedWin(int i);      //winner confirmed, final print etc.

    void    printTurn();
    void    printPlayerHeader(int i);
    void    printCardPlayed(std::string event);
    void    printStatus(int i);

    void    redSevenYes(int i, int winIndex, int draw2);//events when red 7 played
    void    redSevenNo(int i, bool skip);        //events if red 7 can't be played
    void    aceYes(int i);                       //events when ace not surpassed
    void    sevenYes(int i, int draw2);          //events when seven not surpassed
    void    knaveYes(int i);                     //knave played
    void    cannotPlayYes(int i);                //events if player can't play
    void    lastRoundYes(int i, int preWinIndex);//events if last round starts
    void    lastRoundSkipYes(int i);             //events if player has only one card
                                                 //during last round -> must be skipped

public:
            Game(int playerCnt);
    int     play();                 //main playing method
};