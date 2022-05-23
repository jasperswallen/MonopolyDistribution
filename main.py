"""
Simulate Monopoly games to determine space distribution
"""

import random
import matplotlib.pyplot as plt
import mplcursors

from monopoly_game import Monopoly

PROPERTY_INDEXES = [
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
RAILROAD_INDEXES = [
    5,
    15,
    25,
    35,
]
GO_INDEX = [
    0,
]
JAIL_INDEX = [
    10,
]
FREE_PARKING_INDEX = [
    20,
]
TO_JAIL_INDEX = [
    30,
]
CARD_INDEXES = [
    2,
    7,
    17,
    22,
    33,
    36,
]
TAX_INDEXES = [
    4,
    12,
    28,
    38,
]
colors = []
labels = []
for space in range(Monopoly.NUM_SPACES):
    if space in PROPERTY_INDEXES:
        colors.append("green")
        labels.append("Property")
    elif space in RAILROAD_INDEXES:
        colors.append("black")
        labels.append("Railroad")
    elif space in GO_INDEX:
        colors.append("#90EE90")
        labels.append("Go")
    elif space in JAIL_INDEX:
        colors.append("orange")
        labels.append("Jail (Visiting)")
    elif space in FREE_PARKING_INDEX:
        colors.append("#023020")
        labels.append("Free Parking")
    elif space in TO_JAIL_INDEX:
        colors.append("red")
        labels.append("To Jail")
    elif space in CARD_INDEXES:
        colors.append("blue")
        labels.append("Card Draw")
    elif space in TAX_INDEXES:
        colors.append("brown")
        labels.append("Tax")


def main():
    """
    Run simulation of Monopoly games and graph frequency chart
    """

    random.seed()

    monopoly_games = [Monopoly() for _ in range(10_000)]
    for monopoly in monopoly_games:
        for _ in range(random.randint(150, 250)):
            monopoly.play_turn()

    space_index = list(range(Monopoly.NUM_SPACES))
    monopoly_space_distribution = [0 for _ in range(Monopoly.NUM_SPACES)]

    for monopoly in monopoly_games:
        for i, count in enumerate(monopoly.get_distribution()):
            monopoly_space_distribution[i] += count

    plt.xlabel("Space Index")
    plt.ylabel("Number of times landed")
    plt.title("Monopoly Space Frequency Distribution")

    plt.bar(space_index, monopoly_space_distribution, color=colors)

    cursor: mplcursors.Cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Persistent)

    @cursor.connect("add")
    def on_add(sel: mplcursors.Selection):
        x_pos, y_pos, width, height = sel.artist[sel.index].get_bbox().bounds
        index = int(x_pos + width / 2)
        sel.annotation.set(text=f"{index}: {int(height)}\n{labels[index]}",
                           position=(0, 20),
                           anncoords="offset points")
        sel.annotation.xy = (index, y_pos + height)

    plt.show()


if __name__ == "__main__":
    main()
