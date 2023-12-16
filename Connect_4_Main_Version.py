import numpy as np
import pygame
import sys
import random
import time

# Constants for the game
GRID_COLOR = (0, 0, 180)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)

# Game player identifiers
PLAYER_HUMAN = 0
PLAYER_AI = 1

# large number
POSITIVE = 10000000
NEGATIVE = -10000000


# Piece types
PIECE_EMPTY = 0
PIECE_HUMAN = 1
PIECE_AI = 2

# Winning condition line segment length
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

    def place_disc(self, board, row, col, piece):
        """
        Drop a disc in the specified column.
        The piece/disc is placed in the given row and column on the board.
        """
        board[row][col] = piece

    def is_column_open(self, board, col):
        """
        Check if the top cell in the specified column is empty.
        Returns True if the cell is empty, False otherwise.
        """
        return board[self.row_count - 1][col] == PIECE_EMPTY

    def find_open_row(self, board, col):
        """
        Find the next open row in the specified column.
        Returns the row index if an empty cell is found, None otherwise.
        """
        for r in range(self.row_count):
            if board[r][col] == PIECE_EMPTY:

                return r

    def reset_game(self):
        """
        Reset the game by clearing the board and resetting variables.
        The board is reinitialized to its original state with all cells empty.
        """
        self.board = self.create_board()

    def is_winning_pattern(self, board, piece):
        """
        Check if there is a winning pattern on the board for the given piece.
        A winning pattern is four pieces of the same type in a row, column, or diagonal.
        The function checks all possible directions (horizontal, vertical, and two diagonals) for a winning pattern.
        Returns True if a winning pattern is found, False otherwise.
        """
        if piece == PIECE_EMPTY:  # Ensure we are not checking for empty pieces
            return False

        # Horizontal check
        # For each row, check if there are four consecutive pieces of the same type
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if board[r][c] == piece and board[r][c + 1] == piece and \
                        board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Vertical check
        # For each column, check if there are four consecutive pieces of the same type
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and \
                        board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Positive diagonal check
        # For each cell that can be the start of a positive sloped diagonal, check if there are four consecutive pieces of the same type
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and \
                        board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # Negative diagonal check
        # For each cell that can be the start of a negative sloped diagonal, check if there are four consecutive pieces of the same type
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and \
                        board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

        return False


class Connect4AI:
    def __init__(self, game, depth=5):
        """
        Initialize the AI with a game and a search depth.
        """
        self.game = game
        self.depth = depth
        self.transposition_table = {}

    def calculate_dynamic_depth(self, board):
        """
        Calculate the appropriate depth for the minimax algorithm dynamically
        based on the current state of the board.
        """
        empty_cells = np.count_nonzero(board == PIECE_EMPTY)
        total_cells = self.game.row_count * self.game.column_count

        # Base depth starts at a minimum value
        base_depth = 7

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

    def find_playable_columns(self, board):
        playable_columns = []
        winning_columns = []
        for col in range(self.game.column_count):
            if self.game.is_column_open(board, col):
                temp_board = board.copy()
                temp_row = self.game.find_open_row(temp_board, col)
                # Check for immediate win
                temp_board[temp_row][col] = PLAYER_AI
                if self.game.is_winning_pattern(temp_board, PLAYER_AI):
                    winning_columns.append(col)
                # Reset the board
                temp_board[temp_row][col] = PIECE_EMPTY
                playable_columns.append(col)
        return winning_columns if winning_columns else playable_columns

    def is_game_over(self, board):
        """
        Check if the game is over.
        The game is over if there is a winning pattern for the AI or the human, or if there are no playable columns left on the board.
        Returns True if the game is over, False otherwise.
        """
        if self.game.is_winning_pattern(board, PLAYER_AI):
            return True
        if self.game.is_winning_pattern(board, PLAYER_HUMAN):
            return True
        if len(self.find_playable_columns(board)) == 0:
            return True
        return False

    def assess_line(self, line_segment, piece):
        """
        Assess the score of a line segment.
        The score is calculated based on the number of pieces and empty cells in the line segment.
        The score is higher if there are more pieces and fewer empty cells.
        The score is also adjusted based on the presence of the opponent's pieces.
        """
        score = 0
        opponent_piece = PIECE_HUMAN
        if piece == PIECE_HUMAN:
            opponent_piece = PIECE_AI

        if line_segment.count(piece) == 4:
            score += 1000
        elif line_segment.count(piece) == 3 and line_segment.count(PIECE_EMPTY) == 1:
            score += 50
        elif line_segment.count(piece) == 2 and line_segment.count(PIECE_EMPTY) == 2:
            score += 10
        if line_segment.count(opponent_piece) == 3 and line_segment.count(PIECE_EMPTY) == 1:
            score -= 25

        return score

    def evaluate_board_state(self, board, piece):
        """
        Calculate the score for the AI's current board position.
        The score is calculated based on the number of pieces in the center column and the score of all directions on the board.
        """
        score = 0

        # Center column preference
        center_array = [int(i) for i in list(
            board[:, self.game.column_count // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Immediate win check
        for c in range(self.game.column_count):
            for r in range(self.game.row_count):
                if board[r][c] == PIECE_EMPTY:
                    # Temporarily make the move
                    board[r][c] = piece
                    if self.game.is_winning_pattern(board, piece):
                        score += 1000000  # Assign a very high score for an immediate win
                    # Undo the move
                    board[r][c] = PIECE_EMPTY

        # Horizontal scoring
        for r in range(self.game.row_count):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.game.column_count - 3):
                line_segment = row_array[c:c + WINNING_LENGTH]
                score += self.assess_line(line_segment, piece)

        # Vertical scoring
        for c in range(self.game.column_count):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.game.row_count - 3):
                line_segment = col_array[r:r + WINNING_LENGTH]
                score += self.assess_line(line_segment, piece)

        # Positive diagonal scoring
        for r in range(self.game.row_count - 3):
            for c in range(self.game.column_count - 3):
                line_segment = [board[r + i][c + i]
                                for i in range(WINNING_LENGTH)]
                score += self.assess_line(line_segment, piece)

        # Negative diagonal scoring
        for r in range(self.game.row_count - 3):
            for c in range(self.game.column_count - 3):
                line_segment = [board[r + 3 - i][c + i]
                                for i in range(WINNING_LENGTH)]
                score += self.assess_line(line_segment, piece)

        return score

    def get_immediate_win_move(self, board, piece):
        """
        Check if there is an immediate win move for the AI.
        An immediate win move is a move that results in a winning pattern.
        Returns the column number if there is an immediate win move, None otherwise.
        """
        for col in range(self.game.column_count):
            if self.game.is_column_open(board, col):
                row = self.game.find_open_row(board, col)
                board[row][col] = piece
                if self.game.is_winning_pattern(board, piece):
                    # Don't forget to remove the piece after check
                    board[row][col] = PIECE_EMPTY
                    return col
                board[row][col] = PIECE_EMPTY
        return None

    def iterative_deepening_minimax(self, board, max_depth, alpha, beta):
        """
        Implement the Iterative Deepening Minimax algorithm.
        The algorithm iteratively applies the Minimax algorithm to increasing depths, up to a maximum depth.
        It returns the best move and its score.
        If there are no playable columns, the function returns None and a score of 0, indicating a draw.
        """
        # Get the list of playable columns
        playable_columns = self.find_playable_columns(board)
        if not playable_columns:
            # No playable columns, so the game is a draw
            return None, 0

        # Initialize the best score to negative infinity and the best column to a random playable column
        best_score = float('-inf')
        best_col = random.choice(playable_columns)

        # Iteratively apply the Minimax algorithm to increasing depths
        for depth in range(1, max_depth + 1):
            # Apply the Minimax algorithm at the current depth
            column, score = self.minimax(board, depth, alpha, beta, True)
            # If the score is better than the best score, update the best score and the best column
            if score > best_score:
                best_score = score
                best_col = column

        # Return the best column and the best score
        return best_col, best_score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        """
        Implement the minimax algorithm with alpha-beta pruning and transposition table.
        The algorithm recursively searches the game tree to the specified depth and returns the best move and its score.
        The function also uses a transposition table to store the results of previous computations, which can be reused to save time.
        """
        # Convert board to a hashable type for the transposition table
        board_key = str(board)
        # If the current state has been computed before, return the stored result
        if (board_key, depth, maximizingPlayer) in self.transposition_table:
            return self.transposition_table[(board_key, depth, maximizingPlayer)]

        playable_columns = self.find_playable_columns(board)
        is_terminal = self.is_game_over(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.game.is_winning_pattern(board, PLAYER_AI):
                    return (None, POSITIVE - (self.game.row_count * self.game.column_count - depth))
                elif self.game.is_winning_pattern(board, PLAYER_HUMAN):
                    return (None, NEGATIVE + (self.game.row_count * self.game.column_count - depth))
                else:
                    return (None, 0)
            else:
                return (None, self.evaluate_board_state(board, PLAYER_AI))

        if maximizingPlayer:
            value = float('-inf')
            column = random.choice(playable_columns)
            for col in playable_columns:
                row = self.game.find_open_row(board, col)
                b_copy = board.copy()
                self.game.place_disc(b_copy, row, col, PLAYER_AI)
                new_score = self.minimax(
                    b_copy, depth - 1, alpha, beta, False)[1]

                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

        else:  # Minimizing player
            value = float('inf')
            column = random.choice(playable_columns)
            for col in playable_columns:
                row = self.game.find_open_row(board, col)
                b_copy = board.copy()
                self.game.place_disc(b_copy, row, col, PLAYER_HUMAN)
                new_score = self.minimax(
                    b_copy, depth - 1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break

        # Save the result in the transposition table before returning
        self.transposition_table[(board_key, depth, maximizingPlayer)] = (
            column, value)
        return column, value


def main():
    """
    Main function to run the Connect 4 game.
    Args:
        None
    Returns:
        None
    Methods:
        main() - Main function to run the Connect 4 game.
        draw_board(board) - Draw the game board using Pygame.
        display_message(screen, message) - Display a message in the center of the screen.
    """
    # Get the number of rows and columns for the game board
    row_count = int(input("Enter the number of rows: "))
    column_count = int(input("Enter the number of columns: "))

    if row_count < 4 or column_count < 4:
        print("The Connect 4 board must have at least 4 rows and 4 columns.")
        return
    if row_count > 14 or column_count > 15:
        print("The Connect 4 board can have at most 14 rows and 15 columns.")
        return

    # Initialize the game and AI
    game = Connect4Game(row_count, column_count)
    CELL_SIZE = 100
    pygame.init()
    screen = pygame.display.set_mode(
        (game.column_count * CELL_SIZE, game.row_count * CELL_SIZE))

    game.reset_game()

    def draw_board(board):
        """
        Draw the game board using Pygame.
        The board is drawn as a grid of cells, with each cell representing a slot for a piece.
        Each piece is drawn as a circle in the cell.
        The color of the circle depends on the type of the piece (human or AI).
        """
        for c in range(game.column_count):
            for r in range(game.row_count):
                pygame.draw.rect(screen, GRID_COLOR, (c * CELL_SIZE,
                                 (game.row_count - 1 - r) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, COLOR_BLACK, (int(c * CELL_SIZE + CELL_SIZE / 2), int(
                    (game.row_count - 1 - r) * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2 - 5)

                if board[r][c] == PIECE_HUMAN:
                    pygame.draw.circle(screen, COLOR_GREEN, (int(c * CELL_SIZE + CELL_SIZE / 2), int(
                        (game.row_count - 1 - r) * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2 - 5)
                elif board[r][c] == PIECE_AI:
                    pygame.draw.circle(screen, COLOR_YELLOW, (int(c * CELL_SIZE + CELL_SIZE / 2), int(
                        (game.row_count - 1 - r) * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2 - 5)

        pygame.display.update()

    def display_message(screen, message):
        """
        Display a message in the center of the screen.
        The message is displayed for 3 seconds.
        """
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(screen.get_width()/2, screen.get_height()/2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(3000)

    # Main game loop
    while True:
        game_over = False
        turn = random.randint(PLAYER_HUMAN, PLAYER_AI)
        draw_board(game.board)
        # Game round loop
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handling human player input
                if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER_HUMAN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    clicked_column = pos_x // CELL_SIZE
                    if game.is_column_open(game.board, clicked_column):
                        row = game.find_open_row(
                            game.board, clicked_column)
                        game.place_disc(game.board, row,
                                        clicked_column, PIECE_HUMAN)
                        if game.is_winning_pattern(game.board, PIECE_HUMAN):
                            game_over = True
                        turn = PLAYER_AI

                        draw_board(game.board)

            # Inside the main game loop, when it's the AI's turn to play:
            if turn == PLAYER_AI and not game_over:
                immediate_win_col = game.ai.get_immediate_win_move(
                    game.board, PIECE_AI)
                if immediate_win_col is not None:
                    row = game.find_open_row(game.board, immediate_win_col)
                    game.place_disc(game.board, row,
                                    immediate_win_col, PIECE_AI)
                    if game.is_winning_pattern(game.board, PIECE_AI):
                        game_over = True
                        # No need to change turn to PLAYER_HUMAN as the game is over
                    # Also the AI has played its move, so update the display
                    draw_board(game.board)
                else:
                    # If there is no immediate win, continue with the existing minimax logic
                    dynamic_depth = game.ai.calculate_dynamic_depth(game.board)
                    column, _ = game.ai.iterative_deepening_minimax(
                        game.board, dynamic_depth, float('-inf'), float('inf'))
                    if column is None:
                        game_over = True
                        display_message(screen, "It's a draw!")
                    else:
                        if game.is_column_open(game.board, column):
                            row = game.find_open_row(game.board, column)
                            game.place_disc(game.board, row, column, PIECE_AI)
                            if game.is_winning_pattern(game.board, PIECE_AI):
                                game_over = True
                            turn = PLAYER_HUMAN

                    draw_board(game.board)

            pygame.display.update()

        # Handling end of the game and displaying messages
        if game.is_winning_pattern(game.board, PIECE_HUMAN):
            display_message(screen, "Congratulations! You win!")
        elif game.is_winning_pattern(game.board, PIECE_AI):
            display_message(screen, "AI wins! Better luck next time.")
        else:
            display_message(screen, "It's a draw!")


if __name__ == "__main__":
    while True:
        main()
