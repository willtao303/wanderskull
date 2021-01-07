import pygame
from src.mouse import cursor
import src.statemachine as statemachine

pygame.init()

screen_width = 1200 #1000 #for now
screen_height = 675 #600

gameDisplay = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)
pygame.display.set_caption("WanderSkull")#lmao change or keep?  ¯\_(ツ)_/¯


clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
#main loop
running = True
keyspressed = []
state = statemachine.StateMachine()
scroll = 0
h,w = screen_height, screen_width
while running:
    keyspressed = []
    scroll = 0
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            h, w = event.h, event.w
            gameDisplay.fill(pygame.Color(20,20,20))
        if event.type == pygame.KEYDOWN:
            keyspressed.append(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll = -1
            elif event.button == 5:
                scroll = 1


    keysdown = pygame.key.get_pressed()

    cursor.update(scroll)
    state.update(keyspressed, keysdown)
    gameDisplay.fill(pygame.Color(20,20,20))
    state.render(gameDisplay, h, w)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# Quick chat: (Each collaborator can only have one message at a time)
# this is just for leaving messages behind since not 
# everybody is gonna be on the chat at the same time
#
