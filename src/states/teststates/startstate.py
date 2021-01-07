#from player import main_player
import pygame
from src.entities.button import Button

class StartState():
    def __init__(self):
         self.changeTo = None

    def enter(self):
        print("start: hello")

        def escape1():
            self.changeTo = "play"
        
        def escape2():
            self.changeTo = "turn"
        
    def exit(self):
        print("start: bye")
        self.changeTo = None
    
    def update(self, keyspressed, keysdown):
        if keyspressed != []:
            if keyspressed[pygame.K_a]:
                self.changeTo = "attack"
    
    def render(self,screen, h, w):
