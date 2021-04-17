import pygame
import math
import random as rand
import src.entities.algorithms.pathfind as pf
from src.mouse import cursor


class attacker():
    def __init__(self):
        self.body = pygame.Rect((100, 50), (50, 50))
        self.points = {"chx":0, "chy":0, "angle":0}
        self.attacks = []
        self.attackcounter = 0
        self.cooldown = 0
        self.speed = 3
        self.inventory = [
            {"id":"sword", "attacklen":15, "image":pygame.image.load('src/tests/images/wepons/plat-sword.png'), "range":50},
            {"id":"spear", "attacklen":30, "image":pygame.image.load('src/tests/images/wepons/plat-spear.png'), "range":80},
            {"id":"hammer", "attacklen":40, "image":None,"range":80},
            {"id":"radial", "attacklen":20, "image":pygame.image.load('src/tests/images/wepons/bombs.png'),"range":80}]
        self.slotnumber = 0
        self.itemframe = pygame.image.load('src/tests/images/wepons/select.png')
        self.max_health = 100
        self.health =  100
        self.health_bar = pygame.Surface((400, 30))
        self.health_bar_show = pygame.Surface((400, 30))
        
        self.health_bar.fill((0,255,0))
        self.health_bar_show.fill((255, 0 ,0))

        self.knockback = 0
        self.kbangle = 0

        self.health_loss = 0
        self.health_loss_bar = None

    def firstframe(self):
        self.itemframe = pygame.transform.scale(self.itemframe,(144, 108))

    def update(self, keysdown, enemy_attacks):
        
        ind = self.body.collidelist(enemy_attacks)
        if ind != -1 and not self.knockback:
            self.knockback = 15
            self.kbangle = math.atan2(self.body.y-enemy_attacks[ind].y, self.body.x-enemy_attacks[ind].x)
            self.health -= 5
            self.health_loss = 5
            self.health_loss_bar = pygame.Surface((20, 30))#change bounds
            self.health_bar = pygame.Surface((int(400*(self.health/self.max_health)),30))
            self.health_bar.fill((0, 255, 0))
            self.health_loss_bar.fill((192, 192, 192))
        
        if self.knockback == 0:
            moveVectorx = 0
            moveVectory = 0
            if (keysdown[pygame.K_DOWN] or keysdown[pygame.K_s]):
                moveVectory = self.speed
            if (keysdown[pygame.K_UP] or keysdown[pygame.K_w]):
                moveVectory = -self.speed
            if (keysdown[pygame.K_LEFT] or keysdown[pygame.K_a]):
                moveVectorx = -self.speed
            if (keysdown[pygame.K_RIGHT] or keysdown[pygame.K_d]):
                moveVectorx = self.speed
            self.body.move_ip(moveVectorx, moveVectory)

            if not self.attackcounter:
                self.points["angle"] = math.atan2(cursor.y-self.body.y, cursor.x-self.body.x)
                self.points["chx"], self.points["chy"] = math.cos(self.points["angle"])*self.inventory[self.slotnumber]["range"], math.sin(self.points["angle"])*self.inventory[self.slotnumber]["range"]
                if cursor.Lclick and self.cooldown == 0:
                    self.attackcounter += 1
                self.slotnumber += cursor.scroll
                if self.slotnumber >= len(self.inventory):
                    self.slotnumber = 0
                elif self.slotnumber < 0:
                    self.slotnumber = len(self.inventory)-1

            else:
                self.attacks = []
                if self.inventory[self.slotnumber]["id"] == "sword":
                    perpendicular = math.degrees(self.points["angle"])
                    if perpendicular > 0:
                        perpendicular -= 90
                    else:
                        perpendicular += 90
                    perpendicular = math.radians(perpendicular)
                    spacex, spacey = math.cos(perpendicular)*14, math.sin(perpendicular)*14
                    for i in range(-3, 4):#-3,4
                        self.attacks.append(pygame.Rect((self.body.x+25+self.points["chx"]+(i*spacex), self.body.y+25+self.points["chy"]+(i*spacey)), (10,10)))
                
                elif self.inventory[self.slotnumber]["id"] == "spear":
                    for i in range(1,6):
                        a = int(self.inventory[self.slotnumber]["range"]/5)
                        chx, chy = math.cos(self.points["angle"])*(a*i), math.sin(self.points["angle"])*(a*i)
                        self.attacks.append(pygame.Rect((self.body.x+15+chx, self.body.y+15+chy), (10,10)))
                elif self.inventory[self.slotnumber]["id"] == "hammer":
                    pass
                self.attackcounter += 1
                if self.attackcounter >= self.inventory[self.slotnumber]["attacklen"]:
                    self.attacks = []
                    self.attackcounter = 0
                    self.cooldown = 20
        else:
            chx, chy = math.cos(self.kbangle)*self.knockback, math.sin(self.kbangle)*self.knockback
            self.knockback-=1.5 #sorry, its linear but works
            self.health_loss -= 0.5 #cause knockback is 10 frames
            self.health_loss_bar = pygame.Surface((int(self.health_loss/5* 20),30))#change bounds
            self.health_loss_bar.fill((192, 192, 192))
            self.body.move_ip(chx, chy)

        if self.cooldown > 0:
            self.cooldown -= 1
            

        #if not len(self.attacks):

    def draw(self,screen, h, w):
        pygame.draw.rect(screen, (0, 255, 0), self.body)
        for i in self.attacks:
            pygame.draw.rect(screen, (0, 255, 255), i)
        screen.blit(self.itemframe, (w-self.itemframe.get_width()-5, h-self.itemframe.get_height()-5))
        if self.inventory[self.slotnumber]["image"] != None:
            temp = self.inventory[self.slotnumber]["image"]
            screen.blit(pygame.transform.scale(temp, (temp.get_width()*3,temp.get_height()*3)), (w - int(self.itemframe.get_width()/2)-int(temp.get_width()*1.6), h-self.itemframe.get_height()))
        screen.blit(self.health_bar_show, (400, 550))
        screen.blit(self.health_bar, (400, 550))
        if self.health_loss > 0:
            screen.blit(self.health_loss_bar, (int(400*(self.health/self.max_health))+400, 550))#change bounds
        #self.health_bar_show.blit(self.health_bar, (0,0))

class dumbenemy():
    def __init__(self):
        if rand.randint(0, 1):
            self.rect = pygame.Rect((rand.randint(0, 1210), rand.randint(0, 1)*675),(50,50))
        else:
            self.rect = pygame.Rect((rand.randint(0, 1)*1200, rand.randint(0, 685)),(50,50))
        self.speed = 3
        self.hp = 5
        self.hpbar = pygame.Surface((50,10))
        self.hpshow = pygame.Surface((50,10))
        self.dead = False
        self.collide = None
        self.knockback = 0#knockback speed
        self.kbangle = 0#knockback angle
        self.enemy_attack = []
        self.attack_counter = 0
        self.cooldown = 0
        self.points = {"chx":0, "chy":0, "angle": 0}

    def update(self, player):

        if self.rect.collidelist(player.attacks) != -1 and not self.knockback:
            self.hp -= 1
            self.kbangle = player.points["angle"]# knockback code  - finds hitting angle at exact moment
            #when someone clicks
            self.knockback = 15#knockback speed
        
        if not self.knockback:#if its not being knocked back

            if pf.distbetween((self.rect.x, self.rect.y),(player.body.x, player.body.y)) < 100 and self.cooldown == 0 and self.attack_counter == 0:
                self.attack_counter += 1
                self.points["angle"] = math.atan2(player.body.y-self.rect.y, player.body.x-self.rect.x)
                self.points["chx"] = math.cos(self.points["angle"])*50#20 is the range
                self.points["chy"] = math.sin(self.points["angle"])*50
            elif self.attack_counter > 0:
                self.enemy_attack = []
                perpendicular = math.degrees(self.points["angle"])
                if perpendicular > 0:
                    perpendicular -= 90
                else:
                    perpendicular += 90
                perpendicular = math.radians(perpendicular)
                spacex, spacey = math.cos(perpendicular)*14, math.sin(perpendicular)*14
                for i in range(-3, 4):#-3,4
                    self.enemy_attack.append(pygame.Rect((self.rect.x+25+self.points["chx"]+(i*spacex), self.rect.y+25+self.points["chy"]+(i*spacey)), (10,10)))
                self.attack_counter += 1
                if self.attack_counter > 14: #can change 14
                    self.attack_counter = 0
                    self.cooldown = 100
                    self.enemy_attack = []

            if self.collide != None:
                angle = math.atan2(self.rect.y-self.collide.rect.y, self.rect.x-self.collide.rect.x)
                chx, chy = math.cos(angle)*2, math.sin(angle)*2
                self.rect.move_ip(chx, chy)
            if not(math.sqrt((self.rect.x-player.body.x)**2 + (self.rect.y-player.body.y)**2) <= 70):
                angle = math.atan2(player.body.y-self.rect.y, player.body.x-self.rect.x)
                chx, chy = math.cos(angle)*self.speed, math.sin(angle)*self.speed
                self.rect.move_ip(int(chx), int(chy))
        else:
            chx, chy = math.cos(self.kbangle)*self.knockback, math.sin(self.kbangle)*self.knockback
            self.knockback-=1.5 #sorry, its linear but works
            self.rect.move_ip(chx, chy)

        if self.hp <= 0:
            self.dead = True

        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        for i in self.enemy_attack:
            pygame.draw.rect(screen, (0, 0, 255), i)
        screen.blit(self.hpbar,(self.rect.x, self.rect.y-15))
        self.hpbar.fill((255,255,255))
        self.hpshow = pygame.Surface((self.hp*10,10))
        self.hpshow.fill((200,0,0))
        self.hpbar.blit(self.hpshow, (0,0))
        

class AttackState():
    def __init__(self):
        self.changeTo = None
        self.attacker = attacker()
        self.enemies = []
        self.enemiesattacked = []#stores enemy attacks
        self.spawntimer = 0

    def enter(self):
        self.attacker.firstframe()
        print("name: hello")

    def exit(self):
        #before last frame, for saving things and making sure things dont break
        print("play: bye")
        self.changeTo = None

    def update(self, keyspressed, keysdown):
        if keyspressed != []:
            if pygame.K_ESCAPE in keyspressed:
                self.changeTo = "start"
            if pygame.K_SPACE in keyspressed:
                self.enemies.append(dumbenemy())
            if pygame.K_RETURN in keyspressed:
                self.enemies = []

        self.attacker.update(keysdown, self.enemiesattacked)

        for i in self.enemies:
            i.collide = None
            for j in self.enemies:
                if i != j:
                    if i.rect.colliderect(j.rect):
                        i.collide = j
                        break
        
        self.enemiesattacked = []
        for i in range(0, len(self.enemies))[::-1]:
            if not self.enemies[i].dead:
                self.enemies[i].update(self.attacker)
                self.enemiesattacked = self.enemiesattacked + self.enemies[i].enemy_attack
            else:
                self.enemies.pop(i)

        if self.spawntimer <= 0:
            self.enemies.append(dumbenemy())
            self.spawntimer = rand.randint(360, 400)#180, 200
        self.spawntimer -= 1

    def render(self, screen, h, w):
        #for rendering objects
        #if not len(self.enemies):
        for i in self.enemies:
            i.draw(screen)
        self.attacker.draw(screen, h, w)
        