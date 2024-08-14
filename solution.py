from collections import deque
from pprint import pprint

MEMOIZATION = {}
is_visited = set()

def start_DFS(graph, price, target_building):
    global MEMOIZATION
    global is_visited

    queue = deque([target_building])

    while queue:
        item = queue.pop()
        is_visited.add(item)

        if MEMOIZATION.get(item, None) is not None:
            print("HI")
            return MEMOIZATION.get(item, None)

        result = []
        for neighbor in graph[item]:
            if neighbor not in is_visited:
                is_visited.add(neighbor)
                result.append(start_DFS(graph, price, neighbor))
        
        # MEMOIZATION
        if len(result) == 0:
            MEMOIZATION[item] = price[item]
        else:
            MEMOIZATION[item] = max(result) + price[item]


    return MEMOIZATION[item]


T = int(input())

for t_iter in range(1, T+1):
    N, K = list(map(int, input().split()))

    graph = {(n_iter + 1): [] for n_iter in range(N)}

    price_for_building = [0] + list(map(int, input().split()))

    for k_iter in range(K):
        num_to, num_from = list(map(int, input().split()))
        graph[num_from].append(num_to)
    target_building = int(input())

    MEMOIZATION = {}
    is_visited = set()

    start_DFS(graph, price_for_building, target_building)
    print(MEMOIZATION[target_building])


"""
1
5 5
1 2 3 4 5 
1 4
2 4
3 4
5 2
1 3
4
"""