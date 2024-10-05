import pygame
import sys

from constants import *
from game import Game


class Main:
    def __init__(self):
        """Initializes the main class and sets up pygame, a game object, dragger object, board object, and themes object."""
        pygame.init()
        pygame.display.set_caption("Chess")
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

    def event_manager(self,
                      event: pygame.event
                      ) -> None:
        # RESET
        if event.type == pygame.KEYDOWN and event.dict['key'] == UP_ARROW_NUM:
            self.game.__init__()
            
            return

        # # RESIZE
        # SHOULD BE REWORKED. FUCKING UP THE CONSTANTS
        # elif event.type == pygame.VIDEORESIZE:
        #     # Make the window a square, dividable by 8
        #     new_size = min(event.size) - event.size % 8
            
        #     WIDTH = new_size
        #     HEIGHT = new_size
            
        #     self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        #     print(event.size)
            
        #     return

        # SET PREV THEME
        elif event.type == pygame.KEYDOWN and event.dict['key'] == LEFT_ARROW_NUM:
            self.game.themes.set_prev_theme()
            
            return

        # SET NEXT THEME
        elif event.type == pygame.KEYDOWN and event.dict['key'] == RIGHT_ARROW_NUM:
            self.game.themes.set_next_theme()
            
            return

        # CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.game.dragger.update_mouse(event.pos)
            clicked_row = self.game.dragger.mouse_y // SQUARE_SIZE
            clicked_col = self.game.dragger.mouse_x // SQUARE_SIZE

            # The cell has a piece?
            if self.game.board.squares[clicked_row][clicked_col].has_piece():
                piece = self.game.board.squares[clicked_row][clicked_col].piece
                # Start dragging a piece
                self.game.dragger.save_initial((self.game.dragger.mouse_y, self.game.dragger.mouse_x))
                self.game.dragger.drag_piece(piece)
                
                return

        # DRAG
        elif event.type == pygame.MOUSEMOTION:
            # Continue dragging event
            if self.game.dragger.dragging:
                self.game.dragger.update_mouse(event.pos)
                self.game.dragger.update_blit(self.screen)
                
                return
                
        # UNCLICK
        elif event.type == pygame.MOUSEBUTTONUP:
            # Leave peace on the new place
            if self.game.dragger.dragging:
                clicked_row, clicked_col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
                self.game.make_move(self.game.dragger.initial_row,
                                    self.game.dragger.initial_col, 
                                    clicked_row,
                                    clicked_col)
                self.game.dragger.undrag_piece()
                
                return 

        # QUIT
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
            
            return

        return

    def mainloop(self):
        """
        Main game loop.

        While the game is running, it will continuously display the background and pieces, check for events, and update the display.

        :return: None
        """
        while True:
            self.game.show_bg(self.screen)
            self.game.show_pieces(self.screen)

            # Update piece blit while drugging
            if self.game.dragger.dragging:
                self.game.dragger.update_blit(self.screen)

            for event in pygame.event.get():
                self.event_manager(event)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()
