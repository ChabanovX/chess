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


    def _draw_tail(self, surface: pygame.Surface):
        """
        Draws a tail of the previous move

        :param surface: Surface to draw on
        :param theme: Current theme
        """
        
        theme = self.themes.get_current_theme()
        
        outgoing_row = self.moves[-1][0][0]
        outgoing_col = self.moves[-1][0][1]
        ingoing_row = self.moves[-1][1][0]
        ingoing_col = self.moves[-1][1][1]
        
        outgoing_cell = (
            outgoing_col * SQUARE_SIZE,
            outgoing_row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE
            )
        
        ingoing_cell = (
            ingoing_col * SQUARE_SIZE,
            ingoing_row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE
            )
        
        pygame.draw.rect(
            surface, 
            theme["colors"]["touched"][self.check_square_color(outgoing_row, outgoing_col)], # COLOR
            outgoing_cell # PLACE
            )
        
        pygame.draw.rect(
            surface, 
            theme["colors"]["touched"][self.check_square_color(ingoing_row, ingoing_col)], # COLOR
            ingoing_cell # PLACE
            )


    def show_bg(self, surface: pygame.Surface):
        # TODO PNG -> rgb change
        # img = pygame.image.load("assets/images/boards/board_glass.jpeg")
        # img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
        # x = img.get_rect(center=(400, 400))
        # surface.blit(img, x)

        # TODO Might want to check if board is a PNG or a basic color scheme
        
        """Shows the desk"""
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.moves and (self.moves[-1][0] == (row, col) or self.moves[-1][1] == (row, col)):
                    color = self.themes.get_current_theme()["colors"]["touched"]["white"] if (row + col) % 2 == 0 \
                        else self.themes.get_current_theme()["colors"]["touched"]["black"]
                else:
                    color = self.themes.get_current_theme()["colors"]["untouched"]["white"] if (row + col) % 2 == 0 \
                        else self.themes.get_current_theme()["colors"]["untouched"]["black"]
        
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

        if self.moves:
            self._draw_tail(surface)

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
                        
    def _get_possible_squares_for_piece(self, piece, row, col):
        possible_squares = []
        return possible_squares
    
    def _is_square_possible(self, piece, row, col):
        return (row, col) in self._get_possible_squares_for_piece(piece, row, col)

    def _is_move_legal(self, board, dragged_piece, past_row, past_col, cur_row, cur_col,
                       check_for_correct_color=False) -> bool:
        
        # MISSING THE BOARD
        if not (0 <= cur_row <= 7 and 0 <= cur_col <= 7):
            board.destroy(past_row, past_col)  # Unfortunately destroys the piece (Might delete later)
            self.moves_done += 1
            self.make_sound("capture")
            return False

        # SAME SQUARE
        if (cur_row, cur_col) == (past_row, past_col):
            return False

        if check_for_correct_color:
            if (self.moves_done % 2 == 0) != (dragged_piece.color == "white"):
                return False
        
        return True
        
    
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

        if not self._is_move_legal(board, dragged_piece, past_row, past_col, cur_row, cur_col):
            return # Exit
        
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
    def make_sound(move_type, ):
        if move_type == "capture":
            sound = pygame.mixer.Sound(r"assets/sounds/capture.wav")
            pygame.mixer.Sound.play(sound)

            return

        if move_type == "move":
            sound = pygame.mixer.Sound(r"assets/sounds/move.wav")
            pygame.mixer.Sound.play(sound)

            return

        return
    
    @staticmethod
    def check_square_color(row, col):
        if (row + col) % 2 == 0:
            return "white"

        return "black"

