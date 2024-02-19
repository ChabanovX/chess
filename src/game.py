import pygame

from constants import *
from board import Board
from dragger import Dragger


class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.moves_done = 0
        self.rgb_themes = [[(240, 240, 240), (130, 0, 0)],
                           []]
        self.moves = []

    def show_bg(self, surface: pygame.Surface):
        """
        SHOW CHESSBOARD
        :param surface: SHIT
        """
        for row in range(ROWS):
            for col in range(COLUMNS):
                color = (240, 240, 240) if (row + col) % 2 == 0 else (130, 0, 0)
                # MOVE HIGHLIGHTING
                if self.moves:
                    if self.moves[-1][0] == (row, col) or self.moves[-1][1] == (row, col):
                        # color = tuple(map(lambda x: int(x * 1.2) if int(1.2 * x) < 256 else int(x * 0.9), color))
                        color = tuple(int(b - (b - a) * 0.1) for a, b in zip(color, (150, 255, 230)))

                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

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

    def make_move(self, screen, board, dragged_piece, past_row, past_col, cur_row, cur_col):
        """
        SOSO
        :param screen:
        :param board:
        :param dragged_piece:
        :param past_row:
        :param past_col:
        :param cur_row:
        :param cur_col:
        """

        # CHECK IF CURRENT CELL IS IN MATRIX
        if not (0 <= cur_row <= 7 and 0 <= cur_col <= 7):
            board.destroy(past_row, past_col)  # MIGHT DELETE LATER
            self.moves_done += 1
            self.make_sound("capture")
            return

        # TODO CHECK LEGALITY
        if True:
            pass

        # IF THE SAME CELL
        if (cur_row, cur_col) == (past_row, past_col):
            return

        # IF NOT OUR PIECE
        if ((self.moves_done % 2 == 0) + (dragged_piece.color == "white")) % 2 == 1:
            return

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

        return
