import src.entities.algorithms.pathfind as pf
import pygame
import math

class Enemy():
    def __init__(self, pos:tuple):
        #body and position
        self.x = pos[0]*50
        self.y = pos[1]*50
        self.sprite = pygame.Surface((50,50))
        self.sprite.fill((255,0,0))
        self.speed = 2
        self.dims = (50,50)
        self.rect = pygame.Rect((self.x, self.y), self.dims)
        self.color = (255, 0, 0)

        #pathfinding
        self.nextpos = (self.x, self.y)
        self.path = []
        self.range = 10+50
        self.foundplayer = False
        self.canGo = {"down":True, "up":True, "left":True, "right":True}

        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,0,0))
    def startup(self, ppos, room):
        self.path = []
        print("enemy starting up")
        route = {}
        queue = [(int(ppos[0]/50),int(ppos[1]/50))]
        end = [(int(self.x/50),int(self.y/50))]
        print(end)
        num = 1
        while not((int(self.x/50),int(self.y/50)) in route.keys()) and len(queue)!=0:
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
        print("step 1 complete")
        if not((int(ppos[0]/50),int(ppos[1]/50)) in route.keys()) or not((int(self.x/50),int(self.y/50))) in route.keys():
            print("path not found")
            return [((int(self.x/50),int(self.y/50)))]
        print("step 2 initiating...")
        while not((int(ppos[0]/50),int(ppos[1]/50)) in end):
            print("tracing...")
            m = room.graph[end[-1]]
            for i in m:
                if route[i] == route[end[-1]] - 1:
                    end.append(i)
                    break
        print("traced\npath found")
        for i in end:
            self.path.append((i[0]*50, i[1]*50))
        print(self.path)

    def goto(self, point): #moves self.speed pixels towards point
        change = [0,0]
        #if self.speed > 5:
        relx, rely = point[0]-self.x-25, point[1]-self.y-25
        angle = math.degrees(-math.atan2(rely, relx))
        chx, chy = (int(math.cos(-math.radians(angle))*self.speed), int(math.sin(-math.radians(angle))*self.speed))
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

        if (self.canGo["up"] and chy < 0) or (self.canGo["down"] and chy > 0):
            change[1] = chy
        if (self.canGo["left"] and chx < 0) or (self.canGo["right"] and chx > 0):
            change[0] = chx
        self.rect.move_ip(tuple(change))
        self.canGo = {"down":True, "up":True, "left":True, "right":True}

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


    def update(self, room, ppos):
        self.antiwall(room)
        if not self.foundplayer:
            # MEDIOCRE ISSUE: ENEMY FOLLOWS LIST FOR A FEW SECONDS BEFORE COMPLETELY STOPPING FOR SOME REASON
            # POSSIBLE FIX: ????? 
            if len(self.path):
                self.goto(self.path[0])
                if self.rect.collidepoint(self.path[0]):
                    print("n")
                    self.path.pop(0)
                if room.inline(ppos, (self.x+25,self.y+25)):
                    self.foundplayer = True
        elif room.inline(ppos, (self.x+25,self.y+25)):
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
                    if pf.distbetween((self.x,self.y),self.path[i])/(i+1) < dist:
                        if room.inline((self.x+25,self.y+25),self.path[i]):
                            dist = pf.distbetween((self.x,self.y),self.path[i])/(i+1)
                            ind = i
                self.nextpos = self.path[ind]
                self.path = self.path[ind:len(self.path)]

        test = pygame.mouse.get_pos()
        if room.inline(test, (self.x+25,self.y+25)):
            self.color = (0,255,0)
        #     self.goto(test)
        else:
            self.color = (255,0,0)

        self.x = self.rect.x
        self.y = self.rect.y
        
    def render(self, screen, offset):
        #pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.sprite, (self.x-offset[0], self.y-offset[1]))
        for i in self.path:
            screen.blit(self.surf, (i[0]-offset[0], i[1]-offset[1]))
        