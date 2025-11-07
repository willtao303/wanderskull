import math

def Convert(grid, x, y):
    non_wall = []
    for i in range(x):
        for j in range(y):
            if grid[i][j] == 0:
                non_wall.append((i,j))#((j,y-i-1))
    graph = dict()
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

grid = [[0, 0, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]]

graph = Convert(grid, 4, 4)
for i in graph:
    print(i, graph[i])

dist = dict()

for i in graph.keys():
    dist[i] = dict()

for key in graph.keys():
    vis = set()
    for i in dist.keys():
        if key in dist[i]:
            vis.add(i)
            dist[key][i] = dist[i][key]

    nei = [] + [(i, math.sqrt((i[0]-key[0])**2 + (i[1]-key[1])**2)) for i in graph[key]]
    # nei = [((x,y), dist)]  nei[0][0]=(x,y), nei[0][0][0] = x
    vis.add(key)
    dist[key][key] = 0
    while len(nei) > 0:
        if nei[0][0] in vis:
            if nei[0][1] < dist[key][nei[0][0]]:
                dist[key][nei[0][0]] = nei[0][1]
        else:
            dist[key][nei[0][0]] = nei[0][1]
            nei = nei + [(i, math.sqrt((i[0]-nei[0][0][0])**2 + (i[1]-nei[0][0][1])**2)+nei[0][1]) for i in graph[nei[0][0]]]
            vis.add(nei[0][0])
        nei.pop(0)
        if len(vis) == len(graph):
            break
    #print(key)
    #print(dist[key])
#print(dist[(3, 4)][(4, 4)])

psedogrid = grid
start = list(map(int,input("x y Bot Start").split()))
psedogrid[start[0]][start[1]] = "B"# [grid_length - start[1] - 1]
for k in psedogrid:
    print(k)
psedogrid[start[0]][start[1]] = 0

for i in range(5):
    end = list(map(int,input("Your Pos x y").split()))
    nextpos = (0,0)
    distance = 99999999
    for k in graph[(start[0], start[1])]:
        if distance > dist[k][(end[0],end[1])]:
            nextpos = k
            distance = dist[k][(end[0], end[1])]
    if not(distance > dist[(start[0],start[1])][(end[0],end[1])]):
        start = nextpos
    psedogrid[start[0]][start[1]] = "B"
    psedogrid[end[0]][end[1]]="Y"
    for k in psedogrid:
        print(k)
    psedogrid[start[0]][start[1]] = 0
    psedogrid[end[0]][end[1]] = 0