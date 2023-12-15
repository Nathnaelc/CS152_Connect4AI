# Import necessary modules and classes
from Connect4_modified_for_testing import Connect4Game, Connect4AI, PLAYER_AI, PLAYER_HUMAN
import numpy as np
import time
import seaborn as sns


class Connect4DepthEfficiencyTest:
    """
    Class to test the efficiency of the minimax algorithm at different depths
    Attributes:
        game: Connect4Game object
        depth: Depth to test

    """

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
        return column, score, decision_time, nodes_explored


# Helper function to create a board state from a list of pieces
def create_scenario(row_count, column_count, pieces):
    board = np.zeros((row_count, column_count))
    for (row, col, piece) in pieces:
        if 0 <= row < row_count and 0 <= col < column_count:
            board[row][col] = piece
    return board


def main():
    row_count = 6
    column_count = 7
    game = Connect4Game(row_count, column_count)

    # Define different depths to test
    depths = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Define a scenario to test
    scenarios = {
        "early_game": create_scenario(6, 7, [(1, 3, PLAYER_HUMAN)]),
        "mid_game": create_scenario(6, 7, [(1, 2, PLAYER_AI), (2, 3, PLAYER_HUMAN), (3, 3, PLAYER_AI)]),
        "end_game": create_scenario(6, 7, [(0, 0, PLAYER_AI), (0, 1, PLAYER_AI), (0, 2, PLAYER_AI), (1, 3, PLAYER_HUMAN)]),
    }

    results = []
    for scenario_name, board_state in scenarios.items():
        for depth in depths:
            tester = Connect4DepthEfficiencyTest(game, depth)
            column, score, decision_time, nodes_explored = tester.test_scenario(
                board_state)
            results.append({
                "Scenario": scenario_name,
                "Depth": depth,
                "Decision Time": decision_time,
                "Nodes Explored": nodes_explored
            })

    # Convert results to a DataFrame for visualization
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame(results)
    print(df)

    # Visualization code
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Depth", y="Decision Time",
                 hue="Scenario", marker='o')
    plt.title("AI Decision Time vs Depth")
    plt.xlabel("Depth")
    plt.ylabel("Decision Time (seconds)")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Depth", y="Nodes Explored",
                 hue="Scenario", marker='o')
    plt.title("AI Nodes Explored vs Depth")
    plt.xlabel("Depth")
    plt.ylabel("Nodes Explored")
    plt.show()


if __name__ == "__main__":
    main()
