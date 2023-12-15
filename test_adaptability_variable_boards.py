# Import necessary modules and classes
from Connect4_modified_for_testing import Connect4Game, Connect4AI, PLAYER_AI, PLAYER_HUMAN
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time


class Connect4AITest:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    def test_scenario(self, board_state):
        self.game.configure_board(board_state)
        start_time = time.time()
        column, score, decision_time, nodes_explored = self.game.ai.minimax(
            self.game.board, self.depth, float('-inf'), float('inf'), True)
        end_time = time.time()
        decision_time = end_time - start_time
        return decision_time, nodes_explored

    @staticmethod
    def create_scenario(row_count, column_count, pieces):
        board = np.zeros((row_count, column_count))
        for (row, col, piece) in pieces:
            if 0 <= row < row_count and 0 <= col < column_count:
                board[row][col] = piece
        return board


def main():
    board_sizes = [(6, 7), (8, 10), (10, 10)]  # Example board sizes
    depths = [2, 4, 6, 8]
    test_scenario = [(2, 2, PLAYER_AI), (3, 3, PLAYER_HUMAN)
                     ]

    results = []
    for row_count, column_count in board_sizes:
        game = Connect4Game(row_count, column_count)
        board_state = Connect4AITest.create_scenario(
            row_count, column_count, test_scenario)

        for depth in depths:
            tester = Connect4AITest(game, depth)
            decision_time, nodes_explored = tester.test_scenario(board_state)
            results.append({
                "Board Size": f"{row_count}x{column_count}",
                "Depth": depth,
                "Decision Time": decision_time,
                "Nodes Explored": nodes_explored
            })

    df = pd.DataFrame(results)

    # Plotting Decision Time vs Board Size for each Depth
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Board Size",
                 y="Decision Time", hue="Depth", marker='o')
    plt.title("Decision Time vs Board Size at Different Depths")
    plt.ylabel("Decision Time (seconds)")
    plt.show()

    # Plotting Nodes Explored vs Board Size for each Depth
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Board Size",
                 y="Nodes Explored", hue="Depth", marker='o')
    plt.title("Nodes Explored vs Board Size at Different Depths")
    plt.show()


if __name__ == "__main__":
    main()
