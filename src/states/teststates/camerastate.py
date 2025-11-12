from src.world.room import Room
from src.mouse import cursor
import pygame


room = Room.from_str("")

class CameraState():
    def __init__(self):
        self.changeTo = None
        self.offset = [0, 0]
        self.mouseoffset = [0, 0]
        self.speed = 4
    def enter(self):
        #before 1st frame, mainly for initializing things
        print("enter state: camera")

    def exit(self):
        #before last frame, for saving things and making sure things dont break
        print("exit state: camera")
        self.changeTo = None

    def update(self, keyspressed, keysdown):
       #for game logic
        if keysdown[pygame.K_DOWN] or keysdown[pygame.K_s]:
            self.offset[1] -= self.speed
        if keysdown[pygame.K_UP] or keysdown[pygame.K_w]:
            self.offset[1] += self.speed
        if keysdown[pygame.K_LEFT] or keysdown[pygame.K_a]:
            self.offset[0] += self.speed
        if keysdown[pygame.K_RIGHT] or keysdown[pygame.K_d]:
            self.offset[0] -= self.speed
        if keyspressed != None:
            if pygame.K_ESCAPE in keyspressed:
                self.changeTo = "start"

        
    def render(self, screen, h, w):
        self.mouseoffset[0] = -int((cursor.x - (w // 2)) // w * 50)
        self.mouseoffset[1] = -int((cursor.y - (h // 2)) // h * 50)
        room.render(screen, (self.offset[0]+self.mouseoffset[0],self.offset[1]+self.mouseoffset[1]), (-70, w+70, -70, h+70))
 
