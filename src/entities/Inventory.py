from src.entities.Item import Item
import pygame
import math

pygame.font.init()

class Cell():

    def __init__(self):
        self.stored = None
        self.space = 24
        self.count = 0 #number of items stored here
        #Cell surface
        self.surf = pygame.Surface((80, 80))
        #sketchy way to make the background transparent
        self.surf.fill((69, 69, 69))
        self.surf.set_colorkey((69, 69, 69))
        #blit the image on
        self.frameimage = pygame.image.load('src/tests/images/wepons/select.png')
        self.surf.blit(pygame.transform.scale(self.frameimage, (80, 80)), (0, 0))
        self.font = pygame.font.Font("src/lib/fonts/pixelmix.ttf", 15)
        self.text = ""
        #make a new frame
    
    def re_blit(self):
        self.surf.fill((69, 69, 69))
        self.surf.blit(pygame.transform.scale(self.frameimage, (80, 80)), (0, 0))
        self.surf.blit(pygame.transform.scale(self.stored.image, (80, 80)), (0, 0))
        self.text = self.font.render(str(self.count), False, (255, 255, 255))
        self.surf.blit(self.text, (80 - self.text.get_width(), 80 - self.text.get_height()))
    
    def set_to(self, it):
        if it == None:
            self.count = 0
            self.stored = None
            self.space = 24
            self.text = ""
            self.surf.fill((69, 69, 69))
        else:
            self.count = 1
            self.stored = it
            self.space -= self.stored.size
            self.re_blit()
    
    def add_item(self, count):
        self.count += count
        self.space -= self.stored.size
        #blit
        self.re_blit()
    
    def render(self, screen, xy):
        screen.blit(self.surf, (xy[0], xy[1]))

class Inventory():
    
    def __init__(self):
        
        #is inventory on or not?
        self.status = False

        #pics
        self.itemframe = pygame.image.load('src/tests/images/wepons/select.png')
        self.itemframe = pygame.transform.scale(self.itemframe, (80, 80))
        self.inventframe = pygame.transform.scale(self.itemframe,(864, 540))

        self.button = pygame.Surface((120, 90))
        self.button.fill((139,69,19))

        #the actual inventory
        #mainhand is the first 3 cells
        self.inv = [Cell() for i in range(43)]
        self.selected = None
        self.using = None

        #click cooldown
        self.clicking = False
    
    def auto_fill(self, item):
        
        #auto fill in the inventory
        flag = False
        for i in range(43):
            if self.inv[i].stored != None and self.inv[i].stored.name == item.name and self.inv[i].space >= item.size:
                self.inv[i].add_item(1)
                flag = True
                break
        if not flag:
            for i in range(43):
                if self.inv[i].stored == None:
                    self.inv[i].set_to(item)
                    flag = True
                    break
        if not flag:
            #do stuff here when the inventory is filled
            print("inventory full")

    def show(self, screen, dims):

        #always on screen
        screen.blit(self.button, ((1070, 580)))
        for i in range(3):
            self.inv[i].render(screen, (815 + 85 * i, 590))
        #if the inventory is open
        if self.status:
            screen.blit(self.inventframe, (180, 67))
            for i in range(5):
                for j in range(8):
                    self.inv[i*8+j+3].render(screen, (220 + 85*j, 130 + 85 * i))
            for i in range(3):
                self.inv[i].render(screen, (920, 215+85*i))
