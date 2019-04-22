import math

class Route:
    def __init__(self, total_distance, nodes,current_capacity):
        self.total_distance = total_distance
        self.nodes = nodes
        self.current_capacity = current_capacity

def CreateList(n):
    list = [0] * n
    return list


def FindRoute(routes_list,node):
    for route in routes_list:
        if node in route.nodes:
            route_length = len(route.nodes)
            node_position = route.nodes.index(node)
            return(route,node_position == 1,node_position == route_length - 2)


def EuclideanDistance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))

def ReadFile(filename):
    f = open(filename,"r")
    contents = f.readlines()
    for data in contents:
        if data.split()[0] == "DIMENSION":
            dimension = int(data.split()[2])
        elif data.split()[0] == "CAPACITY":
            max_capacity = int(data.split()[2])
        elif data.split()[0] == "NODE_COORD_SECTION":
            initial_coord_index= contents.index(data) + 1
        elif data.split()[0] == "DEMAND_SECTION":
            initial_demand_index = contents.index(data) + 1
            end_coord_index = contents.index(data) 
        elif data.split()[0] == "DEPOT_SECTION":
            end_demand_index = contents.index(data)
    f.close() 
    coord_list = contents[initial_coord_index:end_coord_index]
    demand_list = contents[initial_demand_index:end_demand_index]
    return coord_list,demand_list,dimension,max_capacity

def CreateGraph(filename):
    coord_list,demand_list_file,dimension,max_capacity = ReadFile(filename)
    demand_list = []
    graph = {}

    for i in range(1,dimension + 1):
        graph[i] = CreateList(dimension)

    for node in coord_list:
        node_data = node.split()
        node_number = int(node_data[0])
        x1 = int(node_data[1])
        y1 = int(node_data[2])
        for neighbour in coord_list:
            neighbour_data = neighbour.split()
            neighbour_number = int(neighbour_data[0])
            x2 = int(neighbour_data[1])
            y2 = int(neighbour_data[2])
            if(graph[node_number][neighbour_number-1] == 0):
                distance = EuclideanDistance(x1,y1,x2,y2)
                graph[node_number][neighbour_number-1] = distance
                graph[neighbour_number][node_number-1] = distance

    for demand in demand_list_file:
        demand_list.append(int(demand.split()[1]))


    # graph = {
    # 1: [0,12 ,11, 7 ,10 ,10 ,9, 8 ,6, 12],
    # 2:[12 ,0,8 ,5 ,9 ,12, 14, 16, 17, 22],
    # 3:[11 ,8 ,0 ,9 ,15 ,17, 8 ,18, 14 ,22],
    # 4:[7, 5 ,9 ,0 ,7 ,9 ,11 ,12, 12 ,17],
    # 5:[10, 9 ,15 ,7, 0 ,3 ,17, 7, 15, 18],
    # 6:[10 ,12, 17, 9 ,3 ,0 ,18, 6 ,15 ,15],
    # 7:[9 ,14, 8, 11 ,17, 18 ,0 ,16 ,8 ,16],
    # 8:[8 ,16 ,18, 12, 7 ,6 ,16 ,0 ,11 ,11],
    # 9:[6 ,17,14 ,12 ,15 ,15, 8, 11, 0 ,10],
    # 10:[12, 22, 22, 17, 18, 15, 16 ,11 ,10, 0]
    # }
    # demand_list = [0,10,15,18,17,3,5,9,4,6]
    # max_capacity = 40
    # dimension = 10

              
    return graph,demand_list,max_capacity,dimension
        

def InitialSolution(graph,demand_list,max_capacity,dimension):
    routes = []
    visited = CreateList(dimension)
    visited[0] = 1
    while 0 in visited:
        current_route = []
        total_distance = 0
        route_capacity = 0
        for cont in range(2, dimension + 1):
            if (route_capacity + demand_list[cont-1] < max_capacity) and visited[cont-1] == 0:
                visited[cont-1] = 1
                route_capacity = route_capacity + demand_list[cont-1]
                current_route.append(cont)
        for cont in range(1,len(current_route)):
            total_distance = total_distance + graph[current_route[cont-1]][current_route[cont]-1]     
        # print('Iteracao' + str(t) + '\n')
        # print('capacidade' + str(route_capacity) + '\n')
        # print(current_route)
        # print('\n')
        # t = t +1
        new_route = Route(total_distance+graph[current_route[0]][0]+graph[current_route[-1]][0],[1]+current_route+[1],route_capacity)
        routes.append(new_route)
    return routes








def SimulatedAnnealing(graph,demand_list,max_capacity,dimension):
    routes = InitialSolution(graph,demand_list,max_capacity,dimension)
    total_distance = 0
    for route in routes:
        total_distance = total_distance + route.total_distance
    return total_distance,routes





graph,demand_list,max_capacity,dimension = CreateGraph("X-n204-k19.txt")
distance,routes = SimulatedAnnealing(graph,demand_list,max_capacity,dimension)
print(distance)

for el in routes:
    print(el.nodes)
    print(el.current_capacity)


r = Route(15,[0,1,0],30)
r2 = Route(28,[0,5,4,0],80)
r4 = Route(28,[0,5,4,0],80)
r3 = Route(38,[0,6,8,0],90)
r.current_capacity = 800
#print(r.current_capacity)
a = [1,2,3]

#print(a)
# lisat = r2.nodes[::-1][:-1]
# print(lisat)
# a = [r,r2,r3]


# print(r2.nodes == r4.nodes)

# for el in a:
#     if 5 in el.nodes:
#         print(len(el.nodes))

# print(a[1])
# dict = {}
# dict[1]=[0,0]
# dict[1][1]=50
# dict[1].append(90)
# print(dict)
# a = [1,3,4,5]

# for i in range(0,len(a)):
#     print(a[i])
#     #a.remove(a[i])

# print(a)