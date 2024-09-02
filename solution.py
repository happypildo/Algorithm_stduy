from pprint import pprint

DIRECTION = [[-1, 0], [0, 1], [1, 0], [0, -1], [0, 0]]
DOWN_CONSIDERATION = [1, 2, 3]
LEFT_CONSIDERATION = [0, 2, 3]
RIGHT_CONSIDERATION = [0, 1, 2]

def move_down(R, C, forest, location):
    moved_location = [(x + 1, y) for x, y in location]
    
    cannot_go = False
    for cons in DOWN_CONSIDERATION:
        x, y = location[cons]
        temp_x, temp_y = x + 1, y
        if -1 < temp_x < R + 3:
            if forest[temp_x][temp_y] != 1 and forest[temp_x][temp_y] != 0:
                cannot_go = True
        else:
            cannot_go = True
    
    if cannot_go:
        # 못가니까 왼쪽으로 구르덩가
        return location, cannot_go
    else:
        return moved_location, cannot_go


def turn(R, C, forest, location, dir, is_left):
    dy = 1
    CONSIDERATION = RIGHT_CONSIDERATION
    if is_left: 
        dy = -1
        CONSIDERATION = LEFT_CONSIDERATION
        
    moved_location = [(x, y + dy) for x, y in location]
    
    cannot_go = False
    for cons in CONSIDERATION:
        x, y = location[cons]
        temp_x, temp_y = x, y + dy
        if -1 < temp_y < C:
            if forest[temp_x][temp_y] != 1 and forest[temp_x][temp_y] != 0:
                cannot_go = True
        else:
            cannot_go = True
    
    if cannot_go:
        return location, dir, cannot_go
    else:
        moved_location, jud = move_down(R, C, forest, moved_location)
        if jud:
            # 아래로 못 내려감
            return location, dir, jud
        else:
            dir -= dy
            if dir < 0: dir = 3
            elif dir > 3: dir = 0
            return moved_location, dir, jud
         
            
    
def solve(R, C, forest, orders):
    for idx, order in enumerate(orders):
        col, dir = order
        
        moved = [(col + dx, 1 + dy) for dx, dy in DIRECTION]
        while True:
            moved, jud = move_down(R, C, forest, moved)
            if jud: break
            
        while True:
            moved, dir, jud = turn(R, C, forest, moved, dir, True)
            if jud: break
        
        while True:
            moved, dir, jud = turn(R, C, forest, moved, dir, False)
            if jud: break
        
        require_reset = False
        for x, y in moved:
            if x < 3:
                require_reset = True
                break
        if require_reset:
            forest = [[1 for _ in range(C)] for _ in range(3)]
            for _ in range(R):
                forest.append([0 for _ in range(C)])
        else:
            for i, (x, y) in enumerate(moved):
                if i == dir: forest[x][y] = 2
                else: forest[x][y] = idx + 3
        pprint(forest)
        print("---------")
        

R, C, K = list(map(int, input().split()))
orders = [list(map(int, input().split())) for _ in range(K)]

forest = [[1 for _ in range(C)] for _ in range(3)]
for _ in range(R):
    forest.append([0 for _ in range(C)])
    
solve(R, C, forest, orders)