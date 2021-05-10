import pygame
import math
import random


class Healthbar():

    def __init__(self, maxhealth):

        self.maxhealth = maxhealth
        self.health = maxhealth

        self.maxmana = 0
        self.mana = 0

        #health
        self.health_bar = pygame.Surface((400, 30))
        self.health_bar_show = pygame.Surface((400, 30))
        self.health_bar.fill((0,255,0))
        self.health_bar_show.fill((255, 0 ,0))
        #self.health_loss = 0
        #self.health_loss_bar = None

        #mana
        self.mana_bar = pygame.Surface((400, 30))
        self.mana_bar_show = pygame.Surface((400, 30))
        self.mana_bar.fill((0, 0, 255))
        self.mana_bar_show.fill((255, 255, 0))
        #self.mana_loss = 0
        #self.mana_loss_bar = None
    

    def update(self):
        
        self.health_bar = pygame.Surface((400*(self.health/self.maxhealth),30))
        self.health_bar.fill((0, 255, 0))
    

    def render(self, screen):
        #health
        screen.blit(self.health_bar_show, (400, 550))
        screen.blit(self.health_bar, (400, 550))
        #if self.health_loss > 0:
        #    screen.blit(self.health_loss_bar, (int(400*(self.health/self.max_health))+400, 550))#change bounds
        '''mana'''
        screen.blit(self.mana_bar_show, (400, 600))
        screen.blit(self.mana_bar, (400, 600))
        #if self.mana_loss > 0:
        #    screen.blit(self.mana_loss_bar, (int(400*(self.mana/self.max_mana))+400, 700))#change bounds

