from monopoly_game import Monopoly

import random
import matplotlib.pyplot as plt


def main():
    monopoly_games = [Monopoly() for _ in range(10_000)]
    for monopoly in monopoly_games:
        for _ in range(random.randint(50, 150)):
            monopoly.play_turn()

    x = [i for i in range(Monopoly.NUM_SPACES)]
    monopoly_space_distribution = [0 for _ in range(Monopoly.NUM_SPACES)]
    for monopoly in monopoly_games:
        for i in range(len(monopoly.spaces_landed)):
            monopoly_space_distribution[i] += monopoly.spaces_landed[i]

    plt.xlabel("Space Index")
    plt.ylabel("Number of times landed")

    plt.bar(x, monopoly_space_distribution)
    plt.show()


if __name__ == "__main__":
    main()
