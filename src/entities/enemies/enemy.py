import pygame


class Enemy():
    def __init__(self, pos: tuple, sprite_path: str, behaviours: dict):
        #body and position
        self.x = pos[0] * 50
        self.y = pos[1] * 50
        self.size = (50, 50)
        self.hitbox = pygame.Rect((self.x, self.y), self.dims)

        self.speed = 2

        if not sprite_path:
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 0))
        
        self.color = (255, 0, 0)
        self.moveVectorx = 0
        self.moveVectory = 0
        self.moving = True
        self.enemy_pos = [0, 0]

    def render(self):
        pass
    
    def update(self):
        
