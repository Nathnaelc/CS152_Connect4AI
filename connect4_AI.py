import numpy as np
import pygame
import sys
import math
import random

# Constants for the game
COLOR_BLUE = (100, 0, 180)
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
    def __init__(self, row_count, column_count, ai_depth):
        self.row_count = row_count
        self.column_count = column_count
        self.board = self.create_board()
        self.ai = Connect4AI(self, ai_depth)

    def create_board(self):
        """Create a 2D numpy array for the game board."""
        return np.zeros((self.row_count, self.column_count))

    def drop_piece(self, row, col, piece):
        """Drop a piece in the specified column."""
        self.board[row][col] = piece

    def is_valid_location(self, col):
        cell_value = self.board[self.row_count - 1][col]
        # Debugging print
        print(f"Checking column {col}, cell value: {cell_value}")
        return cell_value == PIECE_EMPTY

    def get_next_open_row(self, col):
        """Find the next open row in the specified column."""
        for r in range(self.row_count):
            if self.board[r][col] == PIECE_EMPTY:
                return r

    def print_board(self):
        """Print the game board."""
        print(np.flip(self.board, 0))

    def reset_game(self):
        """Reset the game by clearing the board and resetting variables."""
        self.board = self.create_board()

    def check_winning_move(self, piece):
        """Check if the last move was a winning move."""
        # Check horizontal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if self.board[r][c] == piece and \
                   self.board[r][c + 1] == piece and \
                   self.board[r][c + 2] == piece and \
                   self.board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if self.board[r][c] == piece and \
                   self.board[r + 1][c] == piece and \
                   self.board[r + 2][c] == piece and \
                   self.board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if self.board[r][c] == piece and \
                   self.board[r + 1][c + 1] == piece and \
                   self.board[r + 2][c + 2] == piece and \
                   self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if self.board[r][c] == piece and \
                   self.board[r - 1][c + 1] == piece and \
                   self.board[r - 2][c + 2] == piece and \
                   self.board[r - 3][c + 3] == piece:
                    return True

        return False

    def evaluate_window(self, window, piece):
        """Evaluate a window of the board and return the score based on the pieces alignment."""
        score = 0
        opponent_piece = PIECE_HUMAN if piece == PIECE_AI else PIECE_AI

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(PIECE_EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(PIECE_EMPTY) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(PIECE_EMPTY) == 1:
            score -= 4

        return score

    def score_board_position(self, board, piece):
        """Calculate the score for the AI's current board position."""
        score = 0

        # Score center column
        center_array = [int(i) for i in list(
            board[:, self.game.column_count // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal, vertical, and diagonal positions
        score += self.evaluate_directions(board, piece)

        return score

    def evaluate_directions(self, board, piece):
        """Evaluate and score all directions on the board."""
        score = 0

        # Score horizontal
        for r in range(self.row_count):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.column_count - 3):
                window = row_array[c:c + WINNING_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for c in range(self.column_count):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.row_count - 3):
                window = col_array[r:r + WINNING_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                window = [board[r + i][c + i] for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Score negative sloped diagonal
        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                window = [board[r + 3 - i][c + i]
                          for i in range(WINNING_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_state(self, board):
        """Check if the board is in a terminal state (win, loss, or draw)."""
        return self.check_winning_move(board, PIECE_HUMAN) or \
            self.check_winning_move(board, PIECE_AI) or \
            len(self.get_valid_locations(board)) == 0


class Connect4AI:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        """Implement the minimax algorithm with alpha-beta pruning."""
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.game.check_winning_move(PLAYER_AI):
                    return (None, 100000000000000)
                elif self.game.check_winning_move(PLAYER_HUMAN):
                    return (None, -100000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, PLAYER_AI))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.game.get_next_open_row(col)
                temp_board = board.copy()
                self.game.drop_piece(temp_board, row, col, PLAYER_AI)
                new_score = self.minimax(
                    temp_board, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.game.get_next_open_row(col)
                temp_board = board.copy()
                self.game.drop_piece(temp_board, row, col, PLAYER_HUMAN)
                new_score = self.minimax(
                    temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self, board):
        """Get a list of columns that can accept a new piece."""
        valid_locations = []
        for col in range(self.game.column_count):
            # Corrected to call is_valid_location without the board parameter
            if self.game.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def is_terminal_node(self, board):
        """Check if the current board state is a terminal node."""
        return self.game.check_winning_move(PLAYER_AI) or \
            self.game.check_winning_move(PLAYER_HUMAN) or \
            len(self.get_valid_locations(board)) == 0

    def score_position(self, board, player):
        """Score the board position."""
        score = 0

        # Center Column Preference
        center_array = [int(i) for i in list(
            board[:, self.game.column_count // 2])]
        center_count = center_array.count(player)
        score += center_count * 3

        # Horizontal Score
        for r in range(self.game.row_count):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.game.column_count - 3):
                window = row_array[c:c + WINNING_LENGTH]
                score += self.game.evaluate_window(window, player)

        # Vertical Score
        for c in range(self.game.column_count):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.game.row_count - 3):
                window = col_array[r:r + WINNING_LENGTH]
                score += self.game.evaluate_window(window, player)

        # Positive Sloped Diagonal
        for r in range(self.game.row_count - 3):
            for c in range(self.game.column_count - 3):
                window = [board[r + i][c + i] for i in range(WINNING_LENGTH)]
                score += self.game.evaluate_window(window, player)

        # Negative Sloped Diagonal
        for r in range(self.game.row_count - 3):
            for c in range(self.game.column_count - 3):
                window = [board[r + 3 - i][c + i]
                          for i in range(WINNING_LENGTH)]
                score += self.game.evaluate_window(window, player)

        return score

    def best_move(self):
        column, minimax_score = self.minimax(
            self.game.board, self.depth, -math.inf, math.inf, True)
        if column is None:
            # Handle the case where no valid move is found

            # You might choose a random valid column or take another specific action
            column = random.choice(self.get_valid_locations(self.game.board))
        return column


def main():
    row_count = int(input("Enter the number of rows: "))
    column_count = int(input("Enter the number of columns: "))
    ai_depth = int(input("Enter the AI depth: "))
    game = Connect4Game(row_count, column_count, ai_depth)

    CELL_SIZE = 100

    pygame.init()

    screen = pygame.display.set_mode(
        (game.column_count * CELL_SIZE, game.row_count * CELL_SIZE))
    game.reset_game()  # Reset the game

    def draw_board(board):
        """Draw the game board."""
        for r in range(game.row_count):
            for c in range(game.column_count):
                pygame.draw.rect(
                    screen, COLOR_BLUE, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if board[r][c] == PIECE_HUMAN:
                    pygame.draw.circle(screen, COLOR_RED, (c * CELL_SIZE + CELL_SIZE //
                                       2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                elif board[r][c] == PIECE_AI:
                    pygame.draw.circle(screen, COLOR_YELLOW, (c * CELL_SIZE + CELL_SIZE //
                                       2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

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
        game.reset_game()  # Reset the game

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close the Pygame window and exit the program
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if turn == PLAYER_HUMAN:
                        # Get human player's input (e.g., mouse position)
                        pos_x, pos_y = pygame.mouse.get_pos()
                        clicked_column = pos_x // CELL_SIZE  # Assuming you have a cell size defined
                        if column is not None and game.is_valid_location(column):
                            row = game.get_next_open_row(clicked_column)
                            game.drop_piece(row, clicked_column, PIECE_HUMAN)
                            if game.check_winning_move(PIECE_HUMAN):
                                # Handle human win (e.g., display message)
                                game_over = True
                            turn = PLAYER_AI

            if turn == PLAYER_AI and not game_over:
                # AI's turn
                column = game.ai.best_move()
                if game.is_valid_location(column):
                    row = game.get_next_open_row(column)
                    game.drop_piece(row, column, PIECE_AI)
                    if game.check_winning_move(PIECE_AI):
                        # Handle AI win (e.g., display message)
                        game_over = True
                    turn = PLAYER_HUMAN

            # Draw board
            draw_board(game.board)
            pygame.display.update()

            # Handling end of the game and displaying messages
        # After the game is over, display the appropriate message
        if game.check_winning_move(PIECE_HUMAN):
            display_message(screen, "Congratulations! You win!")
        elif game.check_winning_move(PIECE_AI):
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
            print("Congratulations! You win!")
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
