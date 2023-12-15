import numpy as np
from Connect4_MyVersion import Connect4Game, Connect4AI, PLAYER_AI, PLAYER_HUMAN, NEGATIVE, POSITIVE
import unittest


class TestMinimax(unittest.TestCase):

    def setUp(self):
        # Initialize the game and AI for each test
        self.game = Connect4Game(6, 7)

    def print_board(self, board):
        # Helper function to print the board state
        print(np.flip(board, 0))

    def test_empty_board(self):
        # Empty board scenario
        test_board = self.game.create_board()
        self.print_board(test_board)
        column, score = self.game.ai.minimax(
            test_board, 5, NEGATIVE, POSITIVE, True)
        # Expect AI to play in the middle column on an empty board
        expected_column = self.game.column_count // 2
        self.assertEqual(column, expected_column)

    def test_mid_game_scenario(self):
        # Mid-game scenario
        test_board = self.game.create_board()
        test_board[0][0] = PLAYER_HUMAN
        test_board[1][0] = PLAYER_AI
        test_board[2][0] = PLAYER_HUMAN
        self.print_board(test_board)
        column, score = self.game.ai.minimax(
            test_board, 5, NEGATIVE, POSITIVE, True)
        # Add your expectation here based on your game logic

    def test_immediate_block(self):
        # AI must block human's immediate win
        test_board = self.game.create_board()
        test_board[0:3, 0] = PLAYER_HUMAN
        self.print_board(test_board)
        column, score = self.game.ai.minimax(
            test_board, 5, NEGATIVE, POSITIVE, True)
        # AI should play in the first column to block the human's win
        self.assertEqual(column, 0)

    # Add more tests for different scenarios...


if __name__ == '__main__':
    unittest.main()
