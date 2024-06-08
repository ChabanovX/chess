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
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        themes = self.game.themes

        while True:

            game.show_bg(screen)
            game.show_pieces(screen)

            # Update piece blit while drugging
            if dragger.dragging:
                dragger.update_blit(screen)

            # value = pygame.event.get()
            # if value:
            #     print(value)

            # Check events
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN and event.dict['key'] == UP_ARROW_NUM:
                    game.__init__()
                    dragger = self.game.dragger
                    board = self.game.board
                    themes = self.game.themes

                elif event.type == pygame.KEYDOWN and event.dict['key'] == LEFT_ARROW_NUM:
                    themes.set_prev_theme()

                elif event.type == pygame.KEYDOWN and event.dict['key'] == RIGHT_ARROW_NUM:
                    themes.set_next_theme()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouse_y // SQUARE_SIZE
                    clicked_col = dragger.mouse_x // SQUARE_SIZE
                    # The cell has a piece?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # Start dragging a piece
                        dragger.save_initial((dragger.mouse_y, dragger.mouse_x))
                        dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEMOTION:
                    # Continue dragging event
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Leave peace on the new place
                    if dragger.dragging:
                        clicked_row, clicked_col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
                        game.make_move(board, dragger.piece,
                                       dragger.initial_row, dragger.initial_col, clicked_row, clicked_col)

                        dragger.undrag_piece()  # As we do not drag anymore

                        # # Logger
                        # print(f"From {dragger.initial_row} {dragger.initial_col}\n"
                        #       f"Came {clicked_row} {clicked_col} with coos: {dragger.mouse_y} {dragger.mouse_x}\n"
                        #       f"Move is the {game.moves_done}th\n"
                        #       f"---")

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()
