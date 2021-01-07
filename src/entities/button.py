import pygame
from src.mouse import cursor

class Button():
    def __init__(self, dimensions, position, function):
        self.w, self.h = dimensions
        self.dims = dimensions

        self.pos = position # pos = (width, height)

        self.rect = pygame.Rect(self.pos, self.dims)
        self.color = (30, 30, 35)

        self.function = function

    def update(self, *qargs):
        self.rect.x, self.rect.y = int(self.pos[0] - self.w/2), int(self.pos[1] - self.h/2)
        self.color = (30, 30, 35)
        if cursor.rect.colliderect(self.rect):
            self.color = (50, 50, 70)
            if cursor.Lclick:
                self.color = (90, 90, 120)
                print("pressed")
                self.function()

    def render(self, screen):
        #print(self.pos[0])
        pygame.draw.rect(screen, self.color, self.rect)