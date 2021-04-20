import math
import pygame

weapon_library = {
    "sword": [10, 20, 50, 15, 15, 1, 7],
    "spear": [15, 25, 50, 15, 15, 4, 2],
    "beam": [10, 50, 50, 30, 15, 30, 1]
}

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
                