import heapq


class Production:
    def __init__(self, p_id, profit, revenue, destination):
        self.id = p_id
        self.profit = profit
        self.revenue = revenue
        self.destination = destination

    def __lt__(self, other):
        if self.profit > other.profit:
            return True
        elif self.profit == other.profit:
            if self.id < other.id:
                return True
            else:
                return False
        else:
            return False


def dijkstra(graph_size, graph, start):
    distances = [float('inf') for _ in range(graph_size)]
    distances[start] = 0

    min_heap = []
    heapq.heappush(min_heap, [0, start])

    while min_heap:
        dist, node = heapq.heappop(min_heap)

        for neighbor, weight in graph[node]:
            original_dist = distances[neighbor]
            incoming_dist = distances[node] + weight

            if incoming_dist < original_dist:
                distances[neighbor] = incoming_dist
                heapq.heappush(min_heap, [incoming_dist, neighbor])
    
    # 서로 같은 경우에 처리
    
    return distances


def make_productions(distances, production_heap, p_id, revenue, destination):
    cost = distances[destination]
    profit = revenue - cost
    if profit >= 0:
        prod = Production(p_id, profit, revenue, destination)
        heapq.heappush(production_heap, prod)
        return True

    return False


def delete_production(production_heap, is_prod, p_id):
    if p_id not in is_prod:
        return False

    popped_prods = []

    while True:
        if len(production_heap) == 0:
            return False

        prod = heapq.heappop(production_heap)
        if prod.id == p_id:
            break
        popped_prods.append(prod)

    for prod in popped_prods:
        heapq.heappush(production_heap, prod)

    return True


def remake_production(distances, production_heap):
    new_heap = []
    new_is_product = set()
    heapq.heapify(new_heap)
    while production_heap:
        prod = heapq.heappop(production_heap)
        ret = make_productions(distances, new_heap, prod.id, prod.revenue, prod.destination)
        if ret:
            new_is_product.add(prod.id)
    return new_heap, new_is_product


distance_map = None
prods_heap = []
is_product = set()
n, m = 0, 0
graph = {}
heapq.heapify(prods_heap)

Q = int(input())
for _ in range(Q):

    orders = list(map(int, input().split()))

    order_num = orders[0]
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

        distance_map = dijkstra(n, graph, 0)
    elif order_num == 200:
        # 상품 생성
        p_id, revenue, destination = orders[1:]
        ret = make_productions(distance_map, prods_heap, p_id, revenue, destination)
        if ret:
            is_product.add(p_id)
    elif order_num == 300:
        # 상품 삭제
        p_id = orders[1]
        ret = delete_production(prods_heap, is_product, p_id)
        if ret:
            is_product.remove(p_id)
    elif order_num == 400:
        # 최적 상품 제안
        if len(prods_heap) == 0:
            print(-1)
        else:
            prod = heapq.heappop(prods_heap)
            print(prod.id)
    elif order_num == 500:
        # 출발지 변경
        new_start = orders[1]
        distance_map = dijkstra(n, graph, new_start)
        prods_heap, is_product = remake_production(distance_map, prods_heap)
        heapq.heapify(prods_heap)
