from itertools import combinations
from copy import deepcopy


def find_best(width, height, input_graph, extra_ladders):
    target = [i for i in range(1, width + 1)]

    ret = ride_ladder(width, height, input_graph)

    judge_arr = [abs(r - t) for r, t in zip(ret, target)]
    minimum_req = max(judge_arr)

    if minimum_req > len(extra_ladders):
        return -1
    if minimum_req == 0:
        return 0

    for comb_size in range(minimum_req, len(extra_ladders) + 1):
        for comb in combinations(extra_ladders, comb_size):
            temp_graph = deepcopy(input_graph)
            for w, h in comb:
                if temp_graph.get((w, h), None) is None and temp_graph.get((w + 1, h), None) is None:
                    temp_graph[(w, h)] = (w + 1, h)
                    temp_graph[(w + 1, h)] = (w, h)
                else:
                    break
                ret = ride_ladder(width, height, temp_graph)
                if ret == target:
                    return comb_size

    return -1


def ride_ladder(width, height, target_graph):
    result = []

    for w in range(1, width+1):
        curr_point = (w, 0)
        is_visited = {(w, 0)}

        # 재귀로 돌려봐서 메모리 에러가 발생하는지 확인하자.
        while curr_point[1] != height + 1:
            if target_graph[curr_point] is None:
                curr_point = (curr_point[0], curr_point[1] + 1)
            elif target_graph[curr_point] in is_visited:
                curr_point = (curr_point[0], curr_point[1] + 1)
            else:
                curr_point = target_graph[curr_point]

            is_visited.add(curr_point)

        result.append(curr_point[0])

    return result


N, M, H = list(map(int, input().split()))
graph = {}
remaining_ladder = set()
for n_iter in range(1, N+1):
    for h_iter in range(0, H + 2):
        graph[(n_iter, h_iter)] = None

        # print((n_iter, h_iter))
        if n_iter < N and (0 < h_iter < H + 1):
            remaining_ladder.add((n_iter, h_iter))

for _ in range(M):
    a, b = list(map(int, input().split()))

    # 이로써, (b, a)와 (b+1, a)는 사용할 수 없는 점이 되어 버렸다.
    graph[(b, a)] = (b + 1, a)
    graph[(b + 1, a)] = (b, a)

    remaining_ladder = remaining_ladder - {(b, a), (b + 1, a)}

print(find_best(N, H, graph, remaining_ladder))