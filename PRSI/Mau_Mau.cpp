#include "game.h"
#include <iostream>
#include <string>


std::string rules = \
"======================================================\n\
SIMPLE MAU-MAU CONSOLE GAME / Czech \"PRSI\" variation\n\
======================================================\n\
\n\
Author: Alice Minarova, 2015\n\
\n\
-----------\n\
-- RULES --\n\
-----------\n\
1. DECK: 32 cards.\n\
2. Each player dealt 4 cards at the beginning.\n\
3. Initial card put on a discarded pile\n\
4. Player on the move must play card:\n\
      a) of the same color (H-hearts, D-diamonds, C-clubs, S-spades)\n\
      b) of the same type (7,8,9,10,J,Q,K,A)\n\
      c) of a special meaning (7,J,A)\n\
5. Played card becomes the top of the discarded pile.\n\
6. If unable to play, Player must draw a card.\n\
7. SPECIAL CARDS:\n\
      a) SEVEN - the next player must draw 2 cards\n\
      b) ACE - the next player cannot play that turn\n\
      c) JACK - can be played on any card\n\
              - doesn't beat SEVEN or ACE effect\n\
8. Both ACE and SEVEN can be surpassed by playing same type card.\n\
      a) SEVEN - for each surpass two extra cards will be drawn\n\
               - e.g: P1 - SEVEN, P2 - SEVEN, P3 draws 4 cards\n\
      b) ACE - surpass only passes \"skip\" to another player\n\
9. The first player to have empty hand starts Last Round.\n\
      +) Last Round follows normal rules with few exceptions\n\
      +) If player has only one card in hand, he is skipped\n\
      +) Player previous to the empty-handed player must play\n\
         RED SEVEN in order to put empty-handed player back\n\
         in game.\n\
10.If empty-handed player is not forced back in game, HE WINS!\n\
\n\
\n\
-----------------\n\
-- GAME FORMAT --\n\
-----------------\n\
1. CARD: J[H] = Heart Jack\n\
2. YOUR HAND: 0. J[H] | 1. 8[D] | 2. *Q[S] |\n\
              ^ card index           ^ can be played\n\
3. Use the given card index to play the respective card.\n\
4. Asterisk (*) marks cards that can be played.\n\
5. ENTER to proceed each player's move.\n\
\n\n\
GOOD LUCK!\n\n\n";


int main()
{
    std::cout << rules;
    Game game(4);
    std::cin.get();
    game.play();

    return 0;
}

