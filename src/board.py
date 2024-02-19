from constants import *
from square import Square
from piece import *


class Board:

    def __init__(self):
        self.squares = [[0] * 8 for col in range(COLUMNS)]
        self.pieces = {
            "pawn": Pawn,
            "knight": Knight,
            "bishop": Bishop,
            "rook": Rook,
            "queen": Queen,
            "king": King
        }

        self._create()
        self._add_pieces("black")
        self._add_pieces("white")

    def _create(self):
        """Initializes SQUARE objects in chessboard matrix."""
        for row in range(ROWS):
            for col in range(COLUMNS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color: str):
        """
        Add pieces on the chessboard matrix (in self.squares)
        :param color: color of pieces (black or white)
        """
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # Pawns creation
        for col in range(COLUMNS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Knights creation
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops creation
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks creation
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen and King creation
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def add_piece(self, name: str, row: int, col: int, color: str):
        """
        Add piece to a corresponding cell
        :param name: name of a piece (Ex: "pawn")
        :param row: row of a matrix
        :param col: col of a matrix
        :param color: "black" or "white"
        :return: None
        """
        self.squares[row][col] = Square(row, col, self.pieces[name](color))

    def destroy(self, row: int, col: int):
        """ Makes an empty cell """
        self.squares[row][col] = Square(row, col, None)
