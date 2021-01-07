def checkcollision(dimensions1, position1, dimensions2, position2):
    h1, w1 = dimensions1
    h2, w2 = dimensions2
    x1, y1 = position1
    x2, y2 = position2
    # object = (top line, bottom line, left line, right line)
    obj1 = [(x1-int(w1/2)),(x1+int(w1/2)),(y1-int(h1/2)),(y1+int(h1/2))]
    obj2 = [(x2-int(w2/2)),(x2+int(w2/2)),(y2-int(h2/2)),(y2+int(h2/2))]

    if obj1[0] > obj2[1] or obj1[1] < obj2[0]:
        if obj1[2] > obj2[3] or obj1[3] < obj2[2]:
            return True
    return False


