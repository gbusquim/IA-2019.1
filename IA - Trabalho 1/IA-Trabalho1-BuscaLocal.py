import math
import copy
from random import *
from time import sleep

class Route:
    def __init__(self, total_distance, nodes,current_capacity):
        self.total_distance = total_distance
        self.nodes = nodes
        self.current_capacity = current_capacity


class Distance:
    def __init__(self, distance, node,current_capacity):
        self.distance = distance
        self.node = node
        self.current_capacity = current_capacity

def CreateList(n):
    list = [0] * n
    return list


def FindRoute(routes_list,node):
    for route in routes_list:
        if node in route.nodes:
            node_position = route.nodes.index(node)
            return route,node_position


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

def FindNextPossibleRoute(routes,current_route_index,max_capacity,current_demand):
    while(routes[current_route_index].current_capacity + current_demand > max_capacity):
        #print(str(current_route_index) + '\n')
        #sleep(0.1)
        if current_route_index == len(routes) - 1:
            current_route_index = 0
        else:
            current_route_index = current_route_index + 1
    return routes[current_route_index]


def Neighbourhood(graph,old_routes,dimension,demand_list,max_capacity):
    new_routes = copy.copy(old_routes)
    #print("---INCIO NEIGHBOUR----\n")
    #for a in old_routes:
        # print('No a ser retirado:' + str(node_high_average.node) + '\n')
        # print('No antes dele: '+str(route.nodes[node_position-1])+ '\n')
        # print('No depois dele: '+str(route.nodes[node_position+1])+ '\n')
        # print('Rota atual: '+str(a.nodes) + '\n')
        # print('Distancia atual: '+str(a.total_distance) + '\n')
        # print('Capacidade atual: '+str(a.current_capacity) + '\n')
    # print("Original routes " + '\n')
    # for a in new_routes:
    #     print(a.nodes)
    #     print(a.total_distance)
    #     print(a.current_capacity)
    #get 5 biggest average distances
    average_distances = []
    for node in range(2,dimension + 1):
        route,node_position = FindRoute(new_routes,node)
        current_average_distance = Distance(graph[node][route.nodes[node_position-1]-1] + graph[node][route.nodes[node_position+1]-1],node,demand_list[node-1])
        average_distances.append(current_average_distance)
    average_distances.sort(key=lambda x: x.distance,reverse=True)
    biggest_avg_distances = average_distances[0:5]
    biggest_avg_distances_cap = copy.copy(biggest_avg_distances)
    biggest_avg_distances_cap.sort(key=lambda x: x.current_capacity,reverse=True)

    # print("Savings " + '\n')
    # for a in biggest_avg_distances:
    #     print('Node: ' + str(a.node))
    #     print('Distance: '+ str(a.distance))

    #remove nodes from routes


    for node_high_average in biggest_avg_distances_cap:
        route,node_position = FindRoute(new_routes,node_high_average.node)
        # print('Rota enm que esta: '+str(route.nodes) + '\n')
        new_total_distance = graph[node_high_average.node][route.nodes[node_position-1]-1] + \
        graph[node_high_average.node][route.nodes[node_position+1]-1]

        route_without_node = Route(route.total_distance-new_total_distance+
        graph[route.nodes[node_position-1]][route.nodes[node_position+1]-1],
        route.nodes[:node_position]+route.nodes[node_position+1:],
        route.current_capacity - demand_list[node_high_average.node-1])
        # print('No a ser retirado:' + str(node_high_average.node) + '\n')
        # print('No antes dele: '+str(route.nodes[node_position-1])+ '\n')
        # print('No depois dele: '+str(route.nodes[node_position+1])+ '\n')
        # print('Rota atual: '+str(route_without_node.nodes) + '\n')
        # print('Distancia atual: '+str(route_without_node.total_distance) + '\n')
        new_routes.remove(route)
        new_routes.append(route_without_node)
    #print("---MEIO NEIGHBOUR----\n")
    #for a in old_routes:
        # print('No a ser retirado:' + str(node_high_average.node) + '\n')
        # print('No antes dele: '+str(route.nodes[node_position-1])+ '\n')
        # print('No depois dele: '+str(route.nodes[node_position+1])+ '\n')
        # print('Rota atual: '+str(a.nodes) + '\n')
        # print('Distancia atual: '+str(a.total_distance) + '\n')
        # print('Capacidade atual: '+str(a.current_capacity) + '\n')
    
    # print("------------------NOVA ITERACAO------\n")
    # print("New routes " + '\n')
    # for a in new_routes:
    #     print(a.nodes)
    #     print(a.total_distance)
    #     print(a.current_capacity)

    # add nodes in random routes
    
    numof_routes = len(new_routes)
    for node_high_average in biggest_avg_distances_cap:
        #print('Rota de destino:' + str(destination_route.nodes) + '\n')
        min_dist = float("inf")
        node_before = -1
        #destination_route_index = randint(0,numof_routes-1)
        #print('Rota de destino:' + str(destination_route.nodes) + '\n')
        #if new_routes[destination_route_index].current_capacity + demand_list[node_high_average.node-1] > max_capacity:
        #print("No que nao da para entrar" + str(node_high_average.node) + '\n')
            #destination_route = FindNextPossibleRoute(new_routes,destination_route_index,max_capacity,demand_list[node_high_average.node-1])
       # else:
            #destination_route = new_routes[destination_route_index]
        routes_capacity_list = copy.copy(new_routes)
        routes_capacity_list.sort(key=lambda x: x.total_distance,reverse=False)
        cont = 0
        # print("------------------------")
        # for el in routes_capacity_list:
        #     print(el.current_capacity)
        while(routes_capacity_list[cont].current_capacity + demand_list[node_high_average.node-1] > max_capacity ):
            cont = cont +1
            if(cont>len(routes_capacity_list)-1):
                print("fudeu")
        destination_route = routes_capacity_list[cont]
      


        for cont in range(1,len(destination_route.nodes)):
            curr_dist = destination_route.total_distance - graph[destination_route.nodes[cont-1]][destination_route.nodes[cont]-1] + \
            graph[destination_route.nodes[cont-1]][node_high_average.node-1] + \
            graph[node_high_average.node][destination_route.nodes[cont]-1]
            if(curr_dist < min_dist):
                min_dist = curr_dist
                node_before = cont
        #print('Rota de destino:' + str(destination_route.nodes) + '\n')
        #print("---FIM NEIGHBOUR----\n")
        #for a in old_routes:
        # print('No a ser retirado:' + str(node_high_average.node) + '\n')
        # print('No antes dele: '+str(route.nodes[node_position-1])+ '\n')
        # print('No depois dele: '+str(route.nodes[node_position+1])+ '\n')
            # print('Rota atual: '+str(a.nodes) + '\n')
            # print('Distancia atual: '+str(a.total_distance) + '\n')
            # print('Capacidade atual: '+str(a.current_capacity) + '\n')
        improved_route = Route(min_dist,destination_route.nodes[:node_before]+[node_high_average.node]+destination_route.nodes[node_before:],
        destination_route.current_capacity + demand_list[node_high_average.node-1])
        new_routes.remove(destination_route)
        new_routes.append(improved_route)




    return new_routes


            






def RoutesCost(routes):
    cost = 0
    for route in routes:
        cost = cost + route.total_distance
    return cost





def SimulatedAnnealing(graph,demand_list,max_capacity,dimension):
    current_routes = InitialSolution(graph,demand_list,max_capacity,dimension)
    # print("ROTAS " + '\n')
    # for a in current_routes:
    #     print(a.nodes)
    #     print(a.total_distance)
    #     print(a.current_capacity)
    #     print('\n')
    alfa = 0.95
    beta = 1.05
    iterations_number = 500
    temperature = 4000
    total_distance = 0
    while(temperature >= 0.01):
        
        while(iterations_number >= 0):
            new_routes = Neighbourhood(graph,current_routes,dimension,demand_list,max_capacity)
            cost_difference = RoutesCost(new_routes) - RoutesCost(current_routes)
            print(cost_difference)
            if(cost_difference < 0):
                current_routes = copy.copy(new_routes)
            else:
                if(random() < math.exp(((-1)*cost_difference)/temperature)):
                    current_routes = copy.copy(new_routes)
            # print("---------------------------ITERACAO-----------------")
            # for a in current_routes:
            #     print('Rota atual: '+str(a.nodes) + '\n')
            #     print('Distancia atual: '+str(a.total_distance) + '\n')
            #     print('Capacidade atual: '+str(a.current_capacity) + '\n')
                
    # print("Iteracao " +str(iterations_number) + '\n')

            iterations_number = iterations_number - 1
        temperature = temperature * alfa
        
    # while(temperature > 0.01):
    #     
    #         
    #         cost_difference = RoutesCost(new_routes) - RoutesCost(current_routes)
    #         if(cost_difference < 0):
    #             current_routes = copy.copy(new_routes)
    #         else:
    #             if(random() < math.exp(((-1)*cost_difference)/temperature)):
    #                current_routes = copy.copy(new_routes)
    #         
    #     
       # 
    return current_routes




graph,demand_list,max_capacity,dimension = CreateGraph("X-n115-k10.txt")
ruimoutes = InitialSolution(graph,demand_list,max_capacity,dimension)
bomoutes = SimulatedAnnealing(graph,demand_list,max_capacity,dimension)

#routes = SimulatedAnnealing(graph,demand_list,max_capacity,dimension)
# print(RoutesCost(ruimoutes))
print(RoutesCost(bomoutes))
# for a in bomoutes:
#     print('Rota atual: '+str(a.nodes) + '\n')
#     print('Distancia atual: '+str(a.total_distance) + '\n')
#     print('Capacidade atual: '+str(a.current_capacity) + '\n')

print(RoutesCost(bomoutes))

    





# print(distance)

# for el in routes:
#     print(el.nodes)
#     print(el.current_capacity)


# r = Route(15,[0,1,0],30)
# r2 = Route(28,[0,5,4,0],80)
# r4 = Route(28,[0,5,4,0],80)
# r3 = Route(38,[0,6,8,0],90)
# r2 = copy.copy(r3)
# print(r2.current_capacity)
# #print(r.current_capacity)
# a = [1,2,3]

# #print(a)
# # lisat = r2.nodes[::-1][:-1]
# # print(lisat)
# a = [r,r2,r3]


# # print(r2.nodes == r4.nodes)



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