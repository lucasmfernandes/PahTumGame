import pygame
import random
import time
import sys
import numpy as np
from copy import deepcopy

B_SIZE = 7
BLACK_HOLES = 5

# --------- Graph ----------#
PLAYER_1_COLOR = (255, 255, 255) #white
PLAYER_2_COLOR = (255, 0, 0) #red
BLACK_HOLE_COLOR = (0,0,0) #black
EMPTY_CELL_COLOR = (161, 102, 47) #wood
BOARD_COLOR = (161, 102, 47) #wood
CELL_SIZE = 100
WIDTH = B_SIZE * CELL_SIZE
HEIGHT = B_SIZE * CELL_SIZE
# --------- Graph ----------#

class State:

    def __init__(self):
        self.board = np.zeros((B_SIZE, B_SIZE))
        self.available_moves = []
        self.player = 1
        self.winner = -1

        for _ in range(BLACK_HOLES + 1):
            row, col = np.random.randint(B_SIZE), np.random.randint(B_SIZE)
            self.board[row, col] = -1  # Place a black hole with value -1

        for row in range(B_SIZE):
            for col in range(B_SIZE):
                if self.board[row, col] == 0:  # If the position is empty
                    self.available_moves.append([row, col])


    def move(self, row, col):
        state_copy = deepcopy(self)
        state_copy.board[row][col] = self.player
        state_copy.available_moves.remove([row, col])
        state_copy.player = 3 - self.player
        return state_copy

    def check_line(self, n, player, values):
        """
        Check if there is a line of 'n' stones of the given player in the list of values.
        :param n: Number of stones in a sequence
        :param player: Player to check for
        :param values: List of values to check (e.g., row, column, diagonal)
        :return: True if there is a line of 'n' stones of the given player, False otherwise
        """
        num_pieces = sum(1 for val in values if val == player)
        return num_pieces >= n

    def count_lines(self, player):
        """
        Count the number of lines for the given player on the board.
        :param player: Player to count lines for
        :return: Total number of lines for the given player
        """
        total_lines = 0
        for row in range(B_SIZE):
            for col in range(B_SIZE):
                # Horizontal line
                if col <= B_SIZE - 4:
                    if self.check_line(4, player, self.board[row, col:col+4]):
                        total_lines += 1
                # Vertical line
                if row <= B_SIZE - 4:
                    if self.check_line(4, player, self.board[row:row+4, col]):
                        total_lines += 1
        return total_lines

    def evaluate_board(self, player):
        """
        Evaluate the current state of the board for the given player.
        :param player: Player to evaluate the board for
        :return: Evaluation score for the given player
        """
        # Calculate points based on the number of lines for the given player
        num_lines = self.count_lines(player)
        if num_lines >= 7:
            return 119
        elif num_lines == 6:
            return 56
        elif num_lines == 5:
            return 25
        elif num_lines == 4:
            return 10
        elif num_lines == 3:
            return 3
        else:
            return 0
        

class PahTumGame:
    
    def __init__(self, player_1_ai, player_2_ai):
        self.state = State()
        self.player_1_ai = player_1_ai
        self.player_2_ai = player_2_ai

    def end_game(self):
        """
        Check if the game has ended (board is full). If the game has ended, evaluate the board for each player and determine the winner based on the points earned.
        :return: Winner of the game (1 for white, 2 for red, 0 for draw, -1 if the game has not ended)
        """
        if not self.state.available_moves:  # Check if there are no available moves left (board is full)
            # Evaluate the board for each player
            white_points = self.state.evaluate_board("white")
            red_points = self.state.evaluate_board("red")
        
            # Determine the winner based on the points earned
            if white_points > red_points:
                return 1  # Player 1 (white) wins
            elif white_points < red_points:
                return 2  # Player 2 (red) wins
            else:
                return 0  # Draw
        else:
            return -1  # Game has not ended
        
    def start(self, log_moves=False):
        self.state = State()
        
        # --------- Graph ----------#
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pah Tum")
        font = pygame.font.SysFont("Arial", 80)
        clock = pygame.time.Clock()
        # --------- Graph ----------#
        
        while True:             
            if self.state.player == 1:  # Adjusted player identification for Pah Tum
                self.player_1_ai(self)
            else:
                self.player_2_ai(self)

            # --------- Graph ----------#
            pygame.time.wait(100)
            screen.fill(BOARD_COLOR)
            for row in range(B_SIZE):  # Adjusted board size for Pah Tum
                for col in range(B_SIZE):  # Adjusted board size for Pah Tum
                    color = EMPTY_CELL_COLOR
                    if self.state.board[row][col] == 1:
                        color = PLAYER_1_COLOR
                    elif self.state.board[row][col] == 2:
                        color = PLAYER_2_COLOR
                    elif self.state.board[row][col] == -1:  # Black hole color
                        color = BLACK_HOLE_COLOR
                    pygame.draw.circle(screen, color, (int(col * CELL_SIZE + CELL_SIZE / 2), int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), int(CELL_SIZE / 2.2))
            # --------- Graph ----------#
            
            # Adjusted function calls and print statements for Pah Tum
            print("L1:", self.state.count_lines(1), " L2:", self.state.count_lines(2))
            
            game_status = self.end_game()  # Check if the game has ended
            if game_status != -1:
                # --------- Graph ----------#
                if game_status == 0:
                    text = font.render("Draw!", True, (0, 0, 0))
                else:
                    text = font.render(f"Player {game_status} wins!", True, (0, 0, 0))
                screen.blit(text, (int(WIDTH / 2 - text.get_width() / 2), int(HEIGHT / 2 - text.get_height() / 2)))
                pygame.display.flip()
                pygame.time.wait(200)
                # --------- Graph ----------#
                break
            
            # --------- Graph ----------#
            pygame.display.flip()
            clock.tick(60)
            pygame.time.wait(50)
            # --------- Graph ----------#
    
    def run_n_matches(self, n, max_time=3600, log_moves=False):
        start_time = time.time()
        
        results = [0, 0, 0] # [draws, player 1 victories, player 2 victories]
        
        while n > 0 and time.time() - start_time < max_time:
            n -= 1
            self.start(log_moves)  # Adjusted method call for Pah Tum
            results[self.end_game()] += 1
            
        print("\n=== Elapsed time: %s seconds ===" % (int(time.time() - start_time)))
        print(f"  Player 1: {results[1]} victories")
        print(f"  Player 2: {results[2]} victories")
        print(f"  Draws: {results[0]} ")
        print("===============================")
        pygame.quit()


def execute_random_move(game):
    # Randomly select an available move (empty intersection) on the board
    move = random.choice(game.state.available_moves)
    # Place a stone of the current player at the selected move
    row, col = move
    game.state.board[row][col] = 1 if game.state.player == 1 else 2
    # Remove the selected move from the list of available moves
    game.state.available_moves.remove(move)
    # Update player turn
    game.state.player = 2 if game.state.player == 1 else 1

game = PahTumGame(execute_random_move, execute_random_move)
game.run_n_matches(1)