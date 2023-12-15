import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from Connect_4_Main_Version import Connect4Game, Connect4AI, PLAYER_AI, PLAYER_HUMAN, PIECE_HUMAN, PIECE_AI, PIECE_EMPTY


def evaluate_board_potentials(board, ai, piece=PIECE_AI):
    potentials = np.zeros_like(board, dtype=float)
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row][col] == PIECE_EMPTY:
                temp_board = board.copy()
                temp_board[row][col] = piece
                potentials[row][col] = ai.evaluate_board_state(
                    temp_board, piece)
    return potentials


def visualize_board_scores(board, scores, scenario_name):
    fig, ax = plt.subplots(figsize=(8, 6))  # Set individual plot size

    # Flipping the board and scores for correct orientation
    flipped_board = np.flip(board, 0)
    flipped_scores = np.flip(scores, 0)

    # Heatmap for scores
    sns.heatmap(flipped_scores, annot=True, cmap="coolwarm", linewidths=.5,
                fmt=".0f", ax=ax, cbar_kws={'label': 'Score', 'orientation': 'horizontal'},
                annot_kws={"size": 10}, square=True)  # Using square cells for better fit
    ax.set_title(scenario_name)
    ax.set_xlabel("Column (1-based)")
    ax.set_ylabel("Row (1-based)")
    ax.set_xticklabels(np.arange(1, board.shape[1] + 1), rotation=0)
    ax.set_yticklabels(np.arange(1, board.shape[0] + 1), rotation=0)

    # Overlay pieces
    for y in range(flipped_board.shape[0]):
        for x in range(flipped_board.shape[1]):
            if flipped_board[y, x] == PIECE_AI:
                ax.add_patch(plt.Circle((x + 0.5, y + 0.5),
                             0.4, color='yellow', zorder=2))
            elif flipped_board[y, x] == PIECE_HUMAN:
                ax.add_patch(plt.Circle((x + 0.5, y + 0.5),
                             0.4, color='green', zorder=2))

    # Create legend for the pieces outside the plot
    yellow_patch = mpatches.Patch(color='yellow', label='AI Player')
    green_patch = mpatches.Patch(color='green', label='Human Player')
    plt.legend(handles=[yellow_patch, green_patch],
               bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

# Rest of the main function remains the same


def main():
    game = Connect4Game(6, 7)
    ai = Connect4AI(game)

    scenarios = {
        "Early Game": game.create_board(),
        "Mid Game": game.create_board(),
        "End Game (AI to win)": game.create_board(),
        "Defensive (Human to win)": game.create_board()
    }

    # Populate boards for different scenarios
    scenarios["Mid Game"][5, 2:5] = PIECE_AI
    scenarios["Mid Game"][5, 4] = PIECE_HUMAN
    scenarios["End Game (AI to win)"][5, 1:4] = PIECE_AI
    scenarios["Defensive (Human to win)"][5, 1:4] = PIECE_HUMAN

    for scenario_name, board in scenarios.items():
        scores = evaluate_board_potentials(board, ai)
        visualize_board_scores(board, scores, scenario_name)


if __name__ == "__main__":
    main()
