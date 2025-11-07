import src.utils.collision as Collision

# TODO: decide implementing render queue in camera or hard coding rendering priorities

# 0, 0 center of screen
# 
class Camera:
    MOUSE = "mouse"
    def __init__(self, pos, dims):
        # position of camera in world (non-tile)
        self.x, self.y = pos

        # screen width and height
        self.width, self.height = dims

        # possible rotations
        # self.theta = rot

        # offsets
        self.offsets = dict()
        self.offsets[self.MOUSE] = (0, 0)


    # x, y are global positions
    def onscreen(self, x, y, w, h) -> bool:
        return Collision.rect_rect(x, y, w, h, self.x, self.y, self.width, self.height, True) 
    
    # converts a position to a rendered position
    def renderpos(self, pos: tuple[int, int], dims: tuple[int, int]) -> tuple[int, int]:
        res = (pos[0] - dims[0]//2 - self.x + self.width//2, pos[1] - dims[1]//2 - self.y + self.height//2)
        for offset in self.offsets.values():
            res[0] += offset[0]
            res[1] += offset[1]
        return res

    # converts a position to a local rendered position (for UI elems)
    def renderlpos(self, pos: tuple[int, int], dims: tuple[int, int]) -> tuple[int, int]:
        return (self.width + (pos[0] - dims[0]), self.height + (pos[0] - dims[0]))

    def set_offset(self, key, pos):
        self.offsets[key] = pos