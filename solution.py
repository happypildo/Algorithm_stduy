import heapq

MAX_GRAPH = 2000
MAX_ID = 30001
NODES = [False for _ in range(MAX_GRAPH)]
POSSIBLE_PRODUCTIONS = [False for _ in range(MAX_ID)]
IS_IN_PRODUCTIONS = [False for _ in range(MAX_ID)]

class Production:
    def __init__(self, p_id, profit, revenue, destination):
        self.id = p_id
        self.profit = profit
        self.revenue = revenue
        self.destination = destination

    def __lt__(self, other):
        global IS_IN_PRODUCTIONS, POSSIBLE_PRODUCTIONS

        if not POSSIBLE_PRODUCTIONS[self.id]:
            return False
        if not POSSIBLE_PRODUCTIONS[other.id]:
            return True

        if self.profit > other.profit:
            return True
        elif self.profit == other.profit:
            if self.id < other.id:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return f"PROFIT {self.profit} - ID {self.id}"


# def dijkstra(graph_size, graph, start):
#     distances = [float('inf') for _ in range(MAX_GRAPH)]
#     distances[start] = 0
#
#     min_heap = []
#     heapq.heappush(min_heap, [0, start])
#
#     while min_heap:
#         dist, node = heapq.heappop(min_heap)
#
#         for neighbor, weight in graph[node]:
#             original_dist = distances[neighbor]
#             incoming_dist = distances[node] + weight
#
#             if incoming_dist < original_dist:
#                 distances[neighbor] = incoming_dist
#                 heapq.heappush(min_heap, [incoming_dist, neighbor])
#
#     return distances
def Floyd(graph):
    distances = [[float('inf') for _ in range(MAX_GRAPH)] for _ in range(MAX_GRAPH)]

    for s in graph.keys():
        distances[s][s] = 0
        for e, w in graph[s]:
            distances[s][e] = w

    for stopover in range(MAX_GRAPH):
        if NODES[stopover]:
            for s in graph.keys():
                for e in graph.keys():
                    if s == stopover or e == stopover:
                        continue
                    distances[s][e] = min(
                        distances[s][e],
                        distances[s][stopover] + distances[stopover][e]
                    )

    return distances


def make_productions(distances, start, production_heap, p_id, revenue, destination):
    global POSSIBLE_PRODUCTIONS, IS_IN_PRODUCTIONS

    cost = distances[start][destination]
    # print(start, destination, distances[start][destination])
    profit = revenue - cost #f cost != float('inf') else float('inf')

    if profit >= 0:
        prod = Production(p_id, profit, revenue, destination)
        POSSIBLE_PRODUCTIONS[p_id] = True
        heapq.heappush(production_heap, prod)
    else:
        prod = Production(p_id, profit, revenue, destination)
        POSSIBLE_PRODUCTIONS[p_id] = False
        heapq.heappush(production_heap, prod)

    IS_IN_PRODUCTIONS[p_id] = True

    return production_heap


def delete_production(production_heap, p_id):
    global IS_IN_PRODUCTIONS, POSSIBLE_PRODUCTIONS

    if not IS_IN_PRODUCTIONS[p_id]:
        return production_heap

    IS_IN_PRODUCTIONS[p_id] = False
    POSSIBLE_PRODUCTIONS[p_id] = False
    heapq.heapify(production_heap)

    return production_heap


def remake_production(distances, start, production_heap):
    new_heap = []
    heapq.heapify(new_heap)

    while production_heap:
        prod = heapq.heappop(production_heap)
        if IS_IN_PRODUCTIONS[prod.id]:
            new_heap = make_productions(distances, start, new_heap, prod.id, prod.revenue, prod.destination)
    return new_heap


distance_map = None
prods_heap = []
is_product = set()
n, m = 0, 0
graph = {}
heapq.heapify(prods_heap)

Q = int(input())
for q in range(Q):
    start = 0
    orders = list(map(int, input().split()))

    order_num = orders[0]
    # print(orders)
    if order_num == 100:
        # 그래프 생성
        n, m, *pairs = orders[1:]
        for i in range(len(pairs) // 3):
            v, u, w = pairs[i * 3:(i + 1) * 3]
            if graph.get(v, None) is None:
                graph[v] = set()
            if graph.get(u, None) is None:
                graph[u] = set()
            graph[v].add((u, w))
            graph[u].add((v, w))

        # distance_map = dijkstra(n, graph, 0)
        distance_map = Floyd(graph)
    elif order_num == 200:
        # 상품 생성
        p_id, revenue, destination = orders[1:]
        prods_heap = make_productions(distance_map, start, prods_heap, p_id, revenue, destination)
    elif order_num == 300:
        # 상품 삭제
        p_id = orders[1]
        prods_heap = delete_production(prods_heap, p_id)
    elif order_num == 400:
        # heapq.heapify(prods_heap)
        # for prod in prods_heap:
        #     print(f"\t {prod} {IS_IN_PRODUCTIONS[prod.id]} {POSSIBLE_PRODUCTIONS[prod.id]}", end=" / ")
        # print()
        # 최적 상품 제안
        if len(prods_heap) == 0:
            print(-1)
        else:
            if POSSIBLE_PRODUCTIONS[prods_heap[0].id]:
                prod = heapq.heappop(prods_heap)
                print(prod.id)
            else:
                print(-1)
    elif order_num == 500:
        # 출발지 변경
        start = orders[1]
        # distance_map = dijkstra(n, graph, new_start)
        prods_heap = remake_production(distance_map, start, prods_heap)
        heapq.heapify(prods_heap)

    # print("")
    # print(orders)
    # for prod in prods_heap:
    #     print(f"{prod} {IS_IN_PRODUCTIONS[prod.id]} {POSSIBLE_PRODUCTIONS[prod.id]}", end = " / ")
    # print("\n-----")