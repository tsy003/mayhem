# coding=utf-8
''' Author - Torkel Syversen '''
import pygame

class Label:
    '''
        Creates a font, with given system font name.
        rounded is round corners.
    '''
    def __init__(self, font_name, size, rounded=True):
        self.f = pygame.font.SysFont(font_name, size)
        self.font_name = font_name
        self.rounded = rounded
        self.color = (0, 255, 255)

    # Rendering font, this creates a surface with the text width and height
    # Then blit given surface to the main screen
    def render(self, surface, text, x, y):
        surface.blit(self.f.render(text, self.rounded, self.color), (x, y))

    def set_color(self, c):
        self.color = c

    def get_size(self, txt):
        return self.f.size(txt)

    def set_size(self, size):
        # Creates new font with given size
        self.f = pygame.font.SysFont(self.font_name, size)
