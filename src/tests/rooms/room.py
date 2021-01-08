#import roomtypes
import src.entities.algorithms.pathfind as pf
import random as rand
import math
import pygame

class Room():
    def __init__(self, pos, wallist, doorlist, startpoint):
        self.w, self.h = pos
        self.graph = dict()
        self.staticwalls = wallist
        self.doors = doorlist
        self.doorsclosed = False
        self.spx, self.spy = startpoint
        # INITIALIZES THE DICT OF DISTANCES

        for i in range(self.spx, self.w):
            #print(i)
            if not (self.spy,i) in self.doors:
                self.staticwalls.append((self.spy,i))
            if not (self.h,i) in self.doors:
                self.staticwalls.append((self.h,i))
        for i in range(self.spy, self.h):
            if not (i,self.spx) in self.doors:
                self.staticwalls.append((i,self.spx))
            if not (i,self.w) in self.doors:
                self.staticwalls.append((i,self.w))
                
        self.walls = self.staticwalls + self.doors
        #the graph has to be converted to from a grid first
        for i in range(self.spy,self.h):
            for j in range(self.spy,self.w):
                if not (i,j) in self.walls:
                    self.graph[(i,j)] = []
        for i in self.graph.keys():
            for j in [(1, 1), (-1, -1), (0, 1), (1, 0), (-1, 0), (0, -1), (-1, 1), (1, -1)]:
                new = (i[0]+j[0], i[1]+j[1])
                if new in self.graph.keys():
                    self.graph[i].append(new)

    def update(self):
        if self.doorsclosed:
            self.walls = self.staticwalls + self.doors
        else:
            self.walls = self.staticwalls 

    def roomcollision(self, entity):
        lw = int((entity.x+1)/50)
        uw = int((entity.y+1)/50)
        rw = int((entity.x+49)/50)
        dw = int((entity.y+49)/50)

        if (lw+1,uw) in self.walls or (lw+1,dw) in self.walls:
            entity.canGo["right"] = False
        if (rw-1,dw) in self.walls or (rw-1, uw) in self.walls:
            entity.canGo["left"] = False
        if (lw,uw+1) in self.walls or (rw,uw+1) in self.walls:
            entity.canGo["down"] = False
        if (rw,dw-1) in self.walls or (lw,dw-1) in self.walls:
            entity.canGo["up"] = False
        
    def autocorrections(self, entity):
        # top left, top right, bottom left, bottom right
        corners = [0,0,0,0]
        if(int((entity.x)/50), int((entity.y)/50)) in self.walls:
            corners[0] = 1
        if(int((entity.x+49)/50), int((entity.y)/50)) in self.walls:
            corners[1] = 1
        if(int((entity.x)/50), int((entity.y+49)/50)) in self.walls:
            corners[2] = 1
        if(int((entity.x+49)/50), int((entity.y+49)/50)) in self.walls:
            corners[3] = 1
        
        if corners != [0,0,0,0]:
            if sum(corners) == 3:
                entity.box.x = int((entity.x+25)/50)*50 
                entity.box.y = int((entity.y+25)/50)*50
            elif (corners == [1,1,0,0]) or (corners == [0,0,1,1]):
                entity.box.y = int((entity.y+25)/50)*50
            elif (corners == [1,0,1,0]) or (corners == [0,1,0,1]):
                entity.box.x = int((entity.x+25)/50)*50
            elif sum(corners) == 1:
                # possibly do if only 1 key is pressed do opposite of the key direction
                if rand.randint(0,1):
                    entity.box.x = int((entity.x+25)/50)*50
                else:
                    entity.box.y = int((entity.y+25)/50)*50
                
    
    def render(self, screen, offset, render): # render = [left wall, right wall, top wall, bottom wall] or [0, width, 0 height]
        for i in self.staticwalls:
            #if render[0] < i[0]*50+offset[0] and i[0]*50+offset[0] < render[1]:
                #if render[2] < i[1]*50-offset[1] and i[1]*50-offset[1] < render[3]:
            pygame.draw.rect(screen, (120, 160, 160), pygame.Rect((i[0]*50 - offset[0], i[1]*50 - offset[1]),(50,50)))
        if self.doorsclosed:
            for i in self.doors:
                pygame.draw.rect(screen, (160,82,45), pygame.Rect((i[0]*50 - offset[0], i[1]*50 - offset[1]),(50,50)))

    def inline(self, spos, epos):
        l = set()
        n = 1
        relx, rely = epos[0]-spos[0]-25, epos[1]-spos[1]-25
        angle = math.degrees(-math.atan2(rely, relx))
        chx, chy = (int(math.cos(-math.radians(angle))*25), int(math.sin(-math.radians(angle))*25))
        while math.sqrt((spos[0]-epos[0])**2 + (spos[1]-epos[1])**2) > n*25:
            l.add((int((spos[0]+n*chx)/50),int((spos[1]+n*chy)/50)))
            n+=1
        return l.isdisjoint(set(self.walls))

    # for error checking
    def printwithplayer(self, player):
        lw = int((player.x-10)/50)
        uw = int((player.y-10)/50)
        rw= int((player.x+10)/50)
        dw = int((player.y+10)/50)
        finalmessage = []
        for y in range(self.h):
            msg = []
            for x in range(self.w):
                if y == uw and x == lw:
                    msg.append('P')
                elif y == dw and x == rw:
                    msg.append('N')
                else:
                    if (x,y) in self.walls:
                        msg.append("1")
                    else:
                        msg.append("0")
                    #msg.append(str(self.map[y][x]))
            finalmessage.append("".join(msg))
        return "\n".join(finalmessage)


    def toString(self):
        pass




class fullmap():
    def generatemap(rooms):
        pass
    
