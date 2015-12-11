#pragma once
#include "game.h"
#include "player.h"
#include "card.h"
#include "deck.h"
#include <vector>
#include <iostream>
#include <string>

std::vector<char> colorSymb{ 'H', 'D', 'C', 'S', '-' };

std::vector<std::string> typeSymb{ "7", "8", "9", "10", "J", "Q", "K", "A", "-" };

Game::Game(int playerCnt) {

    playerType pType = HUMAN;    

    //creates new Player instance
    //first is always HUMAN type, rest is AI
    for (int i = 0; i < playerCnt; i++) {
        players.push_back(Player(i, pType));
        pType = AI;
    }

    dealCards();
    discarded.push_back(deck.drawCard());  //starts the discarded deck
    updateTop();
    turn = 0;
}


void    Game::dealCards() {

    //four rounds, each player gets a card from deck in every round
    for (int i = 0; i < int(players.size()) * 4; i++) {
        players[i%players.size()].drawCard(drawFromDeck()); //i modulo players cnt
    }
}


//updates topType and topColor variables with the actual values
void    Game::updateTop() {

    topType = discarded.back()->getType();
    topColor = discarded.back()->getColor();
}



//ensures that drawCard is not called on empty deck
//if deck is empty, it is replaced by the discarded pile
//only the top card of discarded pile remains
Card    *Game::drawFromDeck() {

    if (deck.isEmpty()) {
        Card* top = discarded.back();
        discarded.pop_back();
        deck.reassign(discarded);
        discarded.clear();
        discarded.push_back(top);
    }
    return deck.drawCard();
}



/////////////////////////////
//MAIN GAMEPLAY METHOD
/////////////////////////////
int     Game::play() {

    bool skip = false;
    int draw2 = 0;
    bool win = false;
    bool winFin = false;
    bool winFailed = false;
    int winIndex = -1; //index of winning player
    int preWinIndex = -1; //index of previous-to-winner player
    
    while (1) {
        turn++;
        printTurn();

        //cycle over players
        for (int i = 0; i < players.size(); i++) {
            printPlayerHeader(i); //prints which player is on move + top card


            //player must draw 2 cards because seven was played, can't surpass
            //separate if in case red seven player gets to draw two cards
            bool hasSeven;
            if (draw2 && !(hasSeven = players[i].playCard(SEVEN, IGNORE_C))) {
                sevenYes(i, draw2);
                draw2 = 0;
            }
            //if the check above put seven in CardToPlay AND draw2 is true
            //we put it back because it is to be dealt with on another place
            else if (draw2 && hasSeven) {
                players[i].cardBackInHand();
            }


            //if this player can play red seven, winner is back in game
            //either HEARTS or DIAMONDS can be used, both specify color red
            if (win && i == preWinIndex) {
                if (players[i].playCard(SEVEN, HEARTS) && !skip) {
                    redSevenYes(i, winIndex, draw2);
                    win = false;
                    winFailed = true;
                    winIndex = -1;
                    preWinIndex = -1;
                }
                else {
                    redSevenNo(i, skip);
                    winFin = true;
                }            
            }
            //if another player would empty their hand in the last round -> skipped
            else if (win && players[i].handCount() == 1) {
                lastRoundSkipYes(i);
                continue;
            }
            //player must be skipped because ace was played, can't surpass
            else if (skip && !players[i].playCard(ACE, IGNORE_C)) {
                skip = false;
                aceYes(i);
                continue;
            }
            
            if (winFin) {
                proceedWin(winIndex);
                return 0;
            }

            //player can play -> discards a card -> discarded pile
            //if draw2 still true at this time = seven prepared to be discarded
            if (skip || draw2 || players[i].canPlay(topType, topColor)) {

                discarded.push_back(players[i].discardCard());
                updateTop();

                //ace surpassed by own ace
                if(skip){
                    printCardPlayed("ACE surpassed");
                }
                //seven surpassed by own seven
                else if (draw2) {
                    printCardPlayed("SEVEN surpassed");
                    draw2++;
                }
                else if (topType == SEVEN) {
                    printCardPlayed("SEVEN played");
                    draw2++;
                }
                //if skip = true, the top ace was played by us as a surpass 
                else if (topType == ACE && !skip) {
                    printCardPlayed("ACE played");
                    skip = true;
                }
                else if (topType == KNAVE) {
                    knaveYes(i);
                }
                else {
                    printCardPlayed("CARD played");
                }

                //checking winning conditions
                if (checkWin(i)) {
                    win = true;
                    winIndex = i;
                    preWinIndex = (players.size() + winIndex - 1) % players.size();
                    //last round starts now
                    lastRoundYes(i, preWinIndex);
                }

            }
            //if player cannot play, they must draw a card
            else {
                if (!winFailed) {      //does not apply for failed winner
                    cannotPlayYes(i);  //he already got two cards -> plays next
                    winFailed = false;
                }
            }
            printStatus(i);
        }
    }
}

//checking winning conditions
bool    Game::checkWin(int i) {

    return (players[i].handCount() == 0);
}


//winner final
void    Game::proceedWin(int i) {

    players[i].printWin();
    std::cin.ignore();
    std::cin.get();  //waits for user key press
}


//prints turn info
void    Game::printTurn() {

    std::cout << "\n==============\n";
    std::cout << "TURN " << turn << "\n";
    std::cout << "==============\n";
}


//prints player-on-move + top card info
void    Game::printPlayerHeader(int i) {

    std::cout << "-----------\n";
    if (i == 0) {
        std::cout << "YOU\n";
    }
    else {
        std::cout << "PLAYER " << i << "\n";
    }
    std::cout << "-----------\n";
    std::cout << "TOP CARD: ";
    //custom print because of Knave color changes
    //which do not reflect existing card objects
    std::cout << typeSymb[topType] << '[' << colorSymb[topColor] << ']';
    std::cout << "\n";
}


//universal "EVENT: <event> : card" print
void    Game::printCardPlayed(std::string event) {

    std::cout << "EVENT: " << event << ": ";
    discarded.back()->printCard();
    std::cout << "\n";
}



void    Game::printStatus(int i) {
    std::cout << "STATUS: " << players[i].handCount() << " cards\n\n";
    std::cin.get();
}


//events if red seven played
void    Game::redSevenYes(int i, int winIndex, int draw2) {

    discarded.push_back(players[i].discardCard());
    updateTop();
    std::cout << "EVENT: RED SEVEN played!: ";
    discarded.back()->printCard();
    std::cout << "\n";
    std::cout << "EVENT: WIN surpassed!\n";
    //almost-winner draws two cards - or more, if red seven
    //was part of seven stack
    for (int j = 0; j < draw2 + 1; j++) {
        players[winIndex].drawCard(drawFromDeck());
        players[winIndex].drawCard(drawFromDeck());
    }
    std::cout << "EVENT: PLAYER " << winIndex << " draws 2 cards! Back in game!\n";
}


//events if red seven can't be played
void    Game::redSevenNo(int i, bool skip) {
    if (skip) {
        std::cout << "EVENT: PLAYER " << i << " skipped. Can't play RED SEVEN.\n";
    }
    else {
        std::cout << "EVENT: PLAYER " << i << " doesn't have RED SEVEN.\n";
    }
}


//events if ace not surpassed
void    Game::aceYes(int i) {

    std::cout << "EVENT: Skipped\n";
    std::cout << "STATUS: " << players[i].handCount() << " cards\n\n";
    std::cin.get();
}


//events when seven not surpassed
void    Game::sevenYes(int i, int draw2) {

    for (int j = 0; j < draw2; j++) {    //for stacked sevens
        players[i].drawCard(drawFromDeck());
        players[i].drawCard(drawFromDeck());
    }
    std::cout << "EVENT: Draws " << draw2 * 2 << " cards\n";
}


//events when knave played
void    Game::knaveYes(int i) {

    printCardPlayed("KNAVE played");

    //updates top info variables
    topColor = players[i].pickColor();
    topType = IGNORE_T;
    std::cout << "EVENT: Color set: " << colorSymb[topColor] << "\n";
}


//events when player cannot play
void    Game::cannotPlayYes(int i) {

    players[i].drawCard(drawFromDeck());
    std::cout << "EVENT: Cannot play, draws a card\n";
}


//events when last round starts
void    Game::lastRoundYes(int i, int preWinIndex) {

    std::cout << "STATUS: PLAYER " << i << " empty handed. Last round starts now.\n";
    std::cout << "STATUS: PLAYER " << preWinIndex << " can stop PLAYER " << i << \
        " by playing RED SEVEN. Good luck!\n";
}


//events when player has only one card during last turn
//will be skipped
void    Game::lastRoundSkipYes(int i) {

    std::cout << "EVENT: Cannot play during last round if only one card in hand.\n";
    std::cout << "EVENT: Skipped.\n";
    std::cout << "STATUS: " << players[i].handCount() << " cards\n\n";
    std::cin.get();
}



