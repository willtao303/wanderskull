import pygame
import math
from src.mouse import cursor
from src.entities.Attack import Weapon
from src.entities.Attack import weapon_library
from src.entities.Inventory import Inventory, Cell
from src.entities.Item import Item
#phd = placeholder

class main_player(pygame.sprite.Sprite):
    def __init__(self):
        self.height, self.width = 50, 50
        self.x, self.y = (1*50, 1*50)

        self.sprite = pygame.Surface((50,50)) #pygame.image.load('src/tests/images/sample image.png')
        self.sprite.fill((0,255,255))
        self.box = None
        self.canGo = {"down":True, "up":True, "left":True, "right":True}
        self.speed = 5
        self.invincible = False
        self.noMove = False # this can be used in cutscenes or whatever to make the game ignore the movement keys
        self.attackbox = pygame.Surface((20, 70))

        self.collide = None
        self.moving = False

        #health

        self.max_health = 100 #all of this just for a health bar
        self.health =  100
        self.health_bar = pygame.Surface((400, 30))
        self.health_bar_show = pygame.Surface((400, 30))
        self.health_bar.fill((0,255,0))
        self.health_bar_show.fill((255, 0 ,0))
        self.health_loss = 0
        self.health_loss_bar = None

        #mana

        self.max_mana = 100 #set up for mana
        self.mana = 100
        self.mana_bar = pygame.Surface((400, 30))
        self.mana_bar_show = pygame.Surface((400, 30))
        self.mana_bar.fill((0, 0, 255))
        self.mana_bar_show.fill((255, 255, 0))
        self.mana_loss = 0
        self.mana_loss_bar = None

        #attack

        self.using = Weapon("sword", weapon_library["sword"])
        self.cooldown = 0
        self.attack_counter = 0
        self.points = {"chx":0, "chy":0, "angle":0}
        self.attacks = []

        #inventory

        self.storage = Inventory()
    
    def firstframe(self):
        #insert json get stuff here
        self.box = pygame.Rect((self.x, self.y),(self.height, self.width))

    def update(self):
        #movement
        self.x = self.box.x
        self.y = self.box.y
        keysdown = pygame.key.get_pressed()
        if not self.noMove:

            #moving

            moveVectorx = 0
            moveVectory = 0
            chx, chy = 0, 0

            if self.collide != None:
                self.canGo["down"] = self.canGo["down"] and self.collide.canGo["down"]
                self.canGo["up"] = self.canGo["up"] and self.collide.canGo["up"]
                self.canGo["left"] = self.canGo["left"] and self.collide.canGo["left"]
                self.canGo["right"] = self.canGo["right"] and self.collide.canGo["right"]

                angle = math.atan2(self.y-self.collide.y, self.x-self.collide.x)
                chx += math.cos(angle) * self.collide.speed
                chy += math.sin(angle) * self.collide.speed

            if (keysdown[pygame.K_DOWN] or keysdown[pygame.K_s]) and self.canGo["down"]:
                moveVectory += self.speed
            if (keysdown[pygame.K_UP] or keysdown[pygame.K_w]) and self.canGo["up"]:
                moveVectory += -self.speed
            if (keysdown[pygame.K_LEFT] or keysdown[pygame.K_a]) and self.canGo["left"]:
                moveVectorx += -self.speed
            if (keysdown[pygame.K_RIGHT] or keysdown[pygame.K_d]) and self.canGo["right"]:
                moveVectorx += self.speed
            
            if moveVectorx != 0 or moveVectory != 0:
                self.moving = True
            else:
                self.moving = False

            moveVectorx += chx
            moveVectory += chy

            if not self.canGo["down"]:
                moveVectory = min(0, moveVectory)
            if not self.canGo["up"]:
                moveVectory = max(0, moveVectory)
            if not self.canGo["left"]:
                moveVectorx = max(0, moveVectorx)
            if not self.canGo["right"]:
                moveVectorx = min(0, moveVectorx)

        if abs(moveVectorx) == abs(moveVectory) and moveVectorx != 0 and 0 != moveVectory:
            diag = math.sqrt(2)#*(7/(8*math.sqrt(5*self.speed)))
            moveVectorx = math.ceil(moveVectorx/diag)
            moveVectory = math.ceil(moveVectory/diag)
           
        self.canGo = {"down":True, "up":True, "left":True, "right":True}

        self.box.move_ip(moveVectorx, moveVectory)


    def render(self, screen, dims, walls):
        #pygame.draw.rect(screen, (0,255,255), self.box)
        screen.blit(self.sprite, ((dims[1]/2)-25+cursor.mouseoffset[0],(dims[0]/2)-25+cursor.mouseoffset[1]))
        self.attack(screen, dims, walls)

        #health
        screen.blit(self.health_bar_show, (400, 550))
        screen.blit(self.health_bar, (400, 550))
        #if self.health_loss > 0:
        #    screen.blit(self.health_loss_bar, (int(400*(self.health/self.max_health))+400, 550))#change bounds
        '''mana'''
        screen.blit(self.mana_bar_show, (400, 600))
        screen.blit(self.mana_bar, (400, 600))
        #if self.mana_loss > 0:
        #    screen.blit(self.mana_loss_bar, (int(400*(self.mana/self.max_mana))+400, 700))#change bounds

    def attack(self, screen, dims, walls):

        '''
        Notice:

        since the image rendered on screen has different x, y than the actual player,
        naturally the attack also has a different x, y than the actual player. What needs
        to happen is that we move the rects to the players real x, y and then don't draw.
        For graphics we just have one surface there rendering the animations

        '''
        self.attacks = []
        if self.attack_counter == 0:
                
            if cursor.Lclick and self.cooldown == 0 and cursor.y < 550:
                self.points["angle"] = math.atan2(cursor.y-dims[0]/2, cursor.x-dims[1]/2)
                self.points["chx"], self.points["chy"] = math.cos(self.points["angle"]), math.sin(self.points["angle"])
                self.attack_counter += 1
            
        else:
            self.attacks = self.using.send_attack([self.x, self.y], self.points, dims, walls, screen)
                
            self.attack_counter += 1
            if self.attack_counter >= self.using.duration:
                self.attacks = []
                self.attack_counter = 0
                self.cooldown = self.using.cooldown
        
        if self.cooldown > 0:
            self.cooldown -= 1

    def attack_prototype(self, screen):
        #self.attackbox.x, self.attackbox.y = self.x+20, self.y+10
        #pygame.draw.rect(screen, (0,255,0), self.attackbox)
        pass
        
        

        
player = main_player()

# quick chat(check main for refrance):
# 
