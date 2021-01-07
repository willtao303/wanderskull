import pygame
from src.states.teststates.startstatebuttons import StartState
from src.states.teststates.playstate import PlayState
from src.states.teststates.turnstate import TurnState
from src.states.teststates.attackstate import AttackState
from src.states.teststates.camerastate import CameraState
from src.mouse import cursor

class StateMachine():
    def __init__(self):
        self.states = {
            "start":StartState(),
            "play":PlayState(),
            "turn":TurnState(),
            "attack":AttackState(),
            "camera":CameraState()
        }
        self.currentstate = self.states["start"]

        self.currentstate.enter()
        
    def change(self, state2):
        self.currentstate.exit()
        self.currentstate = self.states[state2]
        self.currentstate.enter()

    def update(self, keyspressed, keysdown):
        self.currentstate.update(keyspressed, keysdown)
        if self.currentstate.changeTo != None:
            self.change(self.currentstate.changeTo)

    def render(self, screen, h, w):
        self.currentstate.render(screen, h, w)
        cursor.mouseoffset[0] = -int((cursor.x-(w/2))/w*50)
        cursor.mouseoffset[1] = -int((cursor.y-(h/2))/h*50)
        cursor.render(screen)
        
