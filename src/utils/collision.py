from math import sqrt
TILE_SIZE = 50

def dist_eucl(x1, y1, x2, y2) -> float:
    return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

def dist_manh(x1, y1, x2, y2) -> float:
    return abs(x1-x2) + abs(y1-y2)

def rect_rect(x1, y1, w1, h1, x2, y2, w2, h2, centered = False) -> bool:
    if not centered:
        return (x1 + w1 > x2 and x1 < x2 + w2) and (y1 + h1 > y2 and y1 < y2 + h2)
    return (x1 + w1//2 + 1 > x2 - w2//2 and x1 - w1//2 < x2 + w2//2 + 1) and (y1 + h1//2 + 1 > y2 - h2//2 and y1 - h1//2 < y2 + h2//2 + 1)

# def raycast(x, y, dx, dy, collidefn, dist = TILE_SIZE * 30, itrs = 5) -> tuple[int, int] | None:
#    return None

# def rect_centered(x1, y1, w1, h1, x2, y2, w2, h2) -> bool:
#    


