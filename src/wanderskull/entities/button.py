import pygame

from ..mouse import cursor


class Button:
    def __init__(self, dimensions: tuple, position: tuple, function):
        """Creates a rectangle button for use in pygame.

        Args:
            dimensions (int, int): width and height of button.
            position (int, int): centre coordinate of button.
            function: function address to be executed on press.
        """
        self.dims = dimensions
        self.pos = position

        self.rect = pygame.Rect(self.pos, self.dims)

        self.color = (30, 30, 35)

        self.function = function

        self.text = ""

    @property
    def w(self) -> int:
        return self.dims[0]

    @property
    def h(self) -> int:
        return self.dims[1]

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    def __str__(self):
        """String representation of button."""
        return f"Button at (centre) {tuple(self.pos)} \
        dimensions of {tuple(self.dims)}."

    def update(self, offHoverText="", onHoverText="", *args):
        """Handles button presses and hovering."""
        self.rect.x = self.x - self.w // 2
        self.rect.y = self.y - self.h // 2
        self.color = (30, 30, 35)

        self.text = offHoverText

        # if button being hovered
        if cursor.rect.colliderect(self.rect):
            self.color = (50, 50, 70)

            self.text = onHoverText

            # if button being clicked
            if cursor.Lclick:
                self.color = (90, 90, 120)

                print("button pressed")
                self.function()

    def render(self, screen, font=None):
        """Renders button in pygame."""
        # print(str(self))
        pygame.draw.rect(screen, self.color, self.rect)

        font = font if font else pygame.font.SysFont("Arial", 40)

        text = font.render(self.text, False, (255, 255, 255))

        screen.blit(text, (self.x - text.get_width() // 2, self.y - self.h // 2))
