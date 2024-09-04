DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]


def DFS(N, M, input_map, point, current_target, remain_targets, is_visited, depth):
    ret = 0
    x, y = point
    
    for dx, dy in DIRECTION:
        temp_x, temp_y = x + dx, y + dy
        if (-1 < temp_x < N) and (-1 < temp_y < N):
            if (temp_x, temp_y) not in is_visited and input_map[temp_x][temp_y] == 0 and (temp_x, temp_y) not in remain_targets:
                # 갈 수 있음
                temp_is_visited = is_visited | set([(temp_x, temp_y)])
                if (temp_x, temp_y) == current_target:
                    if len(remain_targets) == 0: 
                        ret += 1
                        continue
                    ret += DFS(N, M, input_map, (temp_x, temp_y), remain_targets[0], remain_targets[1:], temp_is_visited, depth+1)
                else:
                    ret += DFS(N, M, input_map, (temp_x, temp_y), current_target, remain_targets, temp_is_visited, depth)
    return ret
                 

N, M = list(map(int, input().split()))

input_map = [list(map(int, input().split())) for _ in range(N)]
orders = [list(map(int, input().split())) for _ in range(M)]
orders = [(order[0] - 1, order[1] - 1) for order in orders]

ret = DFS(N, M, input_map, orders[0], orders[1], orders[2:], set([orders[0]]), 1)
print(ret)