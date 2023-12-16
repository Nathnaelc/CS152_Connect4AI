# this is the modified version of Connect4.py for testing purposes
# it inclides additional methods and attributes to test the AI and the game
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
    """
    Connect4Game class represents a game of Connect 4.

    Attributes:
        row_count (int): The number of rows in the game board.
        column_count (int): The number of columns in the game board.
        board (numpy.ndarray): A 2D numpy array representing the game board.
        ai (Connect4AI): An instance of the Connect4AI class for AI moves.

    Methods:
        __init__(self, row_count, column_count): Initializes the Connect4Game object with the given row and column count.
        create_board(self): Creates a 2D numpy array for the game board.
        place_disc(self, board, row, col, piece): Drops a piece in the specified column.
        is_column_open(self, board, col): Checks if the top cell in the specified column is empty.
        find_open_row(self, board, col): Finds the next open row in the specified column.
        display_board(self): Prints the game board.
        reset_game(self): Resets the game by clearing the board and resetting variables.
        is_winning_move(self, board, piece): Checks if the current move is a winning move.
        configure_board(self, board_state): Sets the board to a specific state for testing.

    """

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
        Drop a piece in the specified column.
        The piece/disk is placed in the given row and column on the board.
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

    def is_winning_move(self, board, piece):
        if piece == PIECE_EMPTY:  # Ensure we are not checking for empty pieces
            # print(
            #     "Called is_winning_move with an empty piece, which should not happen.")
            return False

        # Horizontal check
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if board[r][c] == piece and board[r][c + 1] == piece and \
                        board[r][c + 2] == piece and board[r][c + 3] == piece:
                    # print("Winning move found!: Horizontal")
                    return True

        # Vertical check
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and \
                        board[r + 2][c] == piece and board[r + 3][c] == piece:
                    # print("Winning move found!: Vertical")
                    return True

        # Positive diagonal check
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and \
                        board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    # print("Winning move found!: Positive Diagonal")
                    return True

        # Negative diagonal check
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and \
                        board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    # print("Winning move found!: Negative Diagonal")
                    return True

        return False

    def configure_board(self, board_state):
        """
        Set the board to a specific state for testing
        """
        if board_state.shape == (self.row_count, self.column_count):
            self.board = board_state
        else:
            raise ValueError(
                f"Board state must be of shape ({self.row_count}, {self.column_count}).")

    def is_setting_up_win(self, board, column, piece):
        row = self.find_open_row(board, column)
        if row is None:
            return False

        temp_board = board.copy()
        temp_board[row][column] = piece
        # Check for potential win in the next move
        for col in range(self.column_count):
            future_row = self.find_open_row(temp_board, col)
            if future_row is not None and col != column:
                temp_board[future_row][col] = piece
                if self.is_winning_move(temp_board, piece):
                    return True
                temp_board[future_row][col] = PIECE_EMPTY
        return False

    def is_blocking_opponent(self, board, column, piece):
        row = self.find_open_row(board, column)
        if row is None:
            return False

        temp_board = board.copy()
        opponent_piece = PIECE_HUMAN if piece == PIECE_AI else PIECE_AI
        temp_board[row][column] = opponent_piece
        return self.is_winning_move(temp_board, opponent_piece)

    def get_move_type(self, temp_board, piece):
        """
        Determine if the next move is offensive, defensive or neutral.

        Parameters:
            board (numpy.ndarray): The current board state.
            piece (int): The piece type to check the move for.

        Returns:
            str: The type of move ('Offensive', 'Defensive', 'Neutral').
        """
        # Check for offensive move
        if self.is_winning_move(temp_board, piece):
            return 'Offensive'
        # Check for defensive move by simulating the opponent's move
        opponent_piece = PIECE_HUMAN if piece == PIECE_AI else PIECE_AI
        for col in range(self.column_count):
            if self.is_column_open(temp_board, col):
                temp_board_copy = temp_board.copy()
                row = self.find_open_row(temp_board_copy, col)
                temp_board_copy[row][col] = opponent_piece
                if self.is_winning_move(temp_board_copy, opponent_piece):
                    return 'Defensive'
        return 'Neutral'


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
        base_depth = 5

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
        """
        Get a list of columns that can accept a new piece.
        The list is generated by checking each column in the board to see if it can accept a new piece.
        """
        playable_columns = []
        for col in range(self.game.column_count):
            # Using the provided board parameter
            if self.game.is_column_open(board, col):
                playable_columns.append(col)
        # print(f"Valid locations: {playable_columns}")  # Debugging statement
        return playable_columns

    def is_game_over(self, board):
        # print("Checking terminal state...")  # Debugging statement
        if self.game.is_winning_move(board, PLAYER_AI):
            # print("Terminal: AI wins")  # Debugging statement
            return True
        if self.game.is_winning_move(board, PLAYER_HUMAN):
            # print("Terminal: Human wins")  # Debugging statement
            return True
        if len(self.find_playable_columns(board)) == 0:
            # print("Terminal: Board full")  # Debugging statement
            return True
        return False

    def assess_line(self, line_segment, piece):
        score = 0
        opponent_piece = PIECE_HUMAN
        if piece == PIECE_HUMAN:
            opponent_piece = PIECE_AI

        if line_segment.count(piece) == 4:
            score += 100
        elif line_segment.count(piece) == 3 and line_segment.count(PIECE_EMPTY) == 1:
            score += 5
        elif line_segment.count(piece) == 2 and line_segment.count(PIECE_EMPTY) == 2:
            score += 2
        if line_segment.count(opponent_piece) == 3 and line_segment.count(PIECE_EMPTY) == 1:
            score -= 4

        return score

    def evaluate_board_state(self, board, piece):
        """
        Calculate the score for the AI's current board position.
        The score is calculated based on the number of pieces in the center column and the score of all directions on the board.
        """
        score = 0

        # Center column preference (since it's advantageous to play in the center)
        center_array = [int(i) for i in list(
            board[:, self.game.column_count // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

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

    def iterative_deepening_minimax(self, board, max_depth, alpha, beta):
        best_score = float('-inf')
        best_column = None
        for depth in range(1, max_depth + 1):
            column, score, _, _ = self.minimax(board, depth, alpha, beta, True)
            if score > best_score:
                best_score = score
                best_column = column
        return best_column, best_score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        start_time = time.time()
        board_key = str(board)  # Convert board to a hashable type
        if (board_key, depth, maximizingPlayer) in self.transposition_table:
            return self.transposition_table[(board_key, depth, maximizingPlayer)]

        playable_columns = self.find_playable_columns(board)
        is_terminal = self.is_game_over(board)
        total_nodes_explored = 0

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.game.is_winning_move(board, PLAYER_AI):
                    score = POSITIVE - \
                        (self.game.row_count * self.game.column_count - depth)
                elif self.game.is_winning_move(board, PLAYER_HUMAN):
                    score = NEGATIVE + \
                        (self.game.row_count * self.game.column_count - depth)
                else:  # Game is over with no winner
                    score = 0
            else:  # Depth is zero
                score = self.evaluate_board_state(board, PLAYER_AI)
            end_time = time.time()
            decision_time = end_time - start_time
            return None, score, decision_time, 1

        if maximizingPlayer:
            value = float('-inf')
            column = random.choice(
                playable_columns) if playable_columns else None
            for col in playable_columns:
                row = self.game.find_open_row(board, col)
                b_copy = board.copy()
                self.game.place_disc(b_copy, row, col, PLAYER_AI)
                new_score, _, _, explored = self.minimax(
                    b_copy, depth - 1, alpha, beta, False)
                total_nodes_explored += explored
                if new_score is not None and new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

        else:
            value = float('inf')
            column = random.choice(
                playable_columns) if playable_columns else None
            for col in playable_columns:
                row = self.game.find_open_row(board, col)
                b_copy = board.copy()
                self.game.place_disc(b_copy, row, col, PLAYER_HUMAN)
                new_score, _, _, explored = self.minimax(
                    b_copy, depth - 1, alpha, beta, True)
                total_nodes_explored += explored
                if new_score is not None and new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break

        end_time = time.time()
        decision_time = end_time - start_time
        self.transposition_table[(board_key, depth, maximizingPlayer)] = (
            column, value, decision_time, total_nodes_explored + 1)
        return column, value, decision_time, total_nodes_explored + 1


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
        draw_board(game.board)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER_HUMAN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    clicked_column = pos_x // CELL_SIZE
                    if game.is_column_open(game.board, clicked_column):
                        row = game.find_open_row(
                            game.board, clicked_column)
                        game.place_disc(game.board, row,
                                        clicked_column, PIECE_HUMAN)
                        if game.is_winning_move(game.board, PIECE_HUMAN):
                            game_over = True
                        turn = PLAYER_AI

                        draw_board(game.board)

            # Inside the main game loop
            if turn == PLAYER_AI and not game_over:
                game.ai.transposition_table.clear()  # Clear the transposition table
                dynamic_depth = game.ai.calculate_dynamic_depth(game.board)
                column, _ = game.ai.iterative_deepening_minimax(
                    game.board, dynamic_depth, float('-inf'), float('inf'))
                if column is not None:
                    if game.is_column_open(game.board, column):
                        row = game.find_open_row(game.board, column)
                        game.place_disc(game.board, row, column, PIECE_AI)
                        if game.is_winning_move(game.board, PIECE_AI):
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
        if game.is_winning_move(game.board, PIECE_HUMAN):
            display_message(screen, "Congratulations! You win!")
        elif game.is_winning_move(game.board, PIECE_AI):
            display_message(screen, "AI wins! Better luck next time.")
        else:
            display_message(screen, "It's a draw!")

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_input = False
                        game.reset_game()
                        draw_board(game.board)
                        # main()  # Restart the game
                        break
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    while True:
        main()
