from pprint import pprint
from collections import deque

DIRECTION = [[-1, 0], [0, 1], [1, 0], [0, -1], [0, 0]]
DOWN_CONSIDERATION = [1, 2, 3]
LEFT_CONSIDERATION = [0, 2, 3]
RIGHT_CONSIDERATION = [0, 1, 2]


def move_down(R, C, forest, location, dir):
    moved_location = [(x + 1, y) for x, y in location]
    
    cannot_go = False
    for cons in DOWN_CONSIDERATION:
        x, y = location[cons]
        temp_x, temp_y = x + 1, y
        if -1 < temp_x < R + 3:
            if forest[temp_x][temp_y] != 1 and forest[temp_x][temp_y] != 0:
                cannot_go = True
                break
        else:
            cannot_go = True
            break
    
    if cannot_go:
        # 못가니까 왼쪽으로 구르덩가
        return location, dir, cannot_go
    else:
        return moved_location, dir, cannot_go


def turn(R, C, forest, location, dir, is_left):
    dy = -1 if is_left else 1
    CONSIDERATION = LEFT_CONSIDERATION if is_left else RIGHT_CONSIDERATION
        
    moved_location = [(x, y + dy) for x, y in location]
    
    cannot_go = False
    for cons in CONSIDERATION:
        x, y = location[cons]
        temp_x, temp_y = x, y + dy
        if -1 < temp_y < C:
            if forest[temp_x][temp_y] != 1 and forest[temp_x][temp_y] != 0:
                cannot_go = True
                break
        else:
            cannot_go = True
            break
    
    if cannot_go:
        return location, dir, cannot_go
    else:
        moved_location, dir, jud = move_down(R, C, forest, moved_location, dir)
        if jud:
            return location, dir, jud
        else:
            dir += dy
            if dir == -1: dir = 3
            elif dir == 4: dir = 0
            return moved_location, dir, jud


def get_lower_bound(R, C, forest, graph, idx_graph, own_id):
    locations, dir = graph[own_id]
    esc_x, esc_y = locations[dir]

    queue = deque()
    queue.append((esc_x, esc_y, own_id))

    is_visited = set()
    is_visited.add((esc_x, esc_y))

    lowest_x = locations[2][0]
    while queue:
        esc_x, esc_y, own_id = queue.popleft()

        for dx, dy in DIRECTION[:-1]:
            temp_x, temp_y = esc_x + dx, esc_y + dy
            if (-1 < temp_x < R + 3) and (-1 < temp_y < C):
                c = forest[temp_x][temp_y]
                if c == 0 or c == 1 or c == own_id: continue 
                n_key = idx_graph[(temp_x, temp_y)]
                neighbor_locations, dir = graph[n_key]
                n_x, n_y = neighbor_locations[dir]

                if (n_x, n_y) in is_visited: continue

                queue.append((n_x, n_y, n_key))
                is_visited.add((n_x, n_y))

                lowest_x = neighbor_locations[2][0] if lowest_x < neighbor_locations[2][0] else lowest_x

    return lowest_x - 2


def recursively_move(R, C, forest, moved, dir):
    while True:
        moved, dir, jud = move_down(R, C, forest, moved, dir)
        if jud: break
    moved, dir, jud = turn(R, C, forest, moved, dir, True)
    if not jud: 
        moved, dir, jud = recursively_move(R, C, forest, moved, dir)
    else:
        moved, dir, jud = turn(R, C, forest, moved, dir, False)
        
        if not jud:
            moved, dir, jud = recursively_move(R, C, forest, moved, dir)
        else: 
            return moved, dir, jud
    return moved, dir, jud

def solve(R, C, forest, orders):
    graph = {}
    idx_graph = {}
    answer = 0
    for idx, order in enumerate(orders):
        col, dir = order
        
        moved = [(1 + dx, col - 1 + dy) for dx, dy in DIRECTION]         
        moved, dir, jud = recursively_move(R, C, forest, moved, dir)
        
        require_reset = False
        
        for x, y in moved:
            if forest[x][y] == 1:
                require_reset = True
                break
        if require_reset:
            graph = {}
            idx_graph = {}
            forest = [[1 for _ in range(C)] for _ in range(3)]
            for _ in range(R):
                forest.append([0 for _ in range(C)])
        else:
            graph[idx + 3] = [moved, dir]
            for i, (x, y) in enumerate(moved):
                idx_graph[(x, y)] = idx + 3
                if i == dir: forest[x][y] = 2
                else: forest[x][y] = idx + 3
            
            answer += get_lower_bound(R, C, forest, graph, idx_graph, idx + 3)
        
    return answer


R, C, K = list(map(int, input().split()))
orders = [list(map(int, input().split())) for _ in range(K)]

forest = [[1 for _ in range(C)] for _ in range(3)]
for _ in range(R):
    forest.append([0 for _ in range(C)])
    
answer = solve(R, C, forest, orders)
print(answer)