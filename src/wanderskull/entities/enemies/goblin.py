class goblin:
    def __init__(self):
        self.health = 0
        self.attack = (0, 0)  # randint from x to y

    class normal_goblin:  # just a regular one
        pass

    class goblin_archer:  # long ranged attack. Can miss
        pass

    class goblin_berserker:  # glass cannon goblin
        pass

    class goblin_brute:  # high hp tank
        pass


# quick chat:
# william wu: what if we put all of those under a goblin superclass?
# andrew: i agree
