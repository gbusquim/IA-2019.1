import math

class Route:
    def __init__(self, total_distance, nodes,current_capacity):
        self.total_distance = total_distance
        self.nodes = nodes
        self.current_capacity = current_capacity

class Saving:
    def __init__(self, distance, clients):
        self.distance = distance
        self.clients = clients

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
        

def SavingsMethod(graph,demand_list,max_capacity,dimension):
    savings_list = []
    routes = []
    has_route = []
    total_distance = 0
    cont = -1
    #cretating savings_list
    pair_visited = []
    for node in range(2,dimension + 1):
        for neighbour in range(2,dimension + 1):
            if [node,neighbour] not in pair_visited and node != neighbour:
                distance = graph[node][0] + graph[neighbour][0] - graph[node][neighbour-1]
                current_saving = Saving(distance,[node,neighbour])
                savings_list.append(current_saving)
                pair_visited.append([neighbour,node])
        savings_list.sort(key=lambda x: x.distance,reverse=True)
    for saving in savings_list:
        client1 = saving.clients[0]
        client2 = saving.clients[1]
        demand_client1 = demand_list[client1-1]
        demand_client2 = demand_list[client2-1]
        #print(demand_client1)
        #print(demand_client2)
        if (client1 not in has_route) and (client2 not in has_route):
            if(demand_client1 + demand_client1)<=max_capacity:
                #print("Contador:" + str(cont) +"IF 1   "+ str(client1) + str(client2))
                new_route = Route((graph[client1][0]+graph[client1][client2-1]+graph[client2][0]),
                [1,client1,client2,1],demand_client1+demand_client2)
                routes.append(new_route)
            else:
                new_route1 = Route(graph[client1][0]+graph[client1][0],[1,client1,1],demand_client1)
                new_route2 = Route(graph[client2][0]+graph[client2][0],[1,client2,1],demand_client2)
                routes.append(new_route1)
                routes.append(new_route2)
            has_route.append(client1)
            has_route.append(client2)

        elif (client1 in has_route) and (client2 in has_route):
            #print("Contador:" + str(cont) +"IF 2   "+ str(client1) + str(client2))
            route1,is_first1,is_last1 = FindRoute(routes,client1)
            route2,is_first2,is_last2 = FindRoute(routes,client2)
            if(route1.nodes != route2.nodes):
                if(is_first1 or is_last1) and (is_first2 or is_last2) and \
                route1.current_capacity+route2.current_capacity<=max_capacity:
                    #node 1 is first and node 2 is last
                    if(is_first1 and is_last2):
                        merged_route = Route(route1.total_distance+route2.total_distance-graph[client2][0]-graph[client1][0]+
                        graph[client1][client2-1],route2.nodes[:-1]+route1.nodes[1:],route1.current_capacity+route2.current_capacity)

                    #node 2 is first and node 1 is last
                    elif(is_last1 and is_first2):
                        merged_route = Route(route1.total_distance+route2.total_distance-graph[client1][0]-graph[client2][0]+
                        graph[client1][client2-1],route1.nodes[:-1]+route2.nodes[1:],route1.current_capacity+route2.current_capacity)
                    
                    #node 1 and 2 are first 
                    elif(is_first1 and is_first2):
                        merged_route = Route(route1.total_distance+route2.total_distance-graph[client1][0]-graph[client2][0]+
                        graph[client1][client2-1],route1.nodes[::-1][:-1]+route2.nodes[1:],route1.current_capacity+route2.current_capacity)
                    
                    #node 1 and 2 are last 
                    elif(is_last1 and is_last2):
                        merged_route = Route(route1.total_distance+route2.total_distance-graph[client1][0]-graph[client2][0]+
                        graph[client1][client2-1],route1.nodes[:-1]+route2.nodes[::-1][1:],route1.current_capacity+route2.current_capacity)

                    routes.remove(route1)
                    routes.remove(route2)
                    routes.append(merged_route)

        elif (client1 in has_route) and (client2 not in has_route):
           # print("Contador: " + str(cont) +"IF 3   "+ str(client1) + str(client2))
            route1,is_first1,is_last1 = FindRoute(routes,client1)
            if(is_first1 or is_last1):
                if route1.current_capacity+ demand_client2 <= max_capacity:
                    if(is_first1):
                        improved_route = Route(route1.total_distance+graph[client1][client2-1]-graph[client1][0]+
                        graph[client2][0],[1,client2]+route1.nodes[1:],route1.current_capacity+demand_client2)
                    elif(is_last1):
                        improved_route = Route(route1.total_distance+graph[client1][client2-1]-graph[client1][0]+
                        graph[client2][0],route1.nodes[:-1]+[client2,1],route1.current_capacity+demand_client2)         
                    routes.remove(route1)
                    routes.append(improved_route)
                else:
                    new_route = Route(graph[client2][0]+graph[client2][0],[1,client2,1],demand_client2)
                    routes.append(new_route)
                has_route.append(client2)

        elif (client1 not in has_route) and (client2 in has_route):
            #print("Contador:" + str(cont) +"IF 4   "+ str(client1) + str(client2))
            route2,is_first2,is_last2 = FindRoute(routes,client2)
            if(is_first2 or is_last2):
                if route2.current_capacity + demand_client1 <= max_capacity:
                    if(is_first2):
                        improved_route = Route(route2.total_distance+graph[client1][client2-1]-graph[client2][0]+
                        graph[client1][0],[1,client1]+route2.nodes[1:],route2.current_capacity+demand_client1)
                    elif(is_last2):
                        improved_route = Route(route2.total_distance+graph[client1][client2-1]-graph[client2][0]+
                        graph[client1][0],route2.nodes[:-1]+[client1,1],route2.current_capacity+demand_client1)
                    routes.remove(route2)
                    routes.append(improved_route)
                else:
                    new_route = Route(graph[client1][0]+graph[client1][0],[1,client1,1],demand_client1)
                    routes.append(new_route)
                has_route.append(client1)

    for route in routes:
        total_distance = total_distance + route.total_distance
    #return total_distance,routes
    return total_distance,routes
                

graph,demand_list,max_capacity,dimension = CreateGraph("X-n204-k19.txt")
distance,routes = SavingsMethod(graph,demand_list,max_capacity,dimension)
print(distance)



# r = Route(15,[0,1,0],30)
# r2 = Route(28,[0,5,4,0],80)
# r4 = Route(28,[0,5,4,0],80)
# r3 = Route(38,[0,6,8,0],90)
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