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

        self.spaces_landed: List[int] = [0 for i in range(self.NUM_SPACES)]

        assert len(self.spaces_landed) == self.NUM_SPACES

    def play_turn(self) -> None:
        """
        Play a single turn

        When in jail, attempt to get out of jail only by rolling dice. Assume
        that you do not have enough money and do not have a get-out-of-jail-free
        card (TODO)
        """

        if self.in_jail:
            # currently in jail
            pass
        else:
            # not currently in jail, simply roll two dice
            while True:
                roll_one = random.randint(1, 6)
                roll_two = random.randint(1, 6)

                if roll_one != roll_two:
                    self.num_consecutive_doubles = 0
                    break
                else:
                    self.num_consecutive_doubles += 1
                    if self.num_consecutive_doubles >= 3:
                        self._go_to_jail()
                        # go to jail and end your turn
                        return

                self.current_position += roll_one + roll_two
                self.current_position %= self.NUM_SPACES
                self.spaces_landed[self.current_position] += 1

                if not self.jail_card_drawn and self.current_position in self.CHANCE_SPACES:
                    # landed on a chance space and could go to jail
                    if random.randint(1, self.ORIGINAL_CHANCE_CARDS - self.chance_cards_drawn) <= 1:
                        self._go_to_jail()
                        self.chance_cards_drawn += 1
                        self.jail_card_drawn = True
                        return
                    else:
                        self.chance_cards_drawn += 1

                if self.current_position == self.TO_JAIL_SPACE:
                    self._go_to_jail()
                    return

    def _go_to_jail(self):
        self.current_position = self.JAIL_SPACE
        self.in_jail = True
        self.num_consecutive_doubles = 0
