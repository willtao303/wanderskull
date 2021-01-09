from src.entities.player import player
import src.entities.algorithms.pathfind as pf
#from src.entities.testenemy import enemy
from src.entities.testenemymedium import Enemy
from src.tests.rooms.room import Room
from src.mouse import cursor
import pygame

#roomlist = [Room((12, 12*(i+1)),[],[(12*(i+1), 4),(12*(i+1), 5), (12*(i+1), 6),(12*(i+1), 7),(12*(i+1), 8),(12*i, 4), (12*i, 5), (12*i, 6),(12*i, 7),(12*i, 8)], (0, max(i*12, 0))) for i in range(25)]
roomlist = [
    Room((12,12), [(3,3),(3,4),(4,3),(4,4),(6,10),(7,10),(8,10),(9,10),(10,10),(10,9), (10,8),(10,7), (10,6)], [(5,12),(6,12)], (0,0)),
    Room((12,24), [], [(5,12),(6,12)], (0,12))
    ]

class PlayState():
    def __init__(self):
        self.changeTo = None
        self.paused = False
        self.enemy = Enemy((1,1))
        self.active = 0
        self.acts = (roomlist[0].spx, roomlist[0].spy)
        self.acte = acte = (roomlist[0].w, roomlist[0].h)

    def enter(self):
        player.firstframe()
        print("play: hello")
        self.enemy.startup((player.x, player.y), roomlist[self.active])

    def exit(self):
        print("play: bye")
        self.changeTo = None

    def update(self, keyspressed, keysdown):
        if keyspressed != None:
            if pygame.K_f in keyspressed:
                roomlist[self.active].doorsclosed = not roomlist[self.active].doorsclosed
            if pygame.K_SPACE in keyspressed:
                self.paused = not self.paused
            if pygame.K_h in keyspressed:
                print(Room.printwithplayer(roomlist[self.active], player))
            if pygame.K_ESCAPE in keyspressed:
                self.changeTo = "start"
        
        if self.paused:
            pass
        else:
            #remember that this only works if the rooms only go from left to right
            #print(self.active)
            if self.acte[1] <= int(player.x/50) and self.active < len(roomlist)-1:
                self.active += 1
                self.acts = (roomlist[self.active].spx, roomlist[self.active].spy)
                self.acte = (roomlist[self.active].w, roomlist[self.active].h)
            elif self.acts[1] > int(player.x/50) and self.active > 0:
                self.active -= 1
                self.acts = (roomlist[self.active].spx, roomlist[self.active].spy)
                self.acte = (roomlist[self.active].w, roomlist[self.active].h)

            roomlist[self.active].update()
            roomlist[self.active].roomcollision(self.enemy)
            self.enemy.update(roomlist[self.active], (player.x+24, player.y+24))
            player.update()

        roomlist[self.active].roomcollision(player)

    def minimap_builder(self, screen, enemies, wall):
        square = pygame.Surface((5,5)) #player point
        square.fill((0,255,255))
        screen.blit(square, (1075, 75))
        #find enemy - wall coord relation to player
        
        square.fill((255, 0, 0))
        for coord in enemies:
            if abs(((coord[0]+25)//50 - player.x//50)) + abs(((coord[1]+25)//50 - player.y//50)) <= 14:
                screen.blit(square, (1075+5*((coord[0]+25)//50 - player.x//50), 75+5*((coord[1]+25)//50 - player.y//50)))
        
        square.fill((150, 150, 150))
        for coord in wall:
            if pf.distbetween(coord, (player.x//50,player.y//50)) < 14:
                screen.blit(square, (1075+5*(coord[0] - player.x//50), 75+5*(coord[1] - player.y//50)))
        
    
    def render(self, screen, h, w):
        offset = (player.x+25-w/2-cursor.mouseoffset[0], player.y+25-h/2-cursor.mouseoffset[1])

        pygame.draw.line(screen, (0,255,0), ((self.enemy.x+24-offset[0]), (self.enemy.y+24-offset[1])), ((w/2+cursor.mouseoffset[0]), (h/2+cursor.mouseoffset[1])))
        pygame.draw.line(screen, (0,255,255), ((self.enemy.x-offset[0]), (self.enemy.y-offset[1])), ((w/2+cursor.mouseoffset[0]), (h/2+cursor.mouseoffset[1])))
        if not self.paused:
            roomlist[self.active].autocorrections(player)
            player.render(screen, (h,w))
            self.enemy.render(screen, offset)

            for i in range(max(0, self.active-1), min(self.active+2, len(roomlist))):
                roomlist[i].render(screen, offset, (-20, w+20, -20, h+20))

            mini_map_walls = roomlist[self.active].walls
            if self.active > 0:
                mini_map_walls = mini_map_walls + roomlist[self.active-1].staticwalls#cause only one room's doors will closed at a time
            if self.active < len(roomlist)-1:
                mini_map_walls = mini_map_walls + roomlist[self.active+1].staticwalls
            self.minimap_builder(screen,[(self.enemy.x, self.enemy.y)], mini_map_walls)

 
