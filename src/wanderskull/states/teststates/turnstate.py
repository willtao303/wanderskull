# from player import main_player
import math

import pygame

from ...const import asset_folder
from ...mouse import cursor

# from wanderskull.mouse import cursor


class TurnState:
    def __init__(self):
        self.changeTo = None

        self.x, self.y = 300, 300
        self.surf = pygame.image.load(asset_folder + "images/temp/sample image.png")
        self.angle = 0.0
        self.attack = False

    def enter(self):
        print("turn: hello")

    def exit(self):
        print("turn: bye")
        self.changeTo = None

    def update(self, keyspressed, keysdown):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.changeTo = "start"

        if not self.attack:
            mousex, mousey = pygame.mouse.get_pos()
            relx, rely = mousex - self.x, mousey - self.y
            self.angle = math.degrees(-math.atan2(rely, relx))

            # if cursor.Rclick:
            #     self.attack = True
            self.attack = cursor.Rclick
        else:
            # chx, chy = math.cos(-math.radians(self.angle))*5, math.sin(-math.radians(self.angle))*5
            radians = math.radians(self.angle)

            self.x += int(math.cos(-radians) * 5)
            self.y += int(math.sin(-radians) * 5)

    def render(self, screen, h, w):
        a = pygame.transform.flip(self.surf, False, True) if abs(self.angle) > 90 else self.surf

        a = pygame.transform.rotate(a, self.angle)

        # draw self.surface to screen
        screen.blit(a, (int(self.x - (a.get_width() / 2)), int(self.y - (a.get_height() / 2))))

        if self.x < 0 or self.x > w or self.y < 0 or self.y > h:
            self.x, self.y = 300, 300
            self.attack = False
