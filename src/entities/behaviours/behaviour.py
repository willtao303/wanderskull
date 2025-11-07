from src.entities.enemies.enemy import Enemy
from src.entities.player import main_player

def chase(enemy: Enemy, player: main_player, range: int):
    enemy.x