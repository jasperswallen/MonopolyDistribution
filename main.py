from monopoly_game import Monopoly

import matplotlib.pyplot as plt


def main():
    monopoly = Monopoly()
    for _ in range(100):
        monopoly.play_turn()

    x = [i + 1 for i in range(Monopoly.NUM_SPACES)]

    plt.xlabel("Space Index")
    plt.ylabel("Number of times landed")

    plt.bar(x, monopoly.spaces_landed)
    plt.show()


if __name__ == "__main__":
    main()
