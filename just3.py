import numpy as np
import pygame
import sys
import math
import random

# Constants for the game
COLOR_BLUE = (0, 0, 180)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

# Game player identifiers
PLAYER_HUMAN = 0
PLAYER_AI = 1


# Piece types
PIECE_EMPTY = 0
PIECE_HUMAN = 1
PIECE_AI = 2

# Winning condition window length
WINNING_LENGTH = 4


class Connect4Game:
    def __init__(self, row_count, column_count):
        # Initialize the game with the given row and column count, and AI depth
        self.row_count = row_count
        self.column_count = column_count
        self.board = self.create_board()
        self.ai = Connect4AI(self)

    def create_board(self):
        """
        Create a 2D numpy array for the game board.
        The board is initialized with zeros, indicating all cells are empty.
        """
        return np.zeros((self.row_count, self.column_count))

    def drop_piece(self, board, row, col, piece):
        """
        Drop a piece in the specified column.
        The piece/disk is placed in the given row and column on the board.
        """
        board[row][col] = piece

    def is_valid_location(self, col):
        """
        Check if the top cell in the specified column is empty.
        Returns True if the cell is empty, False otherwise.
        """
        return self.board[self.row_count - 1][col] == PIECE_EMPTY

    def get_next_open_row(self, board, col):
        """
        Find the next open row in the specified column.
        Returns the row index if an empty cell is found, None otherwise.
        """
        for r in range(self.row_count):
            if board[r][col] == PIECE_EMPTY:

                return r

    def print_board(self):
        """
        Print the game board.
        The board is flipped vertically before printing, so the first row printed is the bottom row of the game board.
        """
        print(np.flip(self.board, 0))

    def reset_game(self):
        """
        Reset the game by clearing the board and resetting variables.
        The board is reinitialized to its original state with all cells empty.
        """
        self.board = self.create_board()

    def check_winning_move(self, board, piece):
        """
        Check if the last move was a winning move on the given board.
        This is done by checking all possible directions (horizontal, vertical, and two diagonals) for a sequence of four identical pieces.
        Returns True if a winning sequence is found, False otherwise.
        """
        # Check horizontal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if board[r][c] == piece and \
                        board[r][c + 1] == piece and \
                        board[r][c + 2] == piece and \
                        board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if board[r][c] == piece and \
                        board[r + 1][c] == piece and \
                        board[r + 2][c] == piece and \
                        board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if board[r][c] == piece and \
                        board[r + 1][c + 1] == piece and \
                        board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if board[r][c] == piece and \
                        board[r - 1][c + 1] == piece and \
                        board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

        return False

    def is_terminal_state(self, board):
        """
        Check if the board is in a terminal state (win, loss, or draw).
        The board is in a terminal state if there is a winning move for the human or the AI, or if there are no valid locations left on the board.
        """
        return self.check_winning_move(board, PIECE_HUMAN) or \
            self.check_winning_move(board, PIECE_AI) or \
            len(self.get_valid_locations(board)) == 0


class Connect4AI:
    def __init__(self, game):
        """
        Initialize the AI with a game and a search depth.
        """
        self.game = game

    def calculate_dynamic_depth(self, board):
        """
        Calculate the appropriate depth for the minimax algorithm dynamically
        based on the current state of the board.
        """
        empty_cells = np.count_nonzero(board == PIECE_EMPTY)
        total_cells = self.game.row_count * self.game.column_count

        # Base depth starts at a minimum value
        base_depth = 4

        # Increase depth as the game progresses
        if empty_cells / total_cells < 0.5:  # More than half of the board is filled
            return base_depth + 1
        if empty_cells / total_cells < 0.25:  # 75% of the board is filled
            return base_depth + 2

        # Further increase if a player is close to winning
        if self.is_near_win(board):
            return base_depth + 3

        return base_depth

    def is_near_win(self, board):
        """
        Check if either player is close to winning (e.g., three in a row).
        """
        for piece in [PIECE_HUMAN, PIECE_AI]:
            # Check horizontal locations for near win
            for c in range(self.game.column_count - 3):
                for r in range(self.game.row_count):
                    if sum([board[r][c + i] == piece for i in range(WINNING_LENGTH - 1)]) == 3 and \
                            PIECE_EMPTY in [board[r][c + i] for i in range(WINNING_LENGTH)]:
                        return True

            # Check vertical locations for near win
            for c in range(self.game.column_count):
                for r in range(self.game.row_count - 3):
                    if sum([board[r + i][c] == piece for i in range(WINNING_LENGTH - 1)]) == 3 and \
                            PIECE_EMPTY in [board[r + i][c] for i in range(WINNING_LENGTH)]:
                        return True

            # Check positively sloped diagonals
            for c in range(self.game.column_count - 3):
                for r in range(self.game.row_count - 3):
                    if sum([board[r + i][c + i] == piece for i in range(WINNING_LENGTH - 1)]) == 3 and \
                            PIECE_EMPTY in [board[r + i][c + i] for i in range(WINNING_LENGTH)]:
                        return True

            # Check negatively sloped diagonals
            for c in range(self.game.column_count - 3):
                for r in range(3, self.game.row_count):
                    if sum([board[r - i][c + i] == piece for i in range(WINNING_LENGTH - 1)]) == 3 and \
                            PIECE_EMPTY in [board[r - i][c + i] for i in range(WINNING_LENGTH)]:
                        return True

        return False

    def get_valid_locations(self, board):
        """
        Get a list of columns that can accept a new piece.
        The list is generated by checking each column in the board to see if it can accept a new piece.
        """
        valid_locations = []
        for col in range(self.game.column_count):
            # Using the provided board parameter
            if board[self.game.row_count - 1][col] == PIECE_EMPTY:
                valid_locations.append(col)
        return valid_locations

    def is_terminal_node(self, board):
        return self.game.check_winning_move(board, PLAYER_AI) or \
            self.game.check_winning_move(board, PLAYER_HUMAN) or \
            len(self.get_valid_locations(board)) == 0

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = PIECE_HUMAN if piece == PIECE_AI else PIECE_AI

        # Aggressive scoring for potential wins
        if window.count(piece) == 4:
            score += 100000  # Very high score for a winning move
        elif window.count(piece) == 3 and window.count(PIECE_EMPTY) == 1:
            score += 500  # High score for being one move away from winning
        elif window.count(piece) == 2 and window.count(PIECE_EMPTY) == 2:
            score += 50  # Score for potential future opportunities

        # Predictive defense
        if window.count(opponent_piece) == 3 and window.count(PIECE_EMPTY) == 1:
            score -= 400  # High negative score for opponent being one move away from winning

        return score

    def evaluate_board(self, board, piece):
        """
        Evaluate the game board for a given player (AI or human).
        This evaluation function considers multiple factors to determine the board's score.
        """
        score = 0
        center_array = [int(i) for i in list(
            board[:, self.game.column_count // 2])]
        center_count = center_array.count(piece)
        score += center_count * 10  # Keeping center control weight as is

        # Horizontal, Vertical, Diagonal Evaluation with increased strategic scoring
        for r in range(self.game.row_count):
            for c in range(self.game.column_count - 3):
                horizontal_window = [board[r][c + i]
                                     for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(horizontal_window, piece)

        for c in range(self.game.column_count):
            for r in range(self.game.row_count - 3):
                vertical_window = [board[r + i][c]
                                   for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(vertical_window, piece)

        for r in range(self.game.row_count - 3):
            for c in range(self.game.column_count - 3):
                diag1_window = [board[r + i][c + i]
                                for i in range(WINNING_LENGTH)]
                diag2_window = [board[r + 3 - i][c + i]
                                for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(diag1_window, piece)
                score += self.evaluate_window(diag2_window, piece)

        return score

    def score_board_position(self, board, piece):
        """
        Calculate the score for the AI's current board position.
        The score is calculated based on the number of pieces in the center column and the score of all directions on the board.
        """
        score = 0
        center_array = [int(i) for i in list(
            board[:, self.game.column_count // 2])]
        center_count = center_array.count(piece)
        score += center_count * 4  # Increased weight for center control

        # Adjusted Diagonal Evaluation
        for r in range(self.game.row_count):
            for c in range(self.game.column_count):
                if r + 3 < self.game.row_count and c + 3 < self.game.column_count:
                    diag1_window = [board[r + i][c + i]
                                    for i in range(WINNING_LENGTH)]
                    score += self.evaluate_window(diag1_window, piece)

                if r - 3 >= 0 and c + 3 < self.game.column_count:
                    diag2_window = [board[r - i][c + i]
                                    for i in range(WINNING_LENGTH)]
                    score += self.evaluate_window(diag2_window, piece)

        # Horizontal, Vertical, Diagonal Evaluation
        for r in range(self.game.row_count):
            for c in range(self.game.column_count - 3):
                horizontal_window = [board[r][c + i]
                                     for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(horizontal_window, piece)

        for c in range(self.game.column_count):
            for r in range(self.game.row_count - 3):
                vertical_window = [board[r + i][c]
                                   for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(vertical_window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        """
        Implement the minimax algorithm with alpha-beta pruning and heuristic evaluation.
        The algorithm recursively searches the game tree to the specified depth and returns the best move and its score.
        """

        if depth == 0 or self.is_terminal_node(board):
            if self.is_terminal_node(board):
                if self.game.check_winning_move(board, PLAYER_AI):
                    return (None, float('inf'))
                elif self.game.check_winning_move(board, PLAYER_HUMAN):
                    return (None, float('-inf'))
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_board_position(board, PLAYER_AI if maximizingPlayer else PLAYER_HUMAN))

        if maximizingPlayer:
            value = float('-inf')
            column = random.choice(self.get_valid_locations(board))
            for col in self.get_valid_locations(board):
                row = self.game.get_next_open_row(col)
                b_copy = board.copy()
                b_copy[row][col] = PLAYER_AI

                new_score = self.minimax(
                    b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = float('inf')
            column = random.choice(self.get_valid_locations(board))
            for col in self.get_valid_locations(board):
                row = self.game.get_next_open_row(col)
                b_copy = board.copy()
                b_copy[row][col] = PLAYER_HUMAN
                new_score = self.minimax(
                    b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def best_move(self):
        """
        Determine the best move for the AI.
        The best move is determined by using the minimax algorithm to search the game tree to a specified depth and return the move with the highest score.
        If no valid move is found, None is returned.
        """
        valid_locations = self.get_valid_locations(self.game.board)
        if not valid_locations:  # Check if there are no valid moves
            return None

        best_score = -math.inf
        best_col = random.choice(valid_locations)
        dynamic_depth = self.calculate_dynamic_depth(self.game.board)

        for col in valid_locations:
            row = self.game.get_next_open_row(self.game.board, col)
            if row is not None:
                temp_board = self.game.board.copy()
                temp_board[row][col] = PLAYER_AI
                score = self.minimax(
                    temp_board, dynamic_depth, -math.inf, math.inf, True)[1]
                if score > best_score:
                    best_score = score
                    best_col = col

        return best_col


def main():
    row_count = int(input("Enter the number of rows: "))
    column_count = int(input("Enter the number of columns: "))

    if row_count < 4 or column_count < 4:
        print("The Connect 4 board must have at least 4 rows and 4 columns.")
        return

    game = Connect4Game(row_count, column_count)
    CELL_SIZE = 100
    pygame.init()
    screen = pygame.display.set_mode(
        (game.column_count * CELL_SIZE, game.row_count * CELL_SIZE))

    game.reset_game()

    def draw_board(board):
        for c in range(game.column_count):
            for r in range(game.row_count):
                pygame.draw.rect(screen, COLOR_BLUE, (c * CELL_SIZE,
                                 (game.row_count - 1 - r) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, COLOR_BLACK, (int(c * CELL_SIZE + CELL_SIZE / 2), int(
                    (game.row_count - 1 - r) * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2 - 5)

                if board[r][c] == PIECE_HUMAN:
                    pygame.draw.circle(screen, COLOR_RED, (int(c * CELL_SIZE + CELL_SIZE / 2), int(
                        (game.row_count - 1 - r) * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2 - 5)
                elif board[r][c] == PIECE_AI:
                    pygame.draw.circle(screen, COLOR_YELLOW, (int(c * CELL_SIZE + CELL_SIZE / 2), int(
                        (game.row_count - 1 - r) * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2 - 5)

        pygame.display.update()

    def display_message(screen, message):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))  # White color
        text_rect = text.get_rect(
            center=(screen.get_width()/2, screen.get_height()/2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds

    while True:
        game_over = False
        turn = random.randint(PLAYER_HUMAN, PLAYER_AI)
        game.reset_game()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER_HUMAN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    clicked_column = pos_x // CELL_SIZE
                    if game.is_valid_location(clicked_column):
                        row = game.get_next_open_row(
                            game.board, clicked_column)
                        game.drop_piece(game.board, row,
                                        clicked_column, PIECE_HUMAN)
                        if game.check_winning_move(game.board, PIECE_HUMAN):
                            game_over = True
                        turn = PLAYER_AI

            # Inside the main game loop
            if turn == PLAYER_AI and not game_over:
                column = game.ai.best_move()
                if column is not None:
                    if game.is_valid_location(column):
                        row = game.get_next_open_row(game.board, column)
                        game.drop_piece(game.board, row, column, PIECE_AI)
                        if game.check_winning_move(game.board, PIECE_AI):
                            game_over = True
                        turn = PLAYER_HUMAN
                else:
                    # Handle the case when there are no valid moves left
                    game_over = True
                    display_message(screen, "It's a draw!")

            draw_board(game.board)
            pygame.display.update()

            # Handling end of the game and displaying messages
        # After the game is over, display the appropriate message
        if game.check_winning_move(game.board, PIECE_HUMAN):
            display_message(screen, "Congratulations! You win!")
        elif game.check_winning_move(game.board, PIECE_AI):
            display_message(screen, "AI wins! Better luck next time.")
        else:
            display_message(screen, "It's a draw!")

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_input = False
                        main()  # Restart the game
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

         # Draw board
        draw_board(game.board)
        pygame.display.update()

        # Display result and prompt for restart or close
        if game.check_winning_move(PIECE_HUMAN):
            print("Congratulations! You win! and your AI is fucked up")
        elif game.check_winning_move(PIECE_AI):
            print("AI wins! Better luck next time.")
        else:
            print("It's a draw!")

        while True:
            choice = input(
                "Do you want to restart the game (R) or close (C)? ").upper()
            if choice == 'R':
                break
            elif choice == 'C':
                pygame.quit()  # Close the Pygame window and exit the program
                sys.exit()


if __name__ == "__main__":
    main()
