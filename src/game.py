import pygame

from constants import *
from board import Board
from dragger import Dragger
from themes import Themes


class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.themes = Themes()
        self.moves_done = 0
        self.moves = []

    # Shit code
    def draw_tail(self, surface: pygame.Surface):
        color = "#33FFFF01"
        rect = (self.moves[-1][0][1] * SQUARE_SIZE, self.moves[-1][0][0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, color, rect)
        rect = (self.moves[-1][1][1] * SQUARE_SIZE, self.moves[-1][1][0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, color, rect)

    def show_bg(self, surface: pygame.Surface):
        # TODO PNG
        img = pygame.image.load("assets/images/boards/board_glass.jpeg")
        # img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
        x = img.get_rect(center=(400, 400))
        surface.blit(img, x)

        # # TODO Might want to check if board is a PNG or a basic color scheme
        # """Shows the desk"""
        # for row in range(ROWS):
        #     for col in range(COLUMNS):
        #         if self.moves and (self.moves[-1][0] == (row, col) or self.moves[-1][1] == (row, col)):
        #             color = self.themes.get_current_theme()["touched"]["white"] if (row + col) % 2 == 0 \
        #                 else self.themes.get_current_theme()["touched"]["black"]
        #         else:
        #             color = self.themes.get_current_theme()["untouched"]["white"] if (row + col) % 2 == 0 \
        #                 else self.themes.get_current_theme()["untouched"]["black"]
        #
        #         rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        #         pygame.draw.rect(surface, color, rect)

        if self.moves:
            self.draw_tail(surface)

    def show_pieces(self, surface: pygame.Surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def make_move(self, board, dragged_piece, past_row, past_col, cur_row, cur_col):
        """
        Makes a move with params
        :param board:
        :param dragged_piece:
        :param past_row:
        :param past_col:
        :param cur_row:
        :param cur_col:
        """
        # TODO All the checks should be in a separate function
        # If cell is in matrix?
        if not (0 <= cur_row <= 7 and 0 <= cur_col <= 7):
            board.destroy(past_row, past_col)  # Unfortunately destroys the piece (Might delete later)
            self.moves_done += 1
            self.make_sound("capture")
            return

        # TODO CHECK LEGALITY
        if True:
            pass

        # IF THE SAME CELL
        if (cur_row, cur_col) == (past_row, past_col):
            return

        # # IF NOT OUR TURN / PIECE
        # if (self.moves_done % 2 == 0) != (dragged_piece.color == "white"):
        #     return

        else:
            # SOUND PRODUCING
            if board.squares[cur_row][cur_col].has_piece():
                sound_type = "capture"
            else:
                sound_type = "move"

            self.moves.append([(past_row, past_col), (cur_row, cur_col)])

            board.add_piece(dragged_piece.name, cur_row, cur_col, dragged_piece.color)
            board.destroy(past_row, past_col)

        self.moves_done += 1
        self.make_sound(sound_type)

    @staticmethod
    def make_sound(move_type):
        if move_type == "capture":
            sound = pygame.mixer.Sound(r"assets/sounds/capture.wav")
            pygame.mixer.Sound.play(sound)

        if move_type == "move":
            sound = pygame.mixer.Sound(r"assets/sounds/move.wav")
            pygame.mixer.Sound.play(sound)

        else:
            pass
