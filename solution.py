DIRECTION = {
    'up': [-1, 0],
    'down': [1, 0],
    'left': [0, -1],
    'right': [0, 1]
}

MEMOIZATION = {}


def change_direction(obstacle, direction):
    if obstacle == -1:
        return -1
    elif obstacle == 1:
        if direction == 'up':
            direction = 'down'
        elif direction == 'down':
            direction = 'right'
        elif direction == 'left':
            direction = 'up'
        elif direction == 'right':
            direction = 'left'
    elif obstacle == 2:
        if direction == 'up':
            direction = 'right'
        elif direction == 'down':
            direction = 'up'
        elif direction == 'left':
            direction = 'down'
        elif direction == 'right':
            direction = 'left'
    elif obstacle == 3:
        if direction == 'up':
            direction = 'left'
        elif direction == 'down':
            direction = 'up'
        elif direction == 'left':
            direction = 'right'
        elif direction == 'right':
            direction = 'down'
    elif obstacle == 4:
        if direction == 'up':
            direction = 'down'
        elif direction == 'down':
            direction = 'left'
        elif direction == 'left':
            direction = 'right'
        elif direction == 'right':
            direction = 'up'
    elif obstacle == 5:
        if direction == 'up':
            direction = 'down'
        elif direction == 'down':
            direction = 'up'
        elif direction == 'left':
            direction = 'right'
        elif direction == 'right':
            direction = 'left'
    else:
        return -2
    
    return direction


def recursively_move(pin_map, N, x, y, start_position, direction, hole_pair, depth=0):
    global MEMOIZATION

    ret = 0

    if (-1 < x < N) and (-1 < y < N):
        if [x, y] == start_position and depth != 0:
            return ret
        if pin_map[x][y] == -1:
            return ret

    key = (x, y, direction)
    value = MEMOIZATION.get(key, None)
    if value is not None:
        return value
    
    dx, dy = DIRECTION[direction]
    temp_x = x + dx
    temp_y = y + dy

    if (-1 < temp_x < N) and (-1 < temp_y < N):
        # 이동 가능
        # 장애물 만나면 방향 바꿔서 호출 && +1
        # 홀 만나면 홀로 위치 변경
        if pin_map[temp_x][temp_y] == 0:
            ret = 0 + recursively_move(pin_map, N, temp_x, temp_y, start_position, direction, hole_pair, 1)
        else:
            temp_direction = change_direction(pin_map[temp_x][temp_y], direction)
            if temp_direction == -1: 
                ret =  0
            elif temp_direction == -2:
                # Hole
                holed_x, holed_y = hole_pair[(temp_x, temp_y)]

                ret = 0 + recursively_move(pin_map, N, holed_x, holed_y, start_position, direction, hole_pair, 1)
            else:
                temp_direction = change_direction(pin_map[temp_x][temp_y], direction)
                
                ret = 1 + recursively_move(pin_map, N, temp_x, temp_y, start_position, temp_direction, hole_pair, 1)
    else:
        # 다음에 벽이다 -> 이동 방향 반대로 및 1점
        temp_direction = change_direction(5, direction)

        ret = 1 + recursively_move(pin_map, N, temp_x, temp_y, start_position, temp_direction, hole_pair, 1)
            
    MEMOIZATION[(x, y, direction)] = ret

    return ret

T = int(input())
for t_iter in range(1, T+1):

    N = int(input())

    pin_map = [list(map(int, input().split())) for n_iter in range(N)]

    hole_pair = {}
    for hole in range(6, 11):
        pair = set()
        for i in range(N):
            for j in range(N):
                if pin_map[i][j] == hole:
                    pair.add((i, j))
        pair = list(pair)
        if pair:
            hole_pair[pair[0]] = pair[1]
            hole_pair[pair[1]] = pair[0]
    
    max_score = -1
    for x in range(N):
        for y in range(N):
            MEMOIZATION = {}
            for direction in DIRECTION.keys():
                if pin_map[x][y] == 0:
                    ret = recursively_move(pin_map, N, x, y, [x, y], direction, hole_pair)
                    if max_score < ret:
                        max_score = ret

    print(f"#{t_iter} {max_score}")