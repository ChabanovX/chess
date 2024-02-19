import pygame
import sys

from constants import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen  # SURFACE
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            if dragger.dragging:  # IF WE DRUG DO SHIT
                dragger.update_blit(screen)
            # BUTTONS
            for event in pygame.event.get():
                # CLICKING
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    # UPDATE COORDINATES
                    clicked_row = dragger.mouse_y // SQUARE_SIZE
                    clicked_col = dragger.mouse_x // SQUARE_SIZE
                    # HAS PIECE ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # SAVE FUCKING COORDINATES
                        dragger.save_initial((dragger.mouse_y, dragger.mouse_x))
                        dragger.drag_piece(piece)

                # MOTION
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        dragger.update_blit(screen)

                # UNCLICKING
                elif event.type == pygame.MOUSEBUTTONUP:
                    # IF DRAGGED SOMETHING
                    if dragger.dragging:
                        clicked_row, clicked_col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
                        game.make_move(screen, board, dragger.piece,
                                       dragger.initial_row, dragger.initial_col, clicked_row, clicked_col)

                        dragger.undrag_piece()

                        print(f"From {dragger.initial_row} {dragger.initial_col}\n"
                              f"Came {clicked_row} {clicked_col} with coos: {dragger.mouse_y} {dragger.mouse_x}\n"
                              f"Move is the {game.moves_done}th\n"
                              f"---")
                    else:
                        pass
                # EXITING
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.update()


main = Main()
main.mainloop()
