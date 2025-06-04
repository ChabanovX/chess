from chess.engine.board import Board


def test_board_dimensions():
    board = Board()
    assert len(board.squares) == 8
    assert all(len(row) == 8 for row in board.squares)
