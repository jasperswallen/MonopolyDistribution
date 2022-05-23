"""
Module containing the Monopoly class, which can play a single-player simulated
game of Monopoly
"""

from typing import List

import random


class Monopoly:
    """
    The class responsible for a singular game of Monopoly
    """

    NUM_SPACES = 40
    """
    The total number of spaces in a Monopoly board
    """

    JAIL_SPACE = 10
    """
    The location of the jail, 0-indexed (from Go)
    """

    CHANCE_SPACES = [7, 22, 36]
    """
    The location of the chance draws, 0-indexed (from Go)
    """

    TO_JAIL_SPACE = 30
    """
    The location of the instant-jail space, 0-indexed (from Go)
    """

    ORIGINAL_CHANCE_CARDS = 16
    """
    The number of chance cards to draw from, at the beginning of the game

    It is assumed that only this player draws from the Chance cards
    """

    def __init__(self) -> None:
        """
        Initialize all variables for keeping track of moves, current location,
        and various probabilities
        """

        random.seed()

        self.in_jail = False
        self.current_position = 0
        self.jail_card_drawn = False
        self.chance_cards_drawn = 0
        self.num_consecutive_doubles = 0
        self.num_jail_turns = 0

        self.spaces_landed: List[int] = [0 for _ in range(self.NUM_SPACES)]

        assert len(self.spaces_landed) == self.NUM_SPACES

    def get_distribution(self) -> List[int]:
        """
        Get the distribution of spaces landed on during the course of a game
        """

        return self.spaces_landed

    def play_turn(self) -> None:
        """
        Play a single turn, keeping track of the spaces landed on.

        When in jail, attempt to get out of jail only by rolling dice. Assume
        that you do not have enough money and do not have a get-out-of-jail-free
        card (TODO)

        When not in jail, roll two dice, and move to the position of the sum of
        those dice after your current position. If the two dice are the same,
        keep rolling after performing the function of this space.

        If you roll two of the same value three times in a row (for example,
        3 3, 4 4, 1 1), go directly to jail without performing the function of
        the final space you landed on.

        If you land on a chance space, "draw" a card. There are 16 chance cards
        at the beginning of the game. 1 of these cards is a go-directly-to-jail
        card. When a card is drawn, it is not replaced. If you "draw" the jail
        card, go directly to jail. Otherwise, "discard" this card, and continue
        with your turn.

        If you land on the TO_JAIL_SPACE, go directly to jail.

        When going to jail, your turn immediately ends.
        """

        if self.in_jail:
            # currently in jail

            self.num_jail_turns += 1

            roll_one = random.randint(1, 6)
            roll_two = random.randint(1, 6)

            if roll_one == roll_two or self.num_jail_turns >= 3:
                # move forward this many spaces, but immediately end your turn
                # otherwise (unless it is a chance card)
                self.in_jail = False

                self.current_position += roll_one + roll_two
                self.current_position %= self.NUM_SPACES
                self.spaces_landed[self.current_position] += 1

                if self._check_chance_card():
                    return
        else:
            # not currently in jail

            self.num_consecutive_doubles = 0
            roll_one = 0
            roll_two = 0

            while roll_one == roll_two:
                roll_one = random.randint(1, 6)
                roll_two = random.randint(1, 6)

                if roll_one == roll_two:
                    self.num_consecutive_doubles += 1
                    if self.num_consecutive_doubles >= 3:
                        # go to jail and end your turn without counting this space
                        self._go_to_jail()
                        return

                self.current_position += roll_one + roll_two
                self.current_position %= self.NUM_SPACES
                self.spaces_landed[self.current_position] += 1

                if self._check_chance_card():
                    return

                if self.current_position == self.TO_JAIL_SPACE:
                    self._go_to_jail()
                    return

    def _go_to_jail(self) -> None:
        """
        Helper function to clean up variables when going to jail
        """

        self.current_position = self.JAIL_SPACE
        self.in_jail = True
        self.num_jail_turns = 0

    def _check_chance_card(self) -> bool:
        """
        If we landed on a Chance card pickup, check to see if we picked up the
        go-straight-to-jail card. Otherwise, discard this card.

        @return True if we went to jail by drawing the card, False otherwise
        """

        if not self.jail_card_drawn and self.current_position in self.CHANCE_SPACES:
            # landed on a chance space and could go to jail
            if random.randint(1, self.ORIGINAL_CHANCE_CARDS - self.chance_cards_drawn) <= 1:
                self._go_to_jail()
                self.jail_card_drawn = True

            self.chance_cards_drawn += 1
            return self.jail_card_drawn

        return False
