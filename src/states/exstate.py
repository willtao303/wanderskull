import pygame

class PlayState():
    def __init__(self):
        self.changeTo = None

    def enter(self):
        #before 1st frame, mainly for initializing things
        print("name: hello")

    def exit(self):
        #before last frame, for saving things and making sure things dont break
        print("play: bye")
        self.changeTo = None

    def update(self, keyspressed, keysdown):
       #for game logic
       pass


    def render(self, screen, h, w):
        #for rendering objects
        pass
 
