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
        
    def reset(self):
        self.board = Board()
        self.dragger = Dragger()
        self.moves_done = 0
        self.moves = []

    def _draw_tail(self, surface: pygame.Surface):
        """Draws a tail of the previous move"""
        
        if not self.moves:
            return

        theme = self.themes.get_current_theme()["colors"]
        last_move = self.moves[-1]

        outgoing_row = last_move[0][0]
        outgoing_col = last_move[0][1]
        ingoing_row = last_move[1][0]
        ingoing_col = last_move[1][1]
        
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
            theme["touched"][self.check_square_color(outgoing_row, outgoing_col)], # COLOR
            outgoing_cell # PLACE
            )
        
        pygame.draw.rect(
            surface, 
            theme["touched"][self.check_square_color(ingoing_row, ingoing_col)], # COLOR
            ingoing_cell # PLACE
            )


    def render_board(self, surface: pygame.Surface):
        # TODO PNG -> rgb change
        # img = pygame.image.load("assets/images/boards/board_glass.jpeg")
        # img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
        # x = img.get_rect(center=(400, 400))
        # surface.blit(img, x)

        # TODO Might want to check if board is a PNG or a basic color scheme
        # Now this is only working with RGB
        
        """Renders the desk"""
        current_theme = self.themes.get_current_theme()["colors"]
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board.squares[row][col].is_clicked:
                    color = current_theme["clicked"]["white"] if (row + col) % 2 == 0 \
                        else current_theme["clicked"]["black"]
                else:
                    color = current_theme["untouched"]["white"] if (row + col) % 2 == 0 \
                        else current_theme["untouched"]["black"]
        
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

        self._draw_tail(surface)

    def render_pieces(self, surface: pygame.Surface):
        # If peace was clicked it should produce possible moves. TODO
        
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        if piece.is_clicked:
                            piece.set_texture(size=128)
                        else:
                            piece.set_texture(size=80)
                            
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)


    def _get_possible_squares_for_piece(self, row, col, color):
        piece_name = self.board.squares[row][col].piece.name
        return piece_name
        
        # Let's restrict eating self color piece first
        # Only pawns depend on the color
        
        # We need to know if on a square exist a piece
        # Also check boundaries
        # Also check pins
        
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
        
    
    def make_move(self, past_row, past_col, cur_row, cur_col):
        """Makes a move with params"""
        if not self._is_move_legal(self.board, self.dragger.piece, past_row, past_col, cur_row, cur_col):
            return # Exit
        
        self._make_sound(cur_row, cur_col)
        
        self.moves.append([(past_row, past_col), (cur_row, cur_col)])
        self.board.add_piece(self.dragger.piece.name, cur_row, cur_col, self.dragger.piece.color)
        self.board.destroy(past_row, past_col)

        self.moves_done += 1


    def _make_sound(self, row, col):
        if self.board.squares[row][col].has_piece():
            sound = pygame.mixer.Sound(r"assets/sounds/capture.wav")  
        else:
            sound = pygame.mixer.Sound(r"assets/sounds/move.wav")
            
        pygame.mixer.Sound.play(sound)
        return
    
    @staticmethod
    def check_square_color(row, col):
        if (row + col) % 2 == 0:
            return "white"

        return "black"

