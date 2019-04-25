import math
import copy
from random import *
import random as rand



#classe Rota -> guarda cada rota do trajeto
class Route:
    def __init__(self, total_distance, nodes,current_capacity):
        self.total_distance = total_distance
        self.nodes = nodes
        self.current_capacity = current_capacity

#classe distancia -> guarda cada uma das maiores distancias
class Distance:
    def __init__(self, distance, node,current_capacity):
        self.distance = distance
        self.node = node
        self.current_capacity = current_capacity


#cria uma lista inicializada com 0s
def CreateList(n):
    list = [0] * n
    return list

#encontra um cliente dentro de uma lista de rotas
def FindRoute(routes_list,node):
    for route in routes_list:
        if node in route.nodes:
            node_position = route.nodes.index(node)
            return route,node_position

#calcula a distancia euclidiana entre dois pontos
def EuclideanDistance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))

#le o arquvivo no formato esperado. 
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


#retorna um dicionario onde cada chave e um no do grafo
#e cada valor e uma lista com as distancias da chave pros demais nos.
#tambem retorna uma lista com as demandas
def CreateGraph(filename):
    coord_list,demand_list_file,dimension,max_capacity = ReadFile(filename)
    demand_list = []
    graph = {}

    for i in range(1,dimension + 1):
        graph[i] = CreateList(dimension)

    #obtem a distancia entre todos os nos do grafo
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


    return graph,demand_list,max_capacity,dimension
        
#retorna uma solucao inicial
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
        new_route = Route(total_distance+graph[current_route[0]][0]+graph[current_route[-1]][0],[1]+current_route+[1],route_capacity)
        routes.append(new_route)
    return routes



def Neighbourhood(graph,old_routes,dimension,demand_list,max_capacity):
    new_routes = copy.copy(old_routes)

    #obtem todas distancias medias para cada no

    average_distances = []
    for route in new_routes:
        min_dist = 0
        node_with_biggest_avg = -1
        #acha maior distancia media em cada rota
        for node in route.nodes:
            if(node != 1):
                node_position = route.nodes.index(node)
                avg_distance = (graph[node][route.nodes[node_position-1]-1] + graph[node][route.nodes[node_position+1]-1])/2
                if(avg_distance>min_dist):
                    min_dist = avg_distance
                    node_with_biggest_avg = node
        current_average_distance = Distance(min_dist,node_with_biggest_avg,demand_list[node_with_biggest_avg-1])
        average_distances.append(current_average_distance)



    #ordena lista e obtem as 10 maiores distancias
    average_distances.sort(key=lambda x: x.distance,reverse=True)
    biggest_avg_distances = average_distances[0:10]
    #ordena de acordo com a capacidade
    biggest_avg_distances.sort(key=lambda x: x.current_capacity,reverse=True)

    #remove nos com maior distancia
    for node_high_average in biggest_avg_distances:
        route,node_position = FindRoute(new_routes,node_high_average.node)
        new_total_distance = graph[node_high_average.node][route.nodes[node_position-1]-1] + \
        graph[node_high_average.node][route.nodes[node_position+1]-1]

        route_without_node = Route(route.total_distance-new_total_distance+
        graph[route.nodes[node_position-1]][route.nodes[node_position+1]-1],
        route.nodes[:node_position]+route.nodes[node_position+1:],
        route.current_capacity - demand_list[node_high_average.node-1])

        new_routes.remove(route)
        new_routes.append(route_without_node)

    # adiciona os nos em novas rotas(escolhidas aleatoriamente)

    for node_high_average in biggest_avg_distances:
      
        min_dist = float("inf")
        
        node_before = -1

        possible_route_list = []
        for route in new_routes:
            if(route.current_capacity + demand_list[node_high_average.node-1] <= max_capacity):
                possible_route_list.append(new_routes.index(route))
        
        #seleciona rota aleatoriamente
        cont = rand.choice(possible_route_list)

        destination_route = new_routes[cont]
      
        #avalia melhor possibilidade de colocar o no (menor distancia possivel)
        for cont in range(1,len(destination_route.nodes)):
            curr_dist = destination_route.total_distance - graph[destination_route.nodes[cont-1]][destination_route.nodes[cont]-1] + \
            graph[destination_route.nodes[cont-1]][node_high_average.node-1] + \
            graph[node_high_average.node][destination_route.nodes[cont]-1]
            if(curr_dist < min_dist):
                min_dist = curr_dist
                node_before = cont
        improved_route = Route(min_dist,destination_route.nodes[:node_before]+[node_high_average.node]+destination_route.nodes[node_before:],
        destination_route.current_capacity + demand_list[node_high_average.node-1])
        new_routes.remove(destination_route)
        new_routes.append(improved_route)
    return new_routes







            





#calcula o custo total de uma lista de rotas
def RoutesCost(routes):
    cost = 0
    for route in routes:
        cost = cost + route.total_distance
    return cost




# algoritmo de Simulated Annealing
def SimulatedAnnealing(graph,demand_list,max_capacity,dimension):
    current_routes = InitialSolution(graph,demand_list,max_capacity,dimension)
    alfa = 0.99
    iterations_number = 1000
    temperature = 1000
    while(temperature >= 0.01):       
        while(iterations_number >= 0):
            new_routes = Neighbourhood(graph,current_routes,dimension,demand_list,max_capacity)
            cost_difference = RoutesCost(new_routes) - RoutesCost(current_routes)
            if(cost_difference < 0):
                current_routes = copy.copy(new_routes)
            else:
                if(random() < math.exp(((-1)*cost_difference)/temperature)):
                    current_routes = copy.copy(new_routes)
            iterations_number = iterations_number - 1
        temperature = temperature * alfa

    return RoutesCost(current_routes),current_routes



#main

#leitura do arquivo e criacao do grafo

graph,demand_list,max_capacity,dimension = CreateGraph("X-n204-k19.txt")

total_distance,routes = SimulatedAnnealing(graph,demand_list,max_capacity,dimension)
print('Rota encontradas:')
print('\n')

cont = 1
for route in routes:

    print('Rota '+str(cont) +': '+ str(route.nodes))
    print('Distancia: '+str(route.total_distance))
    print('Capacidade: '+str(route.current_capacity))
    print('\n')
    cont = cont + 1

print("Menor distancia encontrada: " +str(total_distance))




    







