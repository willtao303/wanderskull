import pygame
from src.mouse import cursor


class Button():
    def __init__(self, dimensions, position, function):
        """Creates a rectangle button for use in pygame.

        Args:
            dimensions (int, int): width and height of button.
            position (int, int): centre coordinate of button.
            function: function address to be executed on press.
        """
        self.w, self.h = dimensions
        self.dims = dimensions

        self.pos = position  # pos = (width, height) <- (x, y) ?

        self.rect = pygame.Rect(self.pos, self.dims)

        self.color = (30, 30, 35)

        self.function = function

    def __str__(self):
        """String representation of button."""
        return f"Button at (centre) {tuple(self.pos)} \
        dimensions of {tuple(self.dims)}."

    def update(self, *qargs):  # note: *qargs is unused ?
        """Handles button presses and hovering."""
        self.rect.x = int(self.pos[0] - self.w/2)
        self.rect.y = int(self.pos[1] - self.h/2)
        self.color = (30, 30, 35)
        
        if cursor.rect.colliderect(self.rect):
            self.color = (50, 50, 70)
            if cursor.Lclick:
                self.color = (90, 90, 120)
                print("pressed")
                self.function()

    def render(self, screen):
        """Renders button in pygame."""
        # print(str(self))
        pygame.draw.rect(screen, self.color, self.rect)
