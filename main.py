from monopoly_game import Monopoly

import random
import matplotlib.pyplot as plt
import mplcursors


def main():
    monopoly_games = [Monopoly() for _ in range(10_000)]
    for monopoly in monopoly_games:
        for _ in range(random.randint(50, 150)):
            monopoly.play_turn()

    space_index = [i for i in range(Monopoly.NUM_SPACES)]
    monopoly_space_distribution = [0 for _ in range(Monopoly.NUM_SPACES)]

    for monopoly in monopoly_games:
        for i in range(len(monopoly.spaces_landed)):
            monopoly_space_distribution[i] += monopoly.spaces_landed[i]

    plt.xlabel("Space Index")
    plt.ylabel("Number of times landed")

    plt.bar(space_index, monopoly_space_distribution)

    cursor: mplcursors.Cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Transient)

    @cursor.connect("add")
    def on_add(sel: mplcursors.Selection):
        x, y, width, height = sel.artist[sel.index].get_bbox().bounds
        sel.annotation.set(text=f"{int(x + width / 2)}: {int(height)}",
                           position=(0, 20),
                           anncoords="offset points")
        sel.annotation.xy = (x + width / 2, y + height)

    plt.show()


if __name__ == "__main__":
    main()
