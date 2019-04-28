import math
import copy
import random as rand

#classe Rota -> guarda cada rota do trajeto
class Route:
    def __init__(self, total_distance, nodes,current_capacity):
        self.total_distance = total_distance
        self.nodes = nodes
        self.current_capacity = current_capacity

#classe saving -> guarda cada uma das savings
class Saving:
    def __init__(self, distance, clients):
        self.distance = distance
        self.clients = clients

#cria uma lista inicializada com 0s
def CreateList(n):
    list = [0] * n
    return list

#encontra um cliente dentro de uma lista de rotas
def FindRoute(routes_list,node):
    for route in routes_list:
        if node in route.nodes:
            route_length = len(route.nodes)
            node_position = route.nodes.index(node)
            return(route,node_position == 1,node_position == route_length - 2)

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




#calcula o custo total de uma lista de rotas
def RoutesCost(routes):
    cost = 0
    for route in routes:
        cost = cost + route.total_distance
    return cost  

def CreateSavingsList(graph,dimension):
    savings_list = []
    routes = []
    has_route = []
    total_distance = 0
    #cria lista de savings

    pair_visited = []
    for node in range(2,dimension + 1):
        for neighbour in range(2,dimension + 1):
            if [node,neighbour] not in pair_visited and node != neighbour:
                distance = graph[node][0] + graph[neighbour][0] - graph[node][neighbour-1]
                current_saving = Saving(distance,[node,neighbour])
                savings_list.append(current_saving)
                pair_visited.append([neighbour,node])
        savings_list.sort(key=lambda x: x.distance,reverse=True)
    return savings_list




def InitialSolution(graph,demand_list,dimension):
    routes = []
    for cont in range(2, dimension + 1):
        new_route = Route(graph[cont][0]+graph[cont][0],[1]+[cont]+[1],demand_list[cont-1])
        routes.append(new_route)
    return routes


def BuscaLocal(graph,demand_list,max_capacity,dimension):
    #gera solucao inicial
    current_solution = InitialSolution(graph,demand_list,dimension)
    savings_list = CreateSavingsList(graph,dimension)
    number_iterations = 0

    while (number_iterations < (len(savings_list)/2) and len(savings_list)!=0):
        client1 = savings_list[0].clients[0]
        client2 = savings_list[0].clients[1]
        #retira saving da lista
        savings_list.pop(0)
        new_solution = Neighbourhood(graph,demand_list,max_capacity,dimension,current_solution,client1,client2)
        cost_diff = RoutesCost(new_solution) - RoutesCost(current_solution)
        #nova solucao e melhor
        if(cost_diff < 0):
            current_solution = new_solution
            number_iterations = 0
        else:
            number_iterations = number_iterations + 1
    return current_solution,RoutesCost(current_solution)  



def Neighbourhood(graph,demand_list,max_capacity,dimension,current_solution,client1,client2):
    new_solution = copy.copy(current_solution)
    demand_client1 = demand_list[client1-1]
    demand_client2 = demand_list[client2-1]

    route1,is_first1,is_last1 = FindRoute(new_solution,client1)
    route2,is_first2,is_last2 = FindRoute(new_solution,client2)
    if(route1.nodes != route2.nodes):
        if(is_first1 or is_last1) and (is_first2 or is_last2) and \
        route1.current_capacity+route2.current_capacity<=max_capacity:
            #cliente 1 e o primeiro na sua rota e cliente 2 e o ultimo na sua rota
            if(is_first1 and is_last2):
                merged_route = Route(route1.total_distance+route2.total_distance-graph[client2][0]-graph[client1][0]+
                graph[client1][client2-1],route2.nodes[:-1]+route1.nodes[1:],route1.current_capacity+route2.current_capacity)

            #cliente 2 e o primeiro na sua rota e cliente 1 e o ultimo na sua rota
            elif(is_last1 and is_first2):
                merged_route = Route(route1.total_distance+route2.total_distance-graph[client1][0]-graph[client2][0]+
                graph[client1][client2-1],route1.nodes[:-1]+route2.nodes[1:],route1.current_capacity+route2.current_capacity)
            
            #cliente 1 e cliente 2 sao os primeiros nas suas rotas 
            elif(is_first1 and is_first2):
                merged_route = Route(route1.total_distance+route2.total_distance-graph[client1][0]-graph[client2][0]+
                graph[client1][client2-1],route1.nodes[::-1][:-1]+route2.nodes[1:],route1.current_capacity+route2.current_capacity)
            
            #cliente 1 e cliente 2 sao os ultimos nas suas rotas
            elif(is_last1 and is_last2):
                merged_route = Route(route1.total_distance+route2.total_distance-graph[client1][0]-graph[client2][0]+
                graph[client1][client2-1],route1.nodes[:-1]+route2.nodes[::-1][1:],route1.current_capacity+route2.current_capacity)

            new_solution.remove(route1)
            new_solution.remove(route2)
            new_solution.append(merged_route)

    return new_solution
                

graph,demand_list,max_capacity,dimension = CreateGraph("X-n101-k25.txt")
routes,total_distance = BuscaLocal(graph,demand_list,max_capacity,dimension)
cont = 1

print('Rota encontradas:')

for route in routes:
    print('\n') 
    print('Rota '+str(cont) +': '+ str(route.nodes))
    print('Distancia: '+str(route.total_distance))
    print('Capacidade: '+str(route.current_capacity))
    cont = cont + 1
    

print('\n')
print("Menor distancia encontrada: " +str(total_distance))