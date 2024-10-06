
class Square:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.is_clicked = False

    def has_piece(self) -> bool:
        return self.piece is not None

    def has_team_piece(self, moves_done: int):
        pass

    def has_rival_piece(self, moves_done: int):
        pass

