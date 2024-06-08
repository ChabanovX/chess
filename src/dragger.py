import pygame

from constants import *


class Dragger:

    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0

        self.piece = None
        self.dragging = False

    def update_mouse(self, pos):
        self.mouse_x, self.mouse_y = pos

    def save_initial(self, pos):
        """
        # Save initial row and column.

        :param pos: (x, y) coordinates
        """
        self.initial_row = pos[0] // SQUARE_SIZE  # Y-position
        self.initial_col = pos[1] // SQUARE_SIZE  # X-position

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def update_blit(self, surface: pygame.Surface):
        """ Create motion while 'holding' a peace """
        self.piece.set_texture(size=128)
        img = pygame.image.load(self.piece.texture)
        img_center = self.mouse_x, self.mouse_y

        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)
