import src.entities.algorithms.pathfind as pf  # unused?
import pygame
import math


reset = 0  # what does this do


class Enemy():
    def __init__(self):
        self.x = 9*50
        self.y = 6*50
        self.speed = 3
        self.dims = (50, 50)  # size of enemy
        self.rect = pygame.Rect((self.x, self.y), self.dims)
        self.next = None
        self.range = 10+50  # enemy attack range?
        self.angle = 0

        # this is hypothetical
        self.map = None

    def startup(self, ppos, room):
        """Initialize enemy.

        Args:\n
            ppos (float, float): The player position.
            room (Room): The room enemy is currently in?
        """
        print(ppos)
        self.room = room
        self.map = room.dist
        print(self.map[(0, 0)][(9, 9)])
        self.next = self.find_path(ppos)

    def update(self, ppos):
        """Moves enemy closer to player if possible."""
        dist = math.sqrt((self.x+24-ppos[0])**2+(self.y+24-ppos[1])**2)
        x50 = int(self.x/50)
        y50 = int(self.y/50)

        """        
        -5 / 3
        >>> -1.6666666666666667
        int(-5 / 3)
        >>> -1
        -5 // 3
        >>> -2
        If self.xy is negative, integer division would probably be better
        """

        # ----
        if dist > self.range:  # if enemy is in range
            if (x50, y50) == self.next:  # if the current position is at the targeted position
                self.next = self.find_path(ppos)
                relx, rely = self.next[0]*50-self.x, self.next[1]*50-self.y
                self.angle = math.degrees(-math.atan2(rely, relx))  # get the angle
            else:  # move towards the targeted position
                chx, chy = math.cos(-math.radians(self.angle))*self.speed, math.sin(-math.radians(self.angle))*self.speed
                self.x += int(chx)
                self.y += int(chy)
        # ----

        self.rect.x = self.x
        self.rect.y = self.y
    
    def render(self, screen):
        """Draws enemy on a pygame window."""
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def find_path(self, epos):
        """Finds next position for enemy to reach goal."""
        # starting point is at where the enemy is
        start = (self.x // 50, self.y // 50)
        # end is where the player or the objective is
        end = epos
        print(start, "\n", end)
        nextpos = start  # set this to start so that it automatically
        # compares to staying still
        distance = self.map[start][end]
        for k in self.room.graph[(start)]:  # for all the nodes this node is connected to
            print(self.map)
            if distance > self.map[k][end]:  # if the distance to the end node is lower
                nextpos = k  # change the nextpos
                distance = self.map[k][end]
        '''
        while start != end:
            for k in graph[(start[0], start[1])]:
                if distance > dist[k][(end[0],end[1])]:
                    nextpos = k
                    distance = dist[k][(end[0], end[1])]
            if not(distance > dist[(start[0],start[1])][(end[0],end[1])]):
                start = nextpos
            path.append(((epos[0]-nextpos[0], epos[1]-nextpos[1]), nextpos))
            epos = nextpos
        '''
        self.next = nextpos  # update the next node to go to

# enemy = Enemy()
