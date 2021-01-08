from math import sqrt


def distbetween(m, n):
    return sqrt((m[0]-n[0])**2+(m[1]-n[1])**2)


def createmap(w, h):
    m = []
    for i in range(h):
        m.append([])
        for j in range(w):
            m[i].append(0)

    for i in range(w):
        print(i)
        #m[0][i] = 1
        #m[h-1][i] = 1
##    for i in range(h):
##        map[i][0] = 1
##        map[i][w-1] = 1

        m[6][3] = 1
        m[5][6] = 1
        m[5][7] = 1
        m[6][6] = 1
        m[6][7] = 1

    return m


def DistPathfind(graph, startpos, endpos):
    # dist = dict()  # dictionary of distances from one node to another

    # for i in graph.keys():
    #     dist[i] = dict()  # for all the nodes this node is connected to, create a dictionary
    #     # to store the distances of those nodes to every other node

    dist = {i: dict() for i in graph.keys()}
    # create a dict for all connected nodes

    print(graph)
    for key in graph.keys():  # for every single node
        vis = set()  # no duplicates
        for i in dist.keys():  # if some values have already been precomputed
            if key in dist[i]:
                vis.add(i)
                dist[key][i] = dist[i][key]

        nei = [(key, 0)]  # start at ndoe
        # nei = [((x,y), dist)]  nei[0][0]=(x,y), nei[0][0][0] = x
        vis.add(key)
        dist[key][key] = 0
        while len(nei) > 0:  # while there are still neighbors
            # A simple BFS
            '''
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
            '''
            cur = nei[0][0]  # current node
            step = nei[0][1]  # current distance
            nei.pop(0)
            dist[key][cur] = step  # update the distance in the dictionary
            for nxt in graph[cur]:  # for all the neighbors
                if (not (nxt in vis)):  # check if they are visited
                    nei.append((nxt, sqrt(pow(nxt[0]-cur[0], 2)+pow(nxt[1]-cur[1], 2))+step))
                    vis.add(nxt)  # add it into the queue
        # print(vis)
        # print(dist[key])

    return dist  # return the dictionary of distances

## graf = Convert(createmap(10, 10), 10, 10)
## print(Pathfind(graf, (1,1), (8,8)))
