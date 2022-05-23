"""
Simulate Monopoly games to determine space distribution
"""

import random
import matplotlib.pyplot as plt
import mplcursors

from monopoly_game import Monopoly


def main():
    """
    Run simulation of Monopoly games and graph frequency chart
    """

    monopoly_games = [Monopoly() for _ in range(10_000)]
    for monopoly in monopoly_games:
        for _ in range(random.randint(50, 150)):
            monopoly.play_turn()

    space_index = list(range(Monopoly.NUM_SPACES))
    monopoly_space_distribution = [0 for _ in range(Monopoly.NUM_SPACES)]

    for monopoly in monopoly_games:
        for i, count in enumerate(monopoly.get_distribution()):
            monopoly_space_distribution[i] += count

    plt.xlabel("Space Index")
    plt.ylabel("Number of times landed")
    plt.title("Monopoly Space Frequency Distribution")

    plt.bar(space_index, monopoly_space_distribution)

    cursor: mplcursors.Cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Persistent)

    @cursor.connect("add")
    def on_add(sel: mplcursors.Selection):
        x_pos, y_pos, width, height = sel.artist[sel.index].get_bbox().bounds
        sel.annotation.set(text=f"{int(x_pos + width / 2)}: {int(height)}",
                           position=(0, 20),
                           anncoords="offset points")
        sel.annotation.xy = (x_pos + width / 2, y_pos + height)

    plt.show()


if __name__ == "__main__":
    main()
