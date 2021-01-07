import pygame
import math
from src.mouse import cursor
#phd = placeholder

class main_player(pygame.sprite.Sprite):
    def __init__(self):
        self.height, self.width = 50, 50
        self.x, self.y = (7*50, 7*50)

        self.sprite = pygame.Surface((50,50)) #pygame.image.load('src/tests/images/sample image.png')
        self.sprite.fill((0,255,255))
        self.box = None
        self.canGo = {"down":True, "up":True, "left":True, "right":True}
        self.speed = 5
        self.invincible = False
        self.hp = 3 #phd for now
        self.maxhp = 5 #phd
        self.noMove = False # this can be used in cutscenes or whatever to make the game ignore the movement keys
        self.attackbox = pygame.Surface((20, 70))
        
    
    def firstframe(self):
        #insert json get stuff here
        self.box = pygame.Rect((self.x, self.y),(self.height, self.width))

    def update(self):
        #movement
        self.x = self.box.x
        self.y = self.box.y
        keysdown = pygame.key.get_pressed()
        if not self.noMove:
            moveVectorx = 0
            moveVectory = 0
            if (keysdown[pygame.K_DOWN] or keysdown[pygame.K_s]) and self.canGo["down"]:
                moveVectory = self.speed
            if (keysdown[pygame.K_UP] or keysdown[pygame.K_w]) and self.canGo["up"]:
                moveVectory = -self.speed
            if (keysdown[pygame.K_LEFT] or keysdown[pygame.K_a]) and self.canGo["left"]:
                moveVectorx = -self.speed
            if (keysdown[pygame.K_RIGHT] or keysdown[pygame.K_d]) and self.canGo["right"]:
                moveVectorx = self.speed

        if abs(moveVectorx) == abs(moveVectory) and moveVectorx != 0 and 0 != moveVectory:
            diag = math.sqrt(2)#*(7/(8*math.sqrt(5*self.speed)))
            moveVectorx = math.ceil(moveVectorx/diag)
            moveVectory = math.ceil(moveVectory/diag)
           
        self.canGo = {"down":True, "up":True, "left":True, "right":True}
        self.box.move_ip(moveVectorx, moveVectory)

    def render(self, screen, dims):
        #pygame.draw.rect(screen, (0,255,255), self.box)
        screen.blit(self.sprite, ((dims[1]/2)-25+cursor.mouseoffset[0],(dims[0]/2)-25+cursor.mouseoffset[1]))
        self.attack_prototype(screen)

    def attack(self, screen, type):
        #this would depend on the item wouldnt it?
        pass

    def attack_prototype(self, screen):
        #self.attackbox.x, self.attackbox.y = self.x+20, self.y+10
        #pygame.draw.rect(screen, (0,255,0), self.attackbox)
        pass
        
        

        
player = main_player()

# quick chat(check main for refrance):
# 
