import math
import pygame

#range of a ranged weapon is duration * speed
weapon_library = {
    "sword": {"reach":1, "width":7, "duration":10, "range":28, "mainclass":"sword", "cooldown":40, "damage":15, "knockback":15, "h":10, "w":10, "penetration":999, "on_end":""},
    "spear": {"reach":4, "width":2, "duration":15, "range":70, "mainclass":"sword", "cooldown":60, "damage":20, "knockback":20, "h":10, "w":10, "penetration":999, "on_end":""},
    "bow": {"reach":1, "width":1, "duration":50, "speed":10, "range":500, "mainclass":"range", "cooldown":80, "damage":20, "knockback":25, "h":10, "w":10, "penetration":1,"on_end":""},
    "staff": {"reach":1, "width":1, "duration":20, "range":350, "mainclass":"AOE", "cooldown":100, "damage":20, "knockback":10, "h":80, "w":80, "penetration":999, "on_end":""},
    "small_explosion": {"reach":1, "width":1, "duration":25, "range":-1, "mainclass":"AOE", "cooldown":120, "damage":30, "knockback":25, "h":100, "w":100, "penetration":999, "on_end":""},
    "bomb": {"reach":1, "width":1, "duration":30, "speed":7, "range":210, "mainclass":"range", "cooldown":120, "damage":10, "knockback":10, "h":25, "w":25, "penetration":1,"on_end":"small_explosion"}
}


class Attack():

    def __init__(self, name, colour, stats, points, pxy, xy, cxy, dims):
        # what enemies have been hit
        self.hit = set()
        self.name = name
        self.colour = colour
        self.stats = stats
        self.points = points
        self.xystart = xy
        self.cxystart = cxy
        self.playerxy = pxy
        self.dims = dims
        if self.stats["mainclass"] == "AOE":
            self.show = [pygame.Rect((self.cxystart[0]-5, self.cxystart[1]-5), (10, 10)) for _ in range(self.stats["reach"]*self.stats["width"])]
            self.attacks = [pygame.Rect((cxy[0]+pxy[0]-dims[1]/2+20, cxy[1]+pxy[1]-dims[0]/2+20), (10, 10)) for _ in range(self.stats["reach"]*self.stats["width"])]
        else:
            self.attacks = [pygame.Rect((xy[0]+25, xy[1]+25), (self.stats["h"], self.stats["w"])) for _ in range(self.stats["reach"]*self.stats["width"])]
            #remove when animation comes
            self.show = [pygame.Rect((xy[0]+25, xy[1]+25), (self.stats["h"], self.stats["w"])) for _ in range(self.stats["reach"]*self.stats["width"])]
        self.dur = self.stats["duration"]

        #do space thing
        perpendicular = math.degrees(self.points["angle"])
        if perpendicular > 0:
            perpendicular -= 90
        else:
            perpendicular += 90
        perpendicular = math.radians(perpendicular)
        self.space = [math.cos(perpendicular)*14, math.sin(perpendicular)*14]

        #need delete?
        self.delete = False
    

    def on_end(self, xy, pxy):
        if self.stats["on_end"] != "":
            newx, newy = self.attacks[0].x+self.dims[1]//2-self.xystart[0], self.attacks[0].y+self.dims[0]//2-self.xystart[1]
            return Attack(self.stats["on_end"], self.colour, weapon_library[self.stats["on_end"]], self.points, pxy, (xy[0], xy[1]), (self.show[0].x, self.show[0].y), self.dims)
    

    def splash(self, pxy, xy, screen):
        offset = pxy[0]-self.playerxy[0], pxy[1]-self.playerxy[1]
        if self.show[0].height < self.stats["h"]:
            self.show[0].inflate_ip((10, 10))
            self.attacks[0].inflate_ip((10, 10))
        self.attacks[0].x, self.attacks[0].y = self.cxystart[0]+self.playerxy[0]-600+25-self.attacks[0].height/2, self.cxystart[1]+self.playerxy[1]-337+25-self.attacks[0].height/2
        self.show[0].x, self.show[0].y = self.cxystart[0]-self.show[0].height/2-offset[0], self.cxystart[1]-self.show[0].height/2-offset[1]
        pygame.draw.rect(screen, self.colour, self.show[0])
        #pygame.draw.rect(screen, (0, 255, 255), self.attacks[0])
    

    def ranged_strike(self, pxy, xy, walls, screen):
        offset = (pxy[0]-self.dims[1]/2, pxy[1]-self.dims[0]/2)
        for i in range(len(self.attacks)):
            self.attacks[i].x += self.points["chx"] * self.stats["speed"]
            self.attacks[i].y += self.points["chy"] * self.stats["speed"]
            self.show[i].x = self.points["chx"] * self.stats["speed"] * (self.stats["duration"] - self.dur) + self.xystart[0]-offset[0]#self.xystart[0] #- (xy[0]+25-dims[0]//2)
            self.show[i].y = self.points["chy"] * self.stats["speed"] * (self.stats["duration"] - self.dur) + self.xystart[1]-offset[1]#self.xystart[1] #- (xy[1]+25-dims[1]//2)
            pygame.draw.rect(screen, self.colour, self.show[i])
            #pygame.draw.rect(screen, (0, 255, 255), self.attacks[i])

            if ((self.attacks[i].x//50, self.attacks[i].y//50) in walls):
                self.delete = True 

    
    def sword_strike(self, pxy, xy, walls, screen):
        offset = (xy[0]- pxy[0]+self.dims[1]/2, xy[1]- pxy[1]+self.dims[0]/2)
        # the 14 is the space between the smaller blocks
        col = [True for i in range(self.stats["width"])]
        #whether that column has a wall blocking the way
        for j in range(self.stats["reach"]):
            for i in range(-(self.stats["width"]//2), self.stats["width"]//2+self.stats["width"]%2):#-3,4
                x_val = xy[0]+25+self.points["chx"]*(40+j*14)+(i*self.space[0])
                y_val = xy[1]+25+self.points["chy"]*(40+j*14)+(i*self.space[1])
                #chy * (self.range+j*14) -> the latter block denotes the range
                if not ((int((x_val+1)/50), int((y_val+1)/50)) in walls or (int((x_val+9)/50), int((y_val+9)/50)) in walls) and col[i+self.stats["width"]//2]:
                    self.attacks[j*self.stats["width"]+i].x, self.attacks[j*self.stats["width"]+i].y = x_val, y_val
                    self.show[j*self.stats["width"]+i].x, self.show[j*self.stats["width"]+i].y = offset[0]+self.points["chx"]*(40+j*14)+(i*self.space[0]), offset[1]+self.points["chy"]*(40+j*14)+(i*self.space[1])
                    pygame.draw.rect(screen, self.colour, self.show[j*self.stats["width"]+i])
                    #pygame.draw.rect(screen, (0, 255, 255), self.attacks[j*self.stats["width"]+i])
                else:
                    col[i+self.stats["width"]//2] = False


    def update(self, pxy, xy, walls, screen, dims):
        self.dims = dims
        self.dur -= 1
        if self.stats["mainclass"] == "sword" or self.stats["mainclass"] == "spear":
            #self.ranged_strike(xy, walls, screen)
            self.sword_strike(pxy, xy, walls, screen)
        elif self.stats["mainclass"] == "range":
            self.ranged_strike(pxy, xy, walls, screen)
        elif self.stats["mainclass"] == "AOE":
            self.splash(pxy, xy, screen)

'''
class Weapon():

    def __init__(self, name, type):
        self.name = name #name
        self.damage = type[0] #damage
        self.cooldown = type[1] #cooldown
        self.range = type[2] #range
        self.duration = type[3] #duration of attack
        self.knockback = type[4] # knockback - 10% repeat until 0
        self.length = type[5] 
        self.width = type[6]
    
    def send_attack(self, xy, points, dims, walls, screen):

        perpendicular = math.degrees(points["angle"])
        if perpendicular > 0:
            perpendicular -= 90
        else:
            perpendicular += 90
        perpendicular = math.radians(perpendicular)
        spacex, spacey = math.cos(perpendicular)*14, math.sin(perpendicular)*14
        # the 14 is the space between the smaller blocks

        vals = []
        col = [True for i in range(self.width)]
        #whether that column has a wall blocking the way
        for j in range(self.length):
            for i in range(-(self.width//2), self.width//2+self.width%2):#-3,4
                x_val = xy[0]+25+points["chx"]*(self.range+j*14)+(i*spacex)
                y_val = xy[1]+25+points["chy"]*(self.range+j*14)+(i*spacey)
                #chy * (self.range+j*14) -> the latter block denotes the range
                if not ((int((x_val+1)/50), int((y_val+1)/50)) in walls or (int((x_val+9)/50), int((y_val+9)/50)) in walls) and col[i+self.width//2]:
                    vals.append(pygame.Rect((x_val, y_val), (10,10)))
                    pygame.draw.rect(screen, (0, 255, 255), pygame.Rect((dims[1]/2+points["chx"]*(self.range+j*14)+(i*spacex), dims[0]/2+points["chy"]*(self.range+j*14)+(i*spacey)), (10,10)))
                else:
                    col[i+self.width//2] = False
        return vals
'''
