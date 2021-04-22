import pygame
import math

class Inventory():
    
    def __init__(self):
        
        #is inventory on or not?
        self.status = False

        #pics
        self.itemframe = pygame.image.load('src/tests/images/wepons/select.png')
        self.itemframe = pygame.transform.scale(self.itemframe, (144, 108))
        self.inventframe = pygame.transform.scale(self.itemframe,(864, 540))

        self.button = pygame.Surface((120, 90))
        self.button.fill((139,69,19))

        #the actual inventory
        self.storage = [[None for _ in range(4)] for i in range(4)]
        self.storage_view = [[self.itemframe for _ in range(4)] for i in range(4)]

        #mainhand
        self.mainhand = [None, None, None]
        self.mainhand_view = [self.itemframe for _ in range(3)]

        self.selected = None

        #click cooldown
        self.clicking = False

    def show(self, screen, dims):

        #always on screen
        screen.blit(self.button, ((1070, 575)))
        for i in range(3):
            screen.blit(pygame.transform.scale(self.mainhand_view[i], (75, 75)), (985 - 85 * i, 590))
        #if the inventory is open
        if self.status:
            screen.blit(self.inventframe, (180, 67))
            for i in range(4):
                for j in range(4):
                    screen.blit(self.storage_view[i][j], (220 + 154*j, 105 + 118 * i))
            for i in range(3):
                screen.blit(self.mainhand_view[i], (836, 164 + 118*i))

