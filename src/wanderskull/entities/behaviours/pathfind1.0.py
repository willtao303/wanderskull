import math

# global test = 4 #just testing something


def createmap(w, h):
    m = []
    for i in range(h):
        m.append([])
        for _j in range(w):
            m[i].append(0)

    for i in range(w):
        print(i)
        # m[0][i] = 1
        # m[h-1][i] = 1
        ##    for i in range(h):
        ##        map[i][0] = 1
        ##        map[i][w-1] = 1

        m[6][3] = 1  # walls
        m[5][6] = 1
        m[5][7] = 1
        m[6][6] = 1
        m[6][7] = 1

    return m


def Convert(grid, x, y):
    non_wall = []
    for i in range(x):
        for j in range(y):
            if grid[i][j] == 0:
                non_wall.append((j, i))  # ((j,y-i-1))

    graph = {}
    for i in range(len(non_wall)):
        graph[non_wall[i]] = []
        for j in range(len(non_wall)):
            if non_wall[i][0] == non_wall[j][0]:
                if abs(non_wall[i][1] - non_wall[j][1]) == 1:
                    graph[non_wall[i]].append(non_wall[j])
            elif non_wall[i][1] == non_wall[j][1]:
                if abs(non_wall[i][0] - non_wall[j][0]) == 1:
                    graph[non_wall[i]].append(non_wall[j])
            elif abs(non_wall[i][0] - non_wall[j][0]) == 1 and abs(non_wall[i][1] - non_wall[j][1]) == 1:
                graph[non_wall[i]].append(non_wall[j])
    return graph


def Pathfind(graph, ppos, epos):  # noqa: C901 TODO
    dist = {}
    for i in graph:
        dist[i] = {}

    for key in graph:
        vis = set()
        for i in dist:
            if key in dist[i]:
                vis.add(i)
                dist[key][i] = dist[i][key]

        nei = [] + [(i, math.sqrt((i[0] - key[0]) ** 2 + (i[1] - key[1]) ** 2)) for i in graph[key]]
        # nei = [((x,y), dist)]  nei[0][0]=(x,y), nei[0][0][0] = x
        vis.add(key)
        dist[key][key] = 0
        while len(nei) > 0:
            if nei[0][0] in vis:
                if nei[0][1] < dist[key][nei[0][0]]:
                    dist[key][nei[0][0]] = nei[0][1]
            else:
                dist[key][nei[0][0]] = nei[0][1]
                nei = nei + [
                    (i, math.sqrt((i[0] - nei[0][0][0]) ** 2 + (i[1] - nei[0][0][1]) ** 2) + nei[0][1])
                    for i in graph[nei[0][0]]
                ]
                vis.add(nei[0][0])
            nei.pop(0)
            if len(vis) == len(graph):
                break
        # print(dist[key])
    start = epos

    # def find_path():#finds next position
    end = ppos
    nextpos = (0, 0)
    path = []
    distance = 9999
    while start != end:
        for k in graph[(start[0], start[1])]:
            if distance > dist[k][(end[0], end[1])]:
                nextpos = k
                distance = dist[k][(end[0], end[1])]
        if not (distance > dist[(start[0], start[1])][(end[0], end[1])]):
            start = nextpos
        path.append(((epos[0] - nextpos[0], epos[1] - nextpos[1]), nextpos))
        epos = nextpos

    print(path)

    return path


##graf = Convert(createmap(10, 10), 10, 10)
##print(Pathfind(graf, (1,1), (8,8)))
