import math

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

def SavingsMethod(graph,demand_list,max_capacity,dimension):
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


    #percorre lista de savings
    for saving in savings_list:
        client1 = saving.clients[0]
        client2 = saving.clients[1]
        demand_client1 = demand_list[client1-1]
        demand_client2 = demand_list[client2-1]

        #nenhum dos clientes esta numa rota
        if (client1 not in has_route) and (client2 not in has_route):
            if(demand_client1 + demand_client1)<=max_capacity:
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

        #ambos clientes estao numa rota
        elif (client1 in has_route) and (client2 in has_route):
            #print("Contador:" + str(cont) +"IF 2   "+ str(client1) + str(client2))
            route1,is_first1,is_last1 = FindRoute(routes,client1)
            route2,is_first2,is_last2 = FindRoute(routes,client2)
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

                    routes.remove(route1)
                    routes.remove(route2)
                    routes.append(merged_route)

        #so o cliente 1 esta numa rota
        elif (client1 in has_route) and (client2 not in has_route):
            route1,is_first1,is_last1 = FindRoute(routes,client1)
            if(is_first1 or is_last1):
                if route1.current_capacity+ demand_client2 <= max_capacity:
                    #cliente 1 e o primeiro na sua rota
                    if(is_first1):
                        improved_route = Route(route1.total_distance+graph[client1][client2-1]-graph[client1][0]+
                        graph[client2][0],[1,client2]+route1.nodes[1:],route1.current_capacity+demand_client2)
                    #cliente 1 e o ultimo na sua rota
                    elif(is_last1):
                        improved_route = Route(route1.total_distance+graph[client1][client2-1]-graph[client1][0]+
                        graph[client2][0],route1.nodes[:-1]+[client2,1],route1.current_capacity+demand_client2)         
                    routes.remove(route1)
                    routes.append(improved_route)
                #cria nova rota com cliente 2
                else:
                    new_route = Route(graph[client2][0]+graph[client2][0],[1,client2,1],demand_client2)
                    routes.append(new_route)
                has_route.append(client2)

        #so o cliente 2 esta numa rota
        elif (client1 not in has_route) and (client2 in has_route):
            route2,is_first2,is_last2 = FindRoute(routes,client2)
            if(is_first2 or is_last2):
                if route2.current_capacity + demand_client1 <= max_capacity:
                    #cliente 2 e o primeiro na sua rota
                    if(is_first2):
                        improved_route = Route(route2.total_distance+graph[client1][client2-1]-graph[client2][0]+
                        graph[client1][0],[1,client1]+route2.nodes[1:],route2.current_capacity+demand_client1)
                    #cliente 2 e o ultimo na sua rota
                    elif(is_last2):
                        improved_route = Route(route2.total_distance+graph[client1][client2-1]-graph[client2][0]+
                        graph[client1][0],route2.nodes[:-1]+[client1,1],route2.current_capacity+demand_client1)
                    routes.remove(route2)
                    routes.append(improved_route)
                #cria nova rota com cliente 1
                else:
                    new_route = Route(graph[client1][0]+graph[client1][0],[1,client1,1],demand_client1)
                    routes.append(new_route)
                has_route.append(client1)
    
    return RoutesCost(routes),routes
                

graph,demand_list,max_capacity,dimension = CreateGraph("X-n204-k19.txt")
total_distance,routes = SavingsMethod(graph,demand_list,max_capacity,dimension)

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



