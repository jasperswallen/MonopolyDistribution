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

    ORIGINAL_CHANCE_CARDS = 16
    """
    The number of chance cards to draw from, at the beginning of the game

    It is assumed that only this player draws from the Chance cards
    """

    GO_SPACE = 0
    """
    The location of the Go space (the initial location)
    """

    JAIL_SPACE = 10
    """
    The location of the jail, 0-indexed (from Go)
    """

    FREE_PARKING_SPACE = 20
    """
    The location of the free parking space, 0-indexed (from Go)
    """

    TO_JAIL_SPACE = 30
    """
    The location of the instant-jail space, 0-indexed (from Go)
    """

    CHANCE_SPACES = [7, 22, 36]
    """
    The location of the chance draws, 0-indexed (from Go)
    """

    COMMUNITY_CHEST_SPACES = [2, 17, 33]
    """
    The location of the community chest draws, 0-indexed (from Go)
    """

    PROPERTY_SPACES = [
        1,
        3,
        6,
        8,
        9,
        11,
        13,
        14,
        16,
        18,
        19,
        21,
        23,
        24,
        26,
        27,
        29,
        31,
        32,
        34,
        37,
        39,
    ]
    """
    The spaces that have a property on them, 0-indexed (from Go)
    """

    RAILROAD_SPACES = [5, 15, 25, 35]
    """
    The spaces that have a railroad on them, 0-indexed (from Go)
    """

    TAX_SPACES = [4, 38]
    """
    The spaces where the player must pay a tax, 0-indexed (from Go)
    """

    UTILITY_SPACES = [12, 28]
    """
    Utility spaces, 0-indexed (from Go)
    """

    def __init__(self) -> None:
        """
        Initialize all variables for keeping track of moves, current location,
        and various probabilities
        """

        self.in_jail = False
        self.current_position = 0
        self.get_out_of_jail_card_drawn = [False, False]
        self.num_consecutive_doubles = 0
        self.num_jail_turns = 0

        self.chance_cards = list(range(1, 17))
        self.community_chest_cards = list(range(1, 17))

        random.shuffle(self.chance_cards)
        random.shuffle(self.community_chest_cards)

        self.spaces_landed: List[int] = [0 for _ in range(Monopoly.NUM_SPACES)]

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

        If you land on a chance or community chest space, "draw" a card. There
        are 16 chance cards at the beginning of the game. 1 of these cards is a
        go-directly-to-jail card. When a card is drawn, it is not replaced. If
        you "draw" the jail card, go directly to jail. Otherwise, "discard" this
        card, and continue with your turn.

        If you land on the TO_JAIL_SPACE, go directly to jail.

        When going to jail, your turn immediately ends.
        """

        if self.in_jail:
            self._jail_turn()
        else:
            self._free_turn()

    def _jail_turn(self) -> None:
        """
        Execute a single turn while in jail
        """

        self.num_jail_turns += 1

        if self.num_jail_turns >= 3:
            # only stay in jail for up to 3 turns
            self._free_turn()
            return

        if self.get_out_of_jail_card_drawn[0]:
            # if you have a get-out-of-jail-free card, use it immediately
            self.get_out_of_jail_card_drawn[0] = False
            self.chance_cards.append(1)
            self._free_turn()
            return

        if self.get_out_of_jail_card_drawn[1]:
            self.get_out_of_jail_card_drawn[1] = False
            self.community_chest_cards.append(1)
            self._free_turn()
            return

        roll_one = random.randint(1, 6)
        roll_two = random.randint(1, 6)

        if roll_one == roll_two:
            # move forward this many spaces, but immediately end your turn
            # otherwise (unless it is a chance card)
            self.in_jail = False

            self.current_position += roll_one + roll_two
            self.current_position %= Monopoly.NUM_SPACES
            self.spaces_landed[self.current_position] += 1

            self._draw_card()

    def _free_turn(self) -> None:
        """
        Execute a single turn while not in jail
        """

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
            self.current_position %= Monopoly.NUM_SPACES
            self.spaces_landed[self.current_position] += 1

            if self._draw_card():
                return

            if self.current_position == Monopoly.TO_JAIL_SPACE:
                self._go_to_jail()
                return

    def _go_to_jail(self) -> None:
        """
        Helper function to clean up variables when going to jail
        """

        self.current_position = Monopoly.JAIL_SPACE
        self.in_jail = True
        self.num_jail_turns = 0

    def _draw_card(self) -> None:
        """
        Helper function to draw a card if we are currently on either a Community
        Chest or Chance space.

        We may draw either a go-straight-to-jail card (1/16 odds on a Chance
        draw) or a get-out-of-jail-free card (1/16 odds on both Chance and
        Community Chest draws). If the card is a get-out-of-jail-free card,
        "keep" that card. Otherwise, return it to the pile.

        @return True if we went to jail by drawing the card, False otherwise
        """

        if self.current_position in Monopoly.CHANCE_SPACES:
            # currently on a Chance draw. "Draw" a card.
            # if card_draw is a 2, call that a to-jail card. if it is a 1, call
            # that a get-out-of-jail card
            card_drawn = self.chance_cards.pop()

            if card_drawn == 1:
                # advance to boardwalk
                self.current_position = 39
            elif card_drawn == 2:
                # advance to Go
                self.current_position = Monopoly.GO_SPACE
            elif card_drawn == 3:
                # advance to Illinois Avenue
                self.current_position = 24
            elif card_drawn == 4:
                # advance to St. Charles Place
                self.current_position = 11
            elif card_drawn in (5, 6):
                # advance to the nearest Railway
                self.current_position = min(Monopoly.RAILROAD_SPACES,
                                            key=lambda space: abs(space - self.current_position))
            elif card_drawn == 7:
                # advance to nearest Utility
                self.current_position = min(Monopoly.UTILITY_SPACES,
                                            key=lambda space: abs(space - self.current_position))
            elif card_drawn == 8:
                # bank pays you $50
                pass
            elif card_drawn == 9:
                # get out of jail free card
                self.get_out_of_jail_card_drawn[0] = True
            elif card_drawn == 10:
                # go back three spaces
                self.current_position -= 3
                if self.current_position < 0:
                    self.current_position += self.NUM_SPACES
            elif card_drawn == 11:
                self._go_to_jail()
                self.chance_cards.append(card_drawn)
                return True
            elif card_drawn == 12:
                # general repairs
                pass
            elif card_drawn == 13:
                # speeding fine $15
                pass
            elif card_drawn == 14:
                # advance to Reading Railroad
                self.current_position = 5
            elif card_drawn == 15:
                # pay each player $50
                pass
            elif card_drawn == 16:
                # collect $150
                pass

            self.chance_cards.append(card_drawn)

        elif self.current_position in Monopoly.COMMUNITY_CHEST_SPACES:
            # currently on a Community Chest draw. "Draw" a card
            # if card draw is a 1, call that a get-out-of-jail card (if it has
            # not yet been drawn). otherwise, "discard" this card
            card_drawn = self.community_chest_cards.pop()

            if card_drawn == 1:
                self.get_out_of_jail_card_drawn[1] = True
            else:
                self.community_chest_cards.append(card_drawn)

        return False
