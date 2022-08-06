import pygame
import time


class Board():
    """стакан"""

    def __init__(self, tet_game):
        """"""
        self.screen = tet_game.screen
        self.settings = tet_game.settings
        self.blank_board = self.get_blank_board()
        self.image = pygame.transform.scale(pygame.image.load("images/white.png"), (40, 40))

    def get_blank_board(self):
        """создает новый стакан"""
        board = []
        for i in range(self.settings.board_width):
            board.append([self.settings.blank] * self.settings.board_height)
        return board

    def is_on_board(self, x, y):
        return 0 <= x < self.settings.board_width and y < self.settings.board_height

    def add_to_board(self, board, piece):
        # fill in the board based on piece's location, shape, and rotation
        for x in range(piece.template_width):
            for y in range(piece.template_height):
                if piece.pieces[piece.form['shape']][piece.form['rotation']][y][x] != self.settings.blank:
                    board[x + piece.form['x']][y + piece.form['y']] = piece.form['image']

    def is_complete_line(self, board, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(self.settings.board_width):
            if board[x][y] == self.settings.blank:
                return False
        return True

    def remove_complete_lines(self, board):
        """ Remove any completed lines on the board, move everything above them down,
        and return the number of complete lines."""
        num_lines_removed = 0
        y = self.settings.board_height - 1  # start y at the bottom of the board
        self.draw_removed_line(board, y)
        while y >= 0:
            if self.is_complete_line(board, y):
                # Remove the line and pull boxes down by one line.
                for pull_down_y in range(y, 0, -1):
                    for x in range(self.settings.board_width):
                        board[x][pull_down_y] = board[x][pull_down_y - 1]
                # Set very top line to blank.
                for x in range(self.settings.board_width):
                    board[x][0] = self.settings.blank
                num_lines_removed += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1  # move on to check next row up
        return num_lines_removed

    def draw_removed_line(self, board, y):
        while y >= 0:
            if self.is_complete_line(board, y):
                for x in range(self.settings.board_width):
                    """заполненная линия забивается белыми боксами"""
                    pixel_x = self.settings.x_margin + (x * self.settings.box_size)
                    pixel_y = self.settings.top_margin + (y * self.settings.box_size)
                    self.screen.blit(self.image, (pixel_x, pixel_y))
                    pygame.display.flip()
                    time.sleep(0.03)
            y -= 1

    def is_valid_position(self, board, piece, adj_x=0, adj_y=0):
        # Return True if the piece is within the board and not colliding
        for x in range(piece.template_width):
            for y in range(piece.template_height):
                is_above_board = y + piece.form['y'] + adj_y < 0
                if is_above_board or \
                        piece.pieces[piece.form['shape']][piece.form['rotation']][y][x] == self.settings.blank:
                    continue
                if not self.is_on_board(x + piece.form['x'] + adj_x, y + piece.form['y'] + adj_y):
                    return False
                if board[x + piece.form['x'] + adj_x][y + piece.form['y'] + adj_y] != self.settings.blank:
                    return False
        return True
