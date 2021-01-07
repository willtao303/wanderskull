import pygame

class IntroState():
    def __init__(self):
        self.changeTo = None

    def enter(self):
        print("intro: hello")

    def exit(self):
        print("intro: bye")
        self.changeTo = None

    def update(self, keyspressed, keysdown):
        pass


    def render(self, screen, h, w):
        pass
 
