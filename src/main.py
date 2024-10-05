import pygame
import sys

from constants import *
from game import Game


class Main:
    def __init__(self):
        """
        Initializes the main class and sets up pygame, a game object, dragger object, board object, and themes object.

        :return: None
        """
        pygame.init()
        pygame.display.set_caption("Chess")
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        self.dragger = self.game.dragger
        self.board = self.game.board
        self.themes = self.game.themes
        
        
    
    def event_manager(self,
                      event: pygame.event
                      ) -> None:
        """
        Manages events from pygame.event.get().

        :param event: event returned by pygame.event.get()
        :return: None
        """
        # RESET
        if event.type == pygame.KEYDOWN and event.dict['key'] == UP_ARROW_NUM:
            self.game.__init__()
            self.dragger = self.game.dragger
            self.board = self.game.board
            self.themes = self.game.themes
            
        # SET PREV THEME
        elif event.type == pygame.KEYDOWN and event.dict['key'] == LEFT_ARROW_NUM:
            self.themes.set_prev_theme()
            
        # SET NEXT THEME
        elif event.type == pygame.KEYDOWN and event.dict['key'] == RIGHT_ARROW_NUM:
            self.themes.set_next_theme()
            
        # CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.dragger.update_mouse(event.pos)
            clicked_row = self.dragger.mouse_y // SQUARE_SIZE
            clicked_col = self.dragger.mouse_x // SQUARE_SIZE
            
            # The cell has a piece?
            if self.board.squares[clicked_row][clicked_col].has_piece():
                piece = self.board.squares[clicked_row][clicked_col].piece
                # Start dragging a piece
                self.dragger.save_initial((self.dragger.mouse_y, self.dragger.mouse_x))
                self.dragger.drag_piece(piece)
                
        # DRAG
        elif event.type == pygame.MOUSEMOTION:
            # Continue dragging event
            if self.dragger.dragging:
                self.dragger.update_mouse(event.pos)
                self.dragger.update_blit(self.screen)
                
        # UNCLICK
        elif event.type == pygame.MOUSEBUTTONUP:
            # Leave peace on the new place
            if self.dragger.dragging:
                clicked_row, clicked_col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
                self.game.make_move(self.board,
                                    self.dragger.piece,
                                    self.dragger.initial_row, 
                                    self.dragger.initial_col, 
                                    clicked_row, clicked_col)
                self.dragger.undrag_piece()
                # # Logger
                # print(f"From {dragger.initial_row} {dragger.initial_col}\n"
                #       f"Came {clicked_row} {clicked_col} with coos: {dragger.mouse_y} {dragger.mouse_x}\n"
                #       f"Move is the {game.moves_done}th\n"
                #       f"---")
                
        # QUIT
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

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
            if self.dragger.dragging:
                self.dragger.update_blit(self.screen)

            for event in pygame.event.get():
                self.event_manager(event)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()
