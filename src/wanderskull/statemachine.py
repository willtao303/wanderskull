from wanderskull.mouse import cursor
from wanderskull.states.teststates.attackstate import AttackState
from wanderskull.states.teststates.camerastate import CameraState
from wanderskull.states.teststates.playstate import PlayState
from wanderskull.states.teststates.startstatebuttons import StartState
from wanderskull.states.teststates.turnstate import TurnState


class StateMachine:
    def __init__(self):
        self.states = {
            "start": StartState(),
            "play": PlayState(),
            "turn": TurnState(),
            "attack": AttackState(),
            "camera": CameraState(),
        }
        self.currentstate = self.states["start"]

        self.currentstate.enter()

    def change(self, state2):
        self.currentstate.exit()
        self.currentstate = self.states[state2]
        self.currentstate.enter()

    def update(self, keyspressed, keysdown):
        self.currentstate.update(keyspressed, keysdown)
        if self.currentstate.changeTo is not None:
            self.change(self.currentstate.changeTo)

    def render(self, screen, h, w):
        self.currentstate.render(screen, h, w)
        cursor.mouseoffset[0] = -int((cursor.x - (w / 2)) / w * 50)
        cursor.mouseoffset[1] = -int((cursor.y - (h / 2)) / h * 50)
        cursor.render(screen)
