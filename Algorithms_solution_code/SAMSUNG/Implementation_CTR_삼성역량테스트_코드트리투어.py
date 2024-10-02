import heapq

MAX_GRAPH = 2001
MAX_NODES = 2001
MAX_PRODUCTIONS = 30001
IS_PRODUCTION = [False] * MAX_PRODUCTIONS


class Production:
    """
    상품 클래스로서, 가치와 아이디를 기반으로 상품 추천 시 heapq 연산을 수월하게 해준다.
    """
    def __init__(self, p_id, rev, dest, profit):
        self.p_id = p_id
        self.revenue = rev
        self.destination = dest
        self.profit = profit

    def __lt__(self, other):
        if self.profit > other.profit:
            return True
        elif self.profit == other.profit:
            if self.p_id < other.p_id:
                return True
            else:
                return False
        else:
            return False


def dijkstra(graph, start):
    """

    Args:
        graph: 전달 받은 그래프
        start: 시작 노드

    Returns:
        출발지에서 모든 노드로의 거리
    """
    distances = [float('inf') for _ in range(MAX_GRAPH)]
    distances[start] = 0

    min_heap = []
    heapq.heappush(min_heap, [0, start])

    while min_heap:
        dist, node = heapq.heappop(min_heap)

        if graph.get(node, None) is None:
            continue
        for neighbor, weight in graph[node]:
            original_dist = distances[neighbor]
            incoming_dist = distances[node] + weight

            if incoming_dist < original_dist:
                distances[neighbor] = incoming_dist
                heapq.heappush(min_heap, [incoming_dist, neighbor])

    return distances


def make_production(distances, productions, p_id, rev, dest):
    """
    상품을 새로 만드는 함수
    Args:
        distances: 다익스트라 결과물
        productions: 지금까지 저장되어 있던 상품들
        p_id: 추가할 상품 아이디
        rev: 수익
        dest: 목적지

    Returns:

    """
    global IS_PRODUCTION

    # 이득이 되든, 안 되든 새로운 상품으로 추가한다. 왜? 출발지가 바뀌면 이득이 될 수도 있기 때문
    profit = rev - distances[dest]

    new_prod = Production(p_id, rev, dest, profit)
    IS_PRODUCTION[p_id] = True

    # 힙에 넣어줌으로써 상품의 우선 순위를 보장한다.
    heapq.heappush(productions, new_prod)

    return productions


def delete_production(p_id):
    """

    Args:
        p_id: 상품 아이디

    Returns:

    """
    global IS_PRODUCTION

    # 상품 제거 시 IS_PRODUCTION에서 제외시킨다.
    # 원래 접근법은 heapq에서 하나 씩 빼면서 p_id 상품이 나왔을 때 그 녀석을 제외하고 다시 넣었었음
    # 근데 이건 복잡도 좀 빡셈
    if IS_PRODUCTION[p_id]:
        IS_PRODUCTION[p_id] = False


def recommend_production(productions):
    """

    Args:
        productions: 상품 heapq

    Returns:
        추천되는 상품 아이디(없다면 -1), 빼내고 난 후의 상품 heapq
    """
    global IS_PRODUCTION

    if len(productions) == 0:
        # 길이가 0이라면 애초에 추천할 상품이 없다.
        return -1, productions
    else:
        while productions:
            # heapq가 빌 때까지 하나 씩 빼보며 확인한다.
            target_prod = heapq.heappop(productions)

            # 그 녀석이 PRODUCTION이라면,
            if IS_PRODUCTION[target_prod.p_id]:
                # 그리고 그 녀석이 상품 가치가 있다면
                if target_prod.profit >= 0:
                    # 추천해 줬으니 프로덕션에서 없앤다.
                    IS_PRODUCTION[target_prod.p_id] = False
                    return target_prod.p_id, productions
                # 프로덕션인데 상품 가치가 없다면? 우선 순위에 따라 저장이 되었기 때문에 다시 넣어 주고 -1 반환
                else:
                    heapq.heappush(productions, target_prod)
                    return -1, productions

        return -1, productions


def change_start_point(distances, productions):
    """

    Args:
        distances: 다시 계산된 다익스트라 거리
        productions: 상품 heapq

    Returns:
        새로 만든 heapq
    """
    global IS_PRODUCTION

    new_heap = []
    for prod in productions:
        if not IS_PRODUCTION[prod.p_id]:
            continue

        new_heap = make_production(distances, new_heap,
                                   prod.p_id, prod.revenue, prod.destination)

    return distances, new_heap


distance_map = [float('inf') for _ in range(MAX_NODES)]
prods_heap = []
heapq.heapify(prods_heap)

n, m = 0, 0

graph = {}
nodes = set()

start = 0

prev_order = -1
Q = int(input())
for q in range(Q):
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

        distance_map = dijkstra(graph, 0)
    elif order_num == 200:
        # 상품 생성
        prods_heap = make_production(distance_map, prods_heap, orders[1], orders[2], orders[3])
    elif order_num == 300:
        # 상품 삭제
        delete_production(orders[1])
    elif order_num == 400:
        # 최적 상품 제안
        answer, prods_heap = recommend_production(prods_heap)
        print(answer)
    elif order_num == 500:
        # 출발지 변경
        start = orders[1]
        distance_map = dijkstra(graph, start)

        distance_map, prods_heap = change_start_point(distance_map, prods_heap)