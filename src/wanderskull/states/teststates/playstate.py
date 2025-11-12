import random

import pygame

import wanderskull.entities.behaviours.pathfind as pf
from wanderskull.entities.Attack import weapon_library

# from wanderskull.entities.testenemy import enemy
from wanderskull.entities.enemies.testenemymedium import Enemy
from wanderskull.entities.items.Item import Item, item_library
from wanderskull.entities.player import main_player, player
from wanderskull.mouse import cursor
from wanderskull.sandbox.rooms.room import Room

roomlist = [
    Room(
        (12, 12 * (i + 1)),
        [],
        [
            (12 * (i + 1), 4),
            (12 * (i + 1), 5),
            (12 * (i + 1), 6),
            (12 * (i + 1), 7),
            (12 * (i + 1), 8),
            (12 * i, 4),
            (12 * i, 5),
            (12 * i, 6),
            (12 * i, 7),
            (12 * i, 8),
        ],
        (0, max(i * 12, 0)),
    )
    for i in range(25)
]
# roomlist = [
#    Room((12,12), [(3,3),(3,4),(4,3),(4,4),(6,10),(7,10),(8,10),(9,10),(10,10),(10,9), (10,8),(10,7), (10,6)], [(5,12),(6,12)], (0,0)),
#    Room((12,24), [], [(5,12),(6,12)], (0,12))
#    ]


class PlayState:
    def __init__(self):
        self.changeTo = None
        self.paused = False
        self.enemies = [Enemy((5, 5)) for _ in range(10)]  # [Enemy((1,1)), Enemy((2,2)), Enemy((3, 3))]
        self.enemy_pos = [(1, 1), (2, 2)]  # useless right now
        self.active = 0
        self.acts = (roomlist[0].spx, roomlist[0].spy)
        self.acte = (roomlist[0].w, roomlist[0].h)

        self.drops = []

    def enter(self):
        player.firstframe()
        print("play: hello")
        for nxt in self.enemies:
            nxt.startup((player.x, player.y), roomlist[self.active])
        player.storage.auto_fill(Item("staff", item_library["staff"]))

    def exit(self):
        print("play: bye")
        self.changeTo = None

    def update(self, keyspressed, keysdown):  # noqa: C901
        if keyspressed is not None:
            if pygame.K_f in keyspressed:
                roomlist[self.active].doorsclosed = not roomlist[self.active].doorsclosed
            if pygame.K_SPACE in keyspressed:
                self.paused = not self.paused
            if pygame.K_h in keyspressed:
                print(Room.printwithplayer(roomlist[self.active], player))
            if pygame.K_ESCAPE in keyspressed:
                self.changeTo = "start"

        """
        ----------------- Player Clicking ------------------
        """

        # inventory - using screen height and width
        if cursor.Lclick and 1070 <= cursor.x <= 1190 and 580 <= cursor.y <= 670 and (not player.storage.clicking):
            player.storage.status = not player.storage.status
            player.storage.clicking = True
            # set selected to nothing
            if player.storage.selected != -1:
                player.storage.inv[player.storage.selected].selected = False
                player.storage.inv[player.storage.selected].re_blit()
                player.storage.selected = -1
        elif player.storage.clicking and not cursor.Lclick:
            player.storage.clicking = False

        # inventory cells clicked ?
        if (
            player.storage.status
            and cursor.Lclick
            and (
                (
                    220 <= cursor.x <= 900
                    and 130 <= cursor.y <= 555
                    and cursor.x // 5 not in {61, 78, 95, 112, 129, 146, 163}
                    and cursor.y // 5 not in {43, 60, 77, 94}
                )
                or (920 <= cursor.x <= 1000 and 215 <= cursor.y <= 470 and cursor.y // 5 not in {60, 77})
            )
            and (not player.storage.clicking)
        ):
            # within bounds = 220 + 85x , 130 + 85y = 900 555
            # div by 5 and then compare x = {61, 78, 95, 112, 129, 146, 163} y = {43, 60, 77, 94}
            player.storage.clicking = True
            player.storage.select((cursor.x // 5, cursor.y // 5))
        elif player.storage.clicking and not cursor.Lclick:
            player.storage.clicking = False

        # player switching primary mainhand weapon.
        if (
            (not player.storage.status)
            and cursor.Lclick
            and 815 <= cursor.x <= 1070
            and 590 <= cursor.y <= 670
            and (cursor.x // 5 not in {180, 197})
            and (not player.storage.clicking)
        ):
            player.storage.clicking = True
            player.storage.main_hand((cursor.x - 815) // 85)
            if (
                player.storage.mainhand != 5
                and player.storage.inv[player.storage.mainhand].stored is not None
                and player.storage.inv[player.storage.mainhand].stored.type == "weapon"
            ):
                player.cooldown = weapon_library[player.storage.inv[player.storage.mainhand].stored.name]["cooldown"]
        elif player.storage.clicking and not cursor.Lclick:
            player.storage.clicking = False

        if self.paused:
            pass
        else:
            # remember that this only works if the rooms only go from left to right
            # print(self.active)
            if self.acte[1] <= int(player.x / 50) and self.active < len(roomlist) - 1:
                self.active += 1
                self.acts = (roomlist[self.active].spx, roomlist[self.active].spy)
                self.acte = (roomlist[self.active].w, roomlist[self.active].h)
            elif self.acts[1] > int(player.x / 50) and self.active > 0:
                self.active -= 1
                self.acts = (roomlist[self.active].spx, roomlist[self.active].spy)
                self.acte = (roomlist[self.active].w, roomlist[self.active].h)

            # self.enemy_pos = [(int(nxt.x/50), int(nxt.y/50)) for nxt in self.enemies]

            roomlist[self.active].update()

            enemyattacks = []

            for nxt in self.enemies:  # keep it separate for object collision
                roomlist[self.active].roomcollision(nxt)
                enemyattacks = enemyattacks + nxt.attacks

            roomlist[self.active].roomcollision(player)

            player.update(enemyattacks)

            removelist = []
            for nxt in self.enemies:
                nxt.enemy_pos = [player.x, player.y]
                nxt.update(roomlist[self.active], (player.x + 24, player.y + 24), player)
                if nxt.health <= 0:
                    removelist.append(nxt)
                    for _i in range(random.randint(1, 2)):
                        it = random.randint(0, len(item_library["all"]) - 1)
                        self.drops.append(Item(item_library["all"][it], item_library[item_library["all"][it]]))
                        self.drops[-1].rect.x = random.randint(nxt.x - 17, nxt.x + 18)
                        self.drops[-1].rect.y = random.randint(nxt.y - 17, nxt.y + 18)
            # removing dead enemies
            for nxt in removelist:
                self.enemies.remove(nxt)

            # adding enemies
            # if random.randint(1, 300) == 1:
            #    self.enemies.append(Enemy((7, 7)))
            #    self.enemies[-1].startup((player.x, player.y), roomlist[self.active])

            for i in [player, *self.enemies]:
                # print(player.rect)
                i.collide = None
                i.collide_move = None
                for j in [player, *self.enemies]:
                    if i != j:
                        if isinstance(i, main_player):
                            if i.box.colliderect(j.rect):
                                i.collide = j
                                i.collide_move = [j.speed, j.speed]
                                break
                        elif isinstance(j, main_player):
                            if i.rect.colliderect(j.box):
                                i.collide = j
                                i.collide_move = [j.speed, j.speed]
                                break
                        else:
                            if i.rect.colliderect(j.rect):
                                i.collide = j
                                i.collide_move = [j.speed, j.speed]
                                break

            # item drop collision
            del_list = []
            for item in self.drops:
                if player.box.colliderect(item.rect):
                    item.dropped = False
                    player.storage.auto_fill(item)
                    del_list.append(item)
            for nxt in del_list:
                self.drops.remove(nxt)
            del_list = []

    def minimap_builder(self, screen, enemies, wall):
        square = pygame.Surface((5, 5))  # player point
        square.fill((0, 255, 255))
        screen.blit(square, (1075, 75))
        # find enemy - wall coord relation to player

        square.fill((255, 0, 0))
        for coord in enemies:
            if abs((coord[0] + 25) // 50 - player.x // 50) + abs((coord[1] + 25) // 50 - player.y // 50) <= 14:
                screen.blit(
                    square,
                    (
                        1075 + 5 * ((coord[0] + 25) // 50 - player.x // 50),
                        75 + 5 * ((coord[1] + 25) // 50 - player.y // 50),
                    ),
                )

        square.fill((150, 150, 150))
        for coord in wall:
            if pf.distbetween(coord, (player.x // 50, player.y // 50)) < 14:
                screen.blit(square, (1075 + 5 * (coord[0] - player.x // 50), 75 + 5 * (coord[1] - player.y // 50)))

    def render(self, screen, h, w):
        offset = (player.x + 25 - w / 2 - cursor.mouseoffset[0], player.y + 25 - h / 2 - cursor.mouseoffset[1])

        # pygame.draw.line(screen, (0,255,0), ((self.enemy.x+24-offset[0]), (self.enemy.y+24-offset[1])), ((w/2+cursor.mouseoffset[0]), (h/2+cursor.mouseoffset[1])))
        # pygame.draw.line(screen, (0,255,255), ((self.enemy.x-offset[0]), (self.enemy.y-offset[1])), ((w/2+cursor.mouseoffset[0]), (h/2+cursor.mouseoffset[1])))
        if not self.paused:
            for i in range(max(0, self.active - 1), min(self.active + 2, len(roomlist))):
                roomlist[i].render(screen, offset, (-20, w + 20, -20, h + 20))

            for item in self.drops:
                item.render(screen, offset)

            roomlist[self.active].autocorrections(player)  # switched
            for nxt in self.enemies:
                nxt.render(screen, offset, roomlist[self.active], player)

            if roomlist[self.active].doorsclosed:
                cur_wall = set(roomlist[self.active].staticwalls + roomlist[self.active].doors)
            else:
                cur_wall = set(roomlist[self.active].staticwalls)

            player.render(screen, (h, w), cur_wall)

            mini_map_walls = roomlist[self.active].walls
            if self.active > 0:
                mini_map_walls = (
                    mini_map_walls + roomlist[self.active - 1].staticwalls
                )  # cause only one room's doors will closed at a time
            if self.active < len(roomlist) - 1:
                mini_map_walls = mini_map_walls + roomlist[self.active + 1].staticwalls
            self.minimap_builder(screen, [(nxt.x, nxt.y) for nxt in self.enemies], mini_map_walls)

            # show storage
            player.storage.show(screen, [h, w])
