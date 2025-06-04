import pygame
import sys

from constants import *
from exceptions import *
from game import Game


class Main:
    def __init__(self):
        """Initializes the main class and sets up pygame, a game object, dragger object, board object, and themes object."""
        pygame.init()
        pygame.display.set_caption("Chess")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

    def _do_event_quit(self) -> None:
        pygame.quit()
        sys.exit(0)
        
    def _do_event_reset(self) -> None:
        self.game.reset()
        
    def _do_event_change_theme(self, set_next_theme: bool) -> None:
        if set_next_theme:
            self.game.themes.set_next_theme()
        else:
            self.game.themes.set_prev_theme()
            
    def _do_event_motion(self, event: pygame.event) -> None:
        """
        Handles mouse motion events in the Pygame window.
        
        This function processes the movement of the mouse within the game window and updates
        any necessary game state based on the new mouse position. Typically used to update
        UI elements like hovering effects or highlighting tiles on the chessboard when the
        mouse is moved.
        
        Args:
            event (pygame.event): The motion event triggered by the mouse moving in the window.
        
        Returns:
            None
        """

        if self.game.dragger.dragging:
            self.game.dragger.update_mouse(event.pos)
            self.game.dragger.render_piece_motion(self.screen)
        else:
            pass


    def _do_event_click(self, event: pygame.event) -> None:
        self.game.dragger.update_mouse(event.pos)
        clicked_row = self.game.dragger.mouse_y // SQUARE_SIZE
        clicked_col = self.game.dragger.mouse_x // SQUARE_SIZE
        
        if clicked_col > 7 or clicked_row > 7:
            raise OutOfBoundsException(f"Click out of bounds: row={clicked_row}, col={clicked_col}")
        
        clicked_cell = self.game.board.squares[clicked_row][clicked_col]
        
        if event.button == LEFT_CLICK_NUM:
            # The cell has a piece?
            if clicked_cell.has_piece():
                piece = clicked_cell.piece
                # Start dragging a piece
                self.game.dragger.save_outgoing_square((clicked_row, clicked_col))
                self.game.dragger.drag_piece(piece)
                
                return
            
        elif event.button == RIGHT_CLICK_NUM:
            clicked_cell.is_clicked = not clicked_cell.is_clicked
            
            return
        
    def _do_event_unclick(self, event: pygame.event) -> None:
            # Leave piece on the new place if been dragged
            if self.game.dragger.dragging:
                clicked_row = event.pos[1] // SQUARE_SIZE
                clicked_col = event.pos[0] // SQUARE_SIZE
                self.game.make_move(self.game.dragger.outgoing_row,
                                    self.game.dragger.outgoing_col, 
                                    clicked_row,
                                    clicked_col)
                self.game.dragger.undrag_piece()
            
            else:
                pass
                
            return 

    def event_manager(self, event: pygame.event) -> None:
        # RESIZE
        # TODO: SHOULD BE REWORKED. FUCKING UP THE CONSTANTS
        # elif event.type == pygame.VIDEORESIZE:
        #     # Make the window a square, dividable by 8
        #     new_size = min(event.size) - event.size % 8
            
        #     WIDTH = new_size
        #     HEIGHT = new_size
            
        #     self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        #     print(event.size)
        #     return
        
        # RESET
        if event.type == pygame.KEYDOWN and event.key == UP_ARROW_NUM:
            self._do_event_reset()
            return

        # SET PREV THEME
        elif event.type == pygame.KEYDOWN and event.key == LEFT_ARROW_NUM:
            self._do_event_change_theme(False)
            return

        # SET NEXT THEME
        elif event.type == pygame.KEYDOWN and event.key == RIGHT_ARROW_NUM:
            self._do_event_change_theme(True)
            return

        # CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._do_event_click(event)
            return

        # DRAG
        elif event.type == pygame.MOUSEMOTION:
            self._do_event_motion(event)
            return
                
        # UNCLICK
        elif event.type == pygame.MOUSEBUTTONUP:
            self._do_event_unclick(event)
            return 

        # QUITTING
        elif event.type == pygame.QUIT:
            self._do_event_quit()
            return

        return

    def mainloop(self):
        """Main game loop."""
        while True:
            self.game.render_board(self.screen)
            self.game.render_pieces(self.screen)

            # Update piece blit while dragging
            if self.game.dragger.dragging:
                self.game.dragger.render_piece_motion(self.screen)

            for event in pygame.event.get():
                self.event_manager(event)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()
