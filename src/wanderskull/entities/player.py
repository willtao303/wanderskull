import math

import pygame

from wanderskull.entities.Attack import Attack, weapon_library
from wanderskull.mouse import cursor
from wanderskull.ui.health_bar import Healthbar
from wanderskull.ui.Inventory import Inventory

# phd = placeholder


class main_player(pygame.sprite.Sprite):
    def __init__(self):
        self.height, self.width = 50, 50
        self.x, self.y = (1 * 50, 1 * 50)

        self.sprite = pygame.Surface((50, 50))  # pygame.image.load(asset_folder + 'images/temp/sample image.png')
        self.sprite.fill((0, 255, 255))
        self.box = None
        self.canGo = {"down": True, "up": True, "left": True, "right": True}
        self.speed = 5
        self.invincible = False
        self.noMove = False  # this can be used in cutscenes or whatever to make the game ignore the movement keys
        self.attackbox = pygame.Surface((20, 70))

        self.collide = None
        self.moving = False

        self.healthbar = Healthbar(1000)

        # attack

        self.cooldown = 0
        self.attacks = []

        # inventory

        self.storage = Inventory()

        # player id
        self.id = 1

    def firstframe(self):
        # insert json get stuff here
        self.box = pygame.Rect((self.x, self.y), (self.height, self.width))

    def update(self, enemyattacks):  # noqa: C901

        # attack detection

        for nxt in enemyattacks:
            idx = self.box.collidelist(nxt.attacks)
            if (self.id not in nxt.hit) and idx != -1:
                # if nxt.stats["mainclass"] == "AOE":
                #    self.knock_back_angle = math.atan2(self.rect.y-nxt.attacks[idx].y, self.rect.x-nxt.attacks[idx].x)
                # else:
                #    self.knock_back_angle = math.atan2(self.rect.y-player.y, self.rect.x-player.x)
                # self.knock_back = nxt.stats["knockback"]
                # self.knockback_total = nxt.stats["knockback"]
                self.healthbar.health -= nxt.stats["damage"]
                nxt.hit.add(self.id)

        # movement
        self.x = self.box.x
        self.y = self.box.y
        keysdown = pygame.key.get_pressed()
        if not self.noMove:
            # moving

            moveVectorx = 0
            moveVectory = 0
            chx, chy = 0, 0

            if self.collide is not None:
                self.canGo["down"] = self.canGo["down"] and self.collide.canGo["down"]
                self.canGo["up"] = self.canGo["up"] and self.collide.canGo["up"]
                self.canGo["left"] = self.canGo["left"] and self.collide.canGo["left"]
                self.canGo["right"] = self.canGo["right"] and self.collide.canGo["right"]

                angle = math.atan2(self.y - self.collide.y, self.x - self.collide.x)
                chx += math.cos(angle) * self.collide.speed
                chy += math.sin(angle) * self.collide.speed

            if (keysdown[pygame.K_DOWN] or keysdown[pygame.K_s]) and self.canGo["down"]:
                moveVectory += self.speed
            if (keysdown[pygame.K_UP] or keysdown[pygame.K_w]) and self.canGo["up"]:
                moveVectory += -self.speed
            if (keysdown[pygame.K_LEFT] or keysdown[pygame.K_a]) and self.canGo["left"]:
                moveVectorx += -self.speed
            if (keysdown[pygame.K_RIGHT] or keysdown[pygame.K_d]) and self.canGo["right"]:
                moveVectorx += self.speed

            if moveVectorx != 0 or moveVectory != 0:
                self.moving = True
            else:
                self.moving = False

            moveVectorx += chx
            moveVectory += chy

            if not self.canGo["down"]:
                moveVectory = min(0, moveVectory)
            if not self.canGo["up"]:
                moveVectory = max(0, moveVectory)
            if not self.canGo["left"]:
                moveVectorx = max(0, moveVectorx)
            if not self.canGo["right"]:
                moveVectorx = min(0, moveVectorx)

        if abs(moveVectorx) == abs(moveVectory) and moveVectorx != 0 and moveVectory != 0:
            diag = math.sqrt(2)  # *(7/(8*math.sqrt(5*self.speed)))
            moveVectorx = math.ceil(moveVectorx / diag)
            moveVectory = math.ceil(moveVectory / diag)

        self.canGo = {"down": True, "up": True, "left": True, "right": True}

        self.box.move_ip(moveVectorx, moveVectory)

        self.healthbar.update()

    def render(self, screen, dims, walls):
        # pygame.draw.rect(screen, (0,255,255), self.box)
        screen.blit(
            self.sprite, ((dims[1] / 2) - 25 + cursor.mouseoffset[0], (dims[0] / 2) - 25 + cursor.mouseoffset[1])
        )
        self.attack(screen, dims, walls)
        # pygame.draw.rect(screen, (255, 255, 0), self.box)
        self.healthbar.render(screen)

    def attack(self, screen, dims, walls):
        """
        Notice:

        since the image rendered on screen has different x, y than the actual player,
        naturally the attack also has a different x, y than the actual player. What needs
        to happen is that we move the rects to the players real x, y and then don't draw.
        For graphics we just have one surface there rendering the animations

        """
        if self.cooldown == 0:  # move this later
            if (
                cursor.Lclick
                and cursor.y < 550
                and not self.storage.status
                and self.storage.mainhand != 5
                and self.storage.inv[self.storage.mainhand].stored is not None
                and "weapon" in self.storage.inv[self.storage.mainhand].stored.type
            ):
                # do the aiming stuff
                angle = math.atan2(cursor.y - dims[0] / 2, cursor.x - dims[1] / 2)
                points = {"chx": math.cos(angle), "chy": math.sin(angle), "angle": angle}
                # send the attack
                name = self.storage.inv[self.storage.mainhand].stored.name
                self.attacks.append(
                    Attack(
                        name,
                        (0, 255, 255),
                        weapon_library[name],
                        points,
                        (self.x, self.y),
                        (self.x, self.y),
                        (cursor.x + 5, cursor.y + 5),
                        dims,
                    )
                )
                # cooldown
                self.cooldown = weapon_library[name]["cooldown"]
                if self.storage.inv[self.storage.mainhand].stored.type == "consumable_weapon":
                    self.storage.inv[self.storage.mainhand].add_item(-1)
        else:
            self.cooldown -= 1

        # update attacks
        for nxt in self.attacks:
            nxt.update((self.x, self.y), (self.x, self.y), walls, screen, dims)

        # delete attacks
        removelist = []
        for nxt in self.attacks:
            if nxt.dur <= 0 or nxt.delete or len(nxt.hit) >= nxt.stats["penetration"]:
                removelist.append(nxt)
                if nxt.stats["on_end"] != "":
                    self.attacks.append(nxt.on_end((self.x, self.y), (player.x, player.y)))
        for nxt in removelist:
            self.attacks.remove(nxt)
        removelist = []

    def attack_prototype(self, screen):
        # self.attackbox.x, self.attackbox.y = self.x+20, self.y+10
        # pygame.draw.rect(screen, (0,255,0), self.attackbox)
        pass


player = main_player()

# quick chat(check main for refrance):
#
