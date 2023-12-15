# Import necessary modules and classes
from Connect4_modified_for_testing import Connect4Game, PIECE_HUMAN, PIECE_AI
import numpy as np
import time


def create_scenario(row_count, column_count, scenario_pieces):
    """
    Creates a board scenario based on the given pieces.

    Parameters:
        row_count (int): The number of rows in the board.
        column_count (int): The number of columns in the board.
        scenario_pieces (list): A list of tuples representing pieces on the board in the form (row, column, piece_type).

    Returns:
        numpy.ndarray: A board with the given scenario set up.
    """
    board = np.zeros((row_count, column_count))
    for row, col, piece in scenario_pieces:
        board[row][col] = piece
    return board


def evaluate_ai_decision(game, depth, player_piece):
    """
    Simulates the AI's decision and returns the result.

    Parameters:
        game (Connect4Game): The game object.
        depth (int): The depth of the minimax algorithm.
        player_piece (int): The piece type of the player.

        Returns:
        tuple: A tuple containing the column chosen, the score, the decision time, the move type, and the number of nodes explored.
    """
    # Set the AI's depth
    game.ai.depth = depth

    # Get the start time
    start_time = time.time()

    # Run the minimax algorithm to simulate the AI's decision
    column, score, decision_time, nodes_explored = game.ai.minimax(
        game.board, depth, float('-inf'), float('inf'), player_piece == PIECE_AI)

    # Create a temporary board to simulate the AI's move
    temp_board = game.board.copy()
    if column is not None:
        row = game.find_open_row(temp_board, column)
        temp_board[row][column] = player_piece
        move_type = game.get_move_type(temp_board, player_piece)
    else:
        move_type = 'Neutral'

    return (column, score, decision_time, move_type, nodes_explored)


def test_ai():
    scenarios = {
        "early_game": [(1, 3, PIECE_HUMAN)],
        "mid_game": [(1, 2, PIECE_AI), (2, 3, PIECE_HUMAN), (3, 3, PIECE_AI)],
        "end_game": [(0, 0, PIECE_AI), (0, 1, PIECE_AI), (0, 2, PIECE_AI), (1, 3, PIECE_HUMAN)]
    }

    depths = [2, 4, 5, 6, 7, 8]

    for scenario_name, pieces in scenarios.items():
        print(f"Testing scenario: {scenario_name}")
        game = Connect4Game(6, 7)
        game.board = create_scenario(6, 7, pieces)

        for depth in depths:
            column, score, decision_time, move_type, nodes_explored = evaluate_ai_decision(
                game, depth, PIECE_AI)
            print(f"Depth: {depth}, Chosen Column: {column}, Score: {score}, Decision Time: {decision_time:.2f} seconds, Move Type: {move_type}, Nodes Explored: {nodes_explored}")


if __name__ == "__main__":
    test_ai()
