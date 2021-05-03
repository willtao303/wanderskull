import pygame
from src.mouse import cursor
import src.statemachine as statemachine


pygame.init()

screen_width = 1200  # 1000 for now
screen_height = 675  # 600

gameDisplay = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("WanderSkull")  # lmao change or keep?  ¯\_(ツ)_/¯ YEA!


clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

running = True
keyspressed = []
state = statemachine.StateMachine()
scroll = 0
# h, w = screen_height, screen_width

# main loop
while running:
    keyspressed = []
    scroll = 0
    for event in pygame.event.get(): 
        # print(event)
        if event.type == pygame.QUIT:
            running = False
            break  
        elif event.type == pygame.VIDEORESIZE:
            # h, w = event.h, event.w
            screen_height, screen_width = event.h, event.w
            gameDisplay.fill((20, 20, 20))
        elif event.type == pygame.KEYDOWN:
            keyspressed.append(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll = -1
            elif event.button == 5:
                scroll = 1

    keysdown = pygame.key.get_pressed()

    cursor.update(scroll)
    state.update(keyspressed, keysdown)
    gameDisplay.fill((20, 20, 20))
    state.render(gameDisplay, screen_height, screen_width)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# Quick chat: (Each collaborator can only have one message at a time)
# this is just for leaving messages behind since not
# everybody is gonna be on the chat at the same time