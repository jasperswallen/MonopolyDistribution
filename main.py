"""
Simulate Monopoly games to determine space distribution
"""

import random
import matplotlib.pyplot as plt
import mplcursors

from monopoly_game import Monopoly

colors = []
labels = []
for space in range(Monopoly.NUM_SPACES):
    if space in Monopoly.PROPERTY_SPACES:
        colors.append("green")
        labels.append("Property")
    elif space in Monopoly.RAILROAD_SPACES:
        colors.append("black")
        labels.append("Railroad")
    elif space == Monopoly.GO_SPACE:
        colors.append("#90EE90")
        labels.append("Go")
    elif space == Monopoly.JAIL_SPACE:
        colors.append("orange")
        labels.append("Jail (Visiting)")
    elif space == Monopoly.FREE_PARKING_SPACE:
        colors.append("#023020")
        labels.append("Free Parking")
    elif space == Monopoly.TO_JAIL_SPACE:
        colors.append("red")
        labels.append("To Jail")
    elif space in Monopoly.CHANCE_SPACES:
        colors.append("blue")
        labels.append("Chance Card Draw")
    elif space in Monopoly.COMMUNITY_CHEST_SPACES:
        colors.append("blue")
        labels.append("Community Chest Card Draw")
    elif space in Monopoly.TAX_SPACES:
        colors.append("brown")
        labels.append("Tax")
    elif space in Monopoly.UTILITY_SPACES:
        colors.append("grey")
        labels.append("Utility")


def main():
    """
    Run simulation of Monopoly games and graph frequency chart
    """

    random.seed()

    monopoly_games = [Monopoly() for _ in range(10_000)]
    for monopoly in monopoly_games:
        for _ in range(random.randrange(20, 50)):
            monopoly.play_turn()

    space_index = list(range(Monopoly.NUM_SPACES))
    monopoly_space_distribution = [0 for _ in range(Monopoly.NUM_SPACES)]

    total_spaces = 0
    for monopoly in monopoly_games:
        for i, count in enumerate(monopoly.get_distribution()):
            monopoly_space_distribution[i] += count
            total_spaces += count

    plt.xlabel("Space Index")
    plt.ylabel("Number of times landed")
    plt.title("Monopoly Space Frequency Distribution")

    plt.bar(space_index, monopoly_space_distribution, color=colors)

    cursor: mplcursors.Cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Persistent)

    @cursor.connect("add")
    def on_add(sel: mplcursors.Selection):
        x_pos, y_pos, width, height = sel.artist[sel.index].get_bbox().bounds
        index = int(x_pos + width / 2)
        sel.annotation.set(
            text=f"{index}: {int(height)} ({(height / total_spaces * 100.0):.3f}%)\n{labels[index]}",
            position=(0, 20),
            anncoords="offset points")
        sel.annotation.xy = (index, y_pos + height)

    plt.show()


if __name__ == "__main__":
    main()
