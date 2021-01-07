#from player import main_player
import pygame
from src.entities.button import Button

start = Button((500, 50), (1, 1), None)
turn = Button((500,50), (1,1), None)


class StartState():
    def __init__(self):
         self.changeTo = None
         self.string = ""
         self.typebox = pygame.Surface((600, 50))
         self.states = {"start","play","turn","attack","camera"}
         self.notfound = False
         self.font = pygame.font.Font("src/lib/fonts/pixelmix.ttf", 40)

    def enter(self):
        print("start: hello")

        def escape1():
            self.changeTo = "play"
        
        def escape2():
            self.changeTo = "turn"
        
        start.function = escape1
        turn.function = escape2
        print(turn.function)
        
    def exit(self):
        print("start: bye")
        self.changeTo = None
    
    def update(self, keyspressed, keysdown):
        if keyspressed != []:
            pass
        for i in keyspressed:
            if len(pygame.key.name(i)) == 1:
                self.notfound = False
                self.string += pygame.key.name(i)
            if i == pygame.K_RETURN:
                if self.string in self.states:
                    self.changeTo = self.string
                    self.typebox.fill((30,30,40))
                    self.notfound = False
                else:
                    self.notfound = True
                self.string = ""
            if i == pygame.K_BACKSPACE:
                self.string = self.string[0:len(self.string)-1]

        start.update("cool", "hi")
        turn.update()
    
    def render(self, screen, h, w):
        start.pos = (int(w/2), int(h/2)+50)
        turn.pos = (int(w/2), int(h/2)-50)
        screen.blit(self.typebox, (int(w/2) - 300,10))
        if self.notfound:
            screen.blit(self.font.render("no such state found", False, (255,200,200)), (int(w/2) - 275,70))
        self.typebox.fill((30,30,40))
        self.typebox.blit(self.font.render(self.string, False, (255,255,255)), (5,5))
        start.render(screen)
        turn.render(screen)
        
