import pygame
import math

item_library = {
    "sword": ["weapon", 24, 'src/tests/images/wepons/plat-sword.png'],
    "spear": ["weapon", 24, 'src/tests/images/wepons/plat-spear.png'],
    "bomb": ["weapon", 3, 'src/tests/images/wepons/bombs.png']
}

class Item():

    def __init__(self, name, qualities):

        self.name = name
        self.type = qualities[0]
        self.size = qualities[1]

        self.image = pygame.transform.scale(pygame.image.load(qualities[2]), (35, 35))
        self.rect = self.image.get_rect()

        #render effects "the bobbing item"
        self.rise = False
        self.timer_counter = 0

        #on screen
        self.dropped = True

    def render(self, screen, offset):
        if self.dropped:
            #the bobbing effect
            if self.timer_counter == 10 or self.timer_counter == 0:
                self.rise = not self.rise
            if self.rise:
                self.timer_counter += 0.2
            else:
                self.timer_counter -= 0.2
            self.timer_counter = round(self.timer_counter, 2)
            #actual render
            screen.blit(self.image, (self.rect.x-offset[0], self.rect.y+self.timer_counter-offset[1]))
