import src.entities.behaviours.pathfind as pf
import pygame
import random
import math
from src.entities.items.Item import Item, item_library
from src.entities.Attack import Attack, weapon_library

class Enemy():
    def __init__(self, pos: tuple((float, float))):
        #body and position
        self.x = pos[0] * 50
        self.y = pos[1] * 50
        self.sprite = pygame.Surface((50, 50))
        self.sprite.fill((255, 0, 0))
        self.speed = 2
        self.dims = (50, 50)
        self.rect = pygame.Rect((self.x, self.y), self.dims)
        self.color = (255, 0, 0)
        self.moveVectorx = 0
        self.moveVectory = 0
        self.moving = True
        self.enemy_pos = [0, 0]

        #pathfinding
        self.nextpos = (self.x, self.y)
        self.path = []
        self.range = 10+50
        self.foundplayer = False
        self.canGo = {"down":True, "up":True, "left":True, "right":True}

        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 0, 0))

        self.collide = None

        #attacks

        self.knock_back = 0
        self.knock_back_angle = 0
        self.knockback_total = 0
        it = item_library["all"][random.randint(0, len(item_library["all"])-1)]
        self.weapon = Item(it, item_library[it])
        self.attacks = []
        self.cooldown = 0

        #health
        self.health = 100

        #id
        # generate an id from number 1 to 1000000000
        self.id = random.randint(1, 1000000000)

    def startup(self, ppos: tuple((float, float)), room):
        self.path = self.pathfind(ppos,room)
    '''
    def antiwall(self, room):
        if abs(self.nextpos[0]-self.x) > abs(self.nextpos[1]-self.y): # horizontal to next pos
            way = [0,0]
            if self.x < self.nextpos[0]:
                if (int((self.x+25)/50)+1,int(self.y/50)) in room.walls:
                    way[0] = 1
                if (int((self.x+25)/50)+1,int((self.y+50)/50)) in room.walls:
                    way[1] = 1
            else:
                if (int((self.x+25)/50)-1,int(self.y/50)) in room.walls:
                    way[0] = -1
                if (int((self.x+25)/50)-1,int((self.y+50)/50)) in room.walls:
                    way[1] = -1
                
            if way[0] != way[1]:
                if way[0] == 0:
                    self.rect.y -= 1
                else:
                    self.rect.y += 1
            else:
                pass
                
        else:
            way = [0,0]
            if self.y < self.nextpos[0]:
                if (int(self.x/50),int((self.y+25)/50)+1) in room.walls:
                    way[0] = 1
                if (int((self.x+50)/50),int((self.y+25)/50)+1) in room.walls:
                    way[1] = 1
            else:
                if (int(self.x/50),int((self.y+25)/50)-1) in room.walls:
                    way[0] = -1
                if (int((self.x+50)/50),int((self.y+25)/50)-1) in room.walls:
                    way[1] = -1
                
            if way[0] != way[1]:
                if way[0] == 0:
                    self.rect.x -= 1
                else:
                    self.rect.x += 1
    '''
    def pathfind(self, ppos: tuple((float, float)), room):
        """[summary]
        Args:
            ppos (tuple[float, float]): The player's coordinates.
            room (Room): the room i think
        """
        nei = []
        route = {}

        ppos50 = [ppos[0] // 50, ppos[1] // 50]
        x50, y50 = self.x // 50, self.y // 50

        queue = [(ppos50[0], ppos50[1])]
        end = [(x50, y50)]
        num = 1

        if (x50, y50) not in room.graph.keys():
            print("origin not found")
        while ((x50, y50) not in route.keys()) and queue:
            temp = []
            for i in queue:
                route[i] = num
                for j in room.graph[i]:
                    temp.append(j)
            queue = []
            for i in temp:
                if not i in route.keys():
                    queue.append(i)
            num += 1
            #print("finding...\ntemp: ", temp)
        if ((ppos50[0], ppos50[1]) not in route.keys()) or (x50, y50) not in route.keys():
            print("path not found")
            return [(x50, y50)]
        while (ppos50[0], ppos50[1]) not in end:
            m = room.graph[end[-1]]
            for i in m:
                if i in route.keys() and route[i] == route[end[-1]] - 1:
                    end.append(i)
                    break
        for i in end:
            nei.append((i[0]*50 + 25, i[1]*50 + 25))
        return nei

    def goto(self, point): #moves self.speed pixels towards point
        change = [0,0]
        #if self.speed > 5:
        relx, rely = point[0]-self.x-25, point[1]-self.y-25
        angle = math.degrees(-math.atan2(rely, relx))
        if self.knock_back > 0:
            chx, chy = math.cos(self.knock_back_angle)*self.knock_back, math.sin(self.knock_back_angle)*self.knock_back
            self.moveVectorx , self.moveVectory = chx, chy
            self.knock_back -= self.knockback_total * 0.1
        elif 45+weapon_library[self.weapon.name]["range"] < math.sqrt((self.x- self.enemy_pos[0])**2 + (self.y - self.enemy_pos[1])**2):
            self.moveVectorx, self.moveVectory = (int(math.cos(-math.radians(angle))*self.speed), int(math.sin(-math.radians(angle))*self.speed))
        else:
            self.moveVectorx, self.moveVectory = 0, 0
##        else:
##            if self.x+25 <= point[0] and point[0] <= self.x+25:
##                chx = 0
##            elif point[0] > self.x+25:
##                chx = 1
##            elif point[0] < self.x+25:
##                chx = -1
##            if self.y+25 <= point[1] and point[1] <= self.y+25:
##                chy = 0
##            elif point[1] > self.y+25:
##                chy = 1
##            elif point[1] < self.y+25:
##                chy = -1
        if self.collide != None:
            self.canGo["down"] = self.canGo["down"] and self.collide.canGo["down"]
            self.canGo["up"] = self.canGo["up"] and self.collide.canGo["up"]
            self.canGo["left"] = self.canGo["left"] and self.collide.canGo["left"]
            self.canGo["right"] = self.canGo["right"] and self.collide.canGo["right"]
            if self.collide.moving:
                angle = math.atan2(self.y-self.collide.y, self.x-self.collide.x)
                change[0] += math.cos(angle) * self.collide.speed
                change[1] += math.sin(angle) * self.collide.speed

        if (self.canGo["up"] and self.moveVectory  < 0) or (self.canGo["down"] and self.moveVectory  > 0):
            change[1] += self.moveVectory 
        if (self.canGo["left"] and self.moveVectorx < 0) or (self.canGo["right"] and self.moveVectorx > 0):
            change[0] += self.moveVectorx

        if not self.canGo["down"]:
            change[1] = min(0, change[1])
        if not self.canGo["up"]:
            change[1] = max(0, change[1])
        if not self.canGo["left"]:
            change[0] = max(0, change[0])
        if not self.canGo["right"]:
            change[0] = min(0, change[0])

        self.rect.move_ip(tuple(change))
        self.y = self.rect.y
        self.x = self.rect.x
        self.canGo = {"down":True, "up":True, "left":True, "right":True}

    def antiwall(self, room):
        if abs(self.nextpos[0]-self.x-25) > abs(self.nextpos[1]-self.y-25): # horizontal to next pos
            way = [0, 0]
            if self.x < self.nextpos[0]:
                if ((self.x+25) // 50 + 1, self.y // 50) in room.walls:
                    way[0] = 1
                if ((self.x+25) // 50 + 1, (self.y+50) // 50) in room.walls:
                    way[1] = 1
            else: # LEFT QUADRENT
                if ((self.x+25) // 50 - 1, self.y // 50) in room.walls:
                    way[0] = -1
                if ((self.x+25) // 50 - 1, (self.y+50) // 50) in room.walls:
                    way[1] = -1
                
            if way[0] != way[1]:
                if way[0] == 0 and self.canGo["up"]:
                    self.rect.y -= 1
                elif self.canGo["down"]:
                    self.rect.y += 1
            else:
                pass
                
        else:
            way = [0, 0]
            if self.y < self.nextpos[1]:
                if (self.x // 50, (self.y+25) // 50 + 1) in room.walls:
                    way[0] = 1
                if ((self.x+50) // 50, (self.y+25) // 50 + 1) in room.walls:
                    way[1] = 1
            else: #lower
                if (self.x // 50, (self.y+25) // 50 - 1) in room.walls:
                    way[0] = -1
                if ((self.x+50) // 50, (self.y+25) // 50 - 1) in room.walls:
                    way[1] = -1
                
            if way[0] != way[1]:
                if way[0] == 0 and self.canGo["left"]:
                    self.rect.x -= 1
                elif self.canGo["right"]:
                    self.rect.x += 1

    def update(self, room, ppos, player):
        
        self.enemy_pos = [player.x, player.y]
        #check for attacks
        for nxt in player.attacks:
            idx = self.rect.collidelist(nxt.attacks)
            if (not(self.id in nxt.hit)) and idx != -1 and int(self.knock_back) == 0:
                if nxt.stats["mainclass"] == "AOE":
                    self.knock_back_angle = math.atan2(self.rect.y-nxt.attacks[idx].y, self.rect.x-nxt.attacks[idx].x)
                else:
                    self.knock_back_angle = math.atan2(self.rect.y-player.y, self.rect.x-player.x)
                self.knock_back = nxt.stats["knockback"]
                self.knockback_total = nxt.stats["knockback"]
                self.health -= nxt.stats["damage"]
                nxt.hit.add(self.id)

        self.antiwall(room)
        #if the position of the player is less than 50, move
        if not self.foundplayer:
            if pf.distbetween(self.path[-1], ppos) >= 25:
                self.path.append(ppos)
            # MEDIOCRE ISSUE: ENEMY FOLLOWS LIST FOR A FEW SECONDS BEFORE COMPLETELY STOPPING FOR SOME REASON
            # POSSIBLE FIX: ????? 
            if len(self.path):
                self.goto(self.path[0])
                if self.rect.collidepoint(self.path[0]):
                    self.path.pop(0)
                if room.inline(ppos, (self.x + 25, self.y + 25)): 
                    self.foundplayer = True
        elif room.inline(ppos, (self.x + 25, self.y + 25)):
            self.goto(ppos)
            self.path = [ppos]
            self.nextpos = ppos
        else:
            if pf.distbetween(self.path[-1], ppos) >= 25:
                    self.path.append(ppos)
            if not self.rect.collidepoint(self.nextpos):
                self.goto(self.nextpos)
            else:
                if len(self.path) > 1:
                    self.path.pop(0)
                dist = 1
                ind = 0
                for i in range(len(self.path)):
                    if pf.distbetween((self.x, self.y), self.path[i]) / (i+1) < dist:
                        if room.inline((self.x + 25,self.y + 25), self.path[i]):
                            dist = pf.distbetween((self.x, self.y), self.path[i]) / (i+1)
                            ind = i
                self.nextpos = self.path[ind]
                self.path = self.path[ind:]

        test = ppos
        if room.inline(test, (self.x + 25, self.y + 25)):
            self.sprite.fill((0, 255, 0))
        #     self.goto(test)
        else:
            self.sprite.fill((255, 0, 0))

        if self.x == self.rect.x and self.y == self.rect.y:
            if pf.distbetween((self.x,self.y),ppos) > self.range:
                if pf.distbetween((self.x, self.y), self.nextpos) < 3:
                    pass

        #            self.path = self.pathfind(self.nextpos, room) + self.path
        
        #self.x = self.rect.x
        #self.y = self.rect.y

        # attack

    
    def attack(self, screen, room, player, offset):

        if 45+weapon_library[self.weapon.name]["range"] >= math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2) and self.knock_back <= 0:
            if self.cooldown == 0: #move this later
                #do the aiming stuff
                angle = math.atan2(player.y-self.y, player.x-self.x)
                points = {
                    "chx":math.cos(angle), "chy":math.sin(angle), "angle":angle
                }
                #send the attack
                name = self.weapon.name
                if weapon_library[self.weapon.name]["mainclass"] == "AOE":
                    # splash takes in target location as the screen location
                    self.attacks.append(Attack(name, (255, 0, 0), weapon_library[name], points, (player.x, player.y), (self.x, self.y), (600+random.randint(-100, 100), 337+random.randint(-100, 100)), (1200, 675)))
                    #self.attacks.append(Attack(name, (255, 0, 0), weapon_library[name], points, (player.x, player.y), (self.x, self.y), (600, 337), (1200, 675)))
                else:
                    self.attacks.append(Attack(name, (255, 0, 0), weapon_library[name], points, (player.x, player.y), (self.x, self.y), (player.x, player.y), (1200, 675)))
                #cooldown
                self.cooldown = weapon_library[name]["cooldown"] * 3
                #if self.storage.inv[self.storage.mainhand].stored.type == "consumable_weapon":
                #    self.storage.inv[self.storage.mainhand].add_item(-1)
            else:
                self.cooldown -= 1
        
            #update attacks
            #((self.y+25-offset[1])*2, (self.x+25-offset[0])*2)
            for nxt in self.attacks:
                nxt.update((player.x, player.y),(self.x, self.y), room.walls, screen, (675, 1200))
        
            #delete attacks
            removelist = []
            for nxt in self.attacks:
                if nxt.dur <= 0 or nxt.delete or len(nxt.hit) >= nxt.stats["penetration"]:
                    removelist.append(nxt)
                    if nxt.stats["on_end"] != "":
                        self.attacks.append(nxt.on_end((self.x, self.y), (player.x, player.y)))
            for nxt in removelist:
                self.attacks.remove(nxt)
            removelist = []
        
    def render(self, screen, offset, room, player):
        #pygame.draw.rect(screen, self.color, self.rect)
        # draw line between (self.x[0]+25, self.x[1]+25) and ppos
        screen.blit(self.sprite, (self.x-offset[0], self.y-offset[1]))
        for i in self.path:
            screen.blit(self.surf, (i[0]-offset[0], i[1]-offset[1]))
        
        self.attack(screen, room, player, offset)
        