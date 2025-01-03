import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # add path/to/bayestennis/../ to sys.path
import torch
from bayestennis.Loss import Loss


def main():

    BREAKPOINT_ME = 0

    abilities = [100, 98, 102, 101]

    score = [
        [6, 1, 6, 2, 0, 0],
        [4, 6, 7, 6, 10, 5]
    ]
    player_indices = [
        [0, 0, 1, 1],
        [0, 1, 2, 3]
    ]
    weight = [1.0, 2.0]

    loss = Loss()

    loss.add('MrDodo', score, player_indices, weight)
    loss.add('Toringo', score, player_indices, weight)

    loss_value = loss(abilities)

    BREAKPOINT_ME = 0


if __name__ == "__main__":

    main()
