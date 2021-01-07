import pygame

class Mouse():
    def __init__(self):
        self.x, self.y = 0, 0
        self.hitbox = (10, 10)
        self.rect = pygame.Rect((self.x, self.y), self.hitbox)
        self.Rclick = False
        self.Lclick = False
        self.scroll = 0
        self.mouseoffset = [0,0]

    def update(self, scroll):
        self.Rclick = False
        self.Lclick = False
        self.scroll = scroll
        self.x, self.y = pygame.mouse.get_pos()
        mclick = pygame.mouse.get_pressed()
        if mclick[0]:
            self.Lclick = True
        elif mclick[2]:
            self.Rclick = True
        self.rect.x, self.rect.y = self.x, self.y

    def render(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect)

cursor = Mouse()