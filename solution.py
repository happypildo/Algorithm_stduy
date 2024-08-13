DIRECTION = {
    'up': [-1, 0],
    'down': [1, 0],
    'left': [0, -1],
    'right': [0, 1]
}

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

    return direction


def move_ball(pin_map, N, x, y, start_position, direction, hole_pair):
    score = 0
    already_passed = False
    while True:
        if (x, y) in hole_pair and not already_passed:
            if [x, y] == start_position:
                break
            x, y = hole_pair[(x, y)]
            already_passed = True
        else:
            dx, dy = DIRECTION[direction]
            temp_x = x + dx
            temp_y = y + dy

            if (-1 < temp_x < N) and (-1 < temp_y < N):
                if pin_map[temp_x][temp_y] == 0:
                    pass
                else:
                    temp_direction = change_direction(pin_map[temp_x][temp_y], direction)
                    if temp_direction == -1: break      # BLACKHOLE
                    else: 
                        direction = temp_direction
                        score = score + 1
                x, y = temp_x, temp_y
            else:
                direction = change_direction(5, direction)
                score = score + 1
                x, y = temp_x, temp_y

            if [x, y] == start_position:
                break

            already_passed = False
    
    return score


def start(pin_map, N, hole_pair):
    # 핀볼 게임을 임의의 위치에서 진행한다.
    for x in range(N):
        for y in range(N):
            for dir in DIRECTION:
                print(f"{x, y} - >")
                print(move_ball(pin_map, N, x, y, [x, y], dir, hole_pair))


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
        
    start(pin_map, N, hole_pair)