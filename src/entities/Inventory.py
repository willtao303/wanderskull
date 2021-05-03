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
        self.surf.blit(pygame.transform.scale(self.frameimage, (75, 75)), (2.5, 2.5))
        self.font = pygame.font.Font("src/lib/fonts/pixelmix.ttf", 15)
        self.text = ""

        self.selected = False
        self.mainhand = False
    
    def re_blit(self):
        #mainhand is true when blit and false right after to avoid having the inventory light up too
        if self.mainhand:
            self.surf.fill((255, 0, 0))
        elif self.selected:
            self.surf.fill((0, 255, 255))
        else:
            self.surf.fill((69, 69, 69))
        self.surf.blit(pygame.transform.scale(self.frameimage, (75, 75)), (2.5, 2.5))
        if self.stored != None:
            self.surf.blit(pygame.transform.scale(self.stored.image, (70, 70)), (5, 5))
            self.text = self.font.render(str(self.count), False, (255, 255, 255))
            self.surf.blit(self.text, (75- self.text.get_width(), 72- self.text.get_height()))
    
    def set_to(self, it):
        if it == None:
            self.count = 0
            self.stored = None
            self.space = 24
            self.text = ""
            self.re_blit()
        else:
            self.count = 1
            self.stored = it
            self.space -= self.stored.size
            self.re_blit()
    
    def add_item(self, count):
        #the name is deceptive, you can take items
        self.count += count
        self.space -= self.stored.size * count
        #blit
        if self.count == 0:
            self.set_to(None)
        else:
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
        # selected is an index
        self.selected = -1
        #mainhand is also an index
        self.mainhand = 5
        #mainhand has a resting index of 5 becuase by the time index 5 is rendered,
        #it would be false again

        #click cooldown
        self.clicking = False
    
    def main_hand(self, pos):
        if pos == self.mainhand:
            self.mainhand = 5
        else:
            self.mainhand = pos
    
    def select(self, pos):
        #get actual coords
        if pos[0] < 184:
            x, y= (pos[0]-44)//17, (pos[1]-26)//17
            cur =  x + 3 + y * 8
        else:
            y = (pos[1]-43)//17
            cur = y
        if cur == self.selected:
            #if clicking on a selected box, set selection to none
            self.inv[cur].selected = False
            self.inv[cur].re_blit()
            self.selected = -1
        elif self.selected != -1:
            if (self.inv[cur].stored != None and self.inv[self.selected].stored != None and 
            self.inv[self.selected].stored.name == self.inv[cur].stored.name and 
            self.inv[cur].space >= self.inv[self.selected].stored.size):
                # transfer from selected to new, selected is not full & they store the same thing
                can_take = self.inv[cur].space // self.inv[self.selected].stored.size
                if self.inv[self.selected].count <= can_take:
                    self.inv[cur].add_item(self.inv[self.selected].count)
                    self.inv[self.selected].set_to(None)
                else:
                    self.inv[cur].add_item(can_take)
                    self.inv[self.selected].add_item(-can_take)
            #do swap
            else:
                self.inv[self.selected], self.inv[cur] = self.inv[cur], self.inv[self.selected]
            self.inv[self.selected].selected, self.inv[cur].selected = False, True
            self.inv[self.selected].re_blit()
            self.selected = cur
            self.inv[cur].re_blit()
        else:
            #first selection
            self.selected = cur
            self.inv[self.selected].selected = True
            self.inv[self.selected].re_blit()
    
    def auto_fill(self, item):
        
        #auto fill in the inventory
        flag = False
        #check for same items
        for i in range(43):
            if self.inv[i].stored != None and self.inv[i].stored.name == item.name and self.inv[i].space >= item.size:
                self.inv[i].add_item(1)
                flag = True
                break
        #check for empty slots
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
        #make mainhand light up but not in the inventory
        self.inv[self.mainhand].mainhand = True
        self.inv[self.mainhand].re_blit()
        for i in range(3):
            self.inv[i].render(screen, (815 + 85 * i, 590))
        self.inv[self.mainhand].mainhand = False
        self.inv[self.mainhand].re_blit()
        #if the inventory is open
        if self.status:
            screen.blit(self.inventframe, (180, 67))
            for i in range(5):
                for j in range(8):
                    self.inv[i*8+j+3].render(screen, (220 + 85*j, 130 + 85 * i))
            for i in range(3):
                self.inv[i].render(screen, (920, 215+85*i))
        
        #self.inv[0].selected(True)
