DIRECTION = {
    0: [-1, 0],
    1: [1, 0],
    2: [0, -1],
    3: [0, 1]
}
MEMOIZATION = {
}
result = set()
 
N = 4
MAP = [[0 for _ in range(N)] for __ in range(N)]
 
 
def search(possible_string, current_location, depth):
    global result
 
    memoi_string = ""
 
    possible_string = possible_string + str(MAP[current_location[0]][current_location[1]])
 
    if depth == 6:
        result.add(possible_string)
        return
 
    for direction_idx in range(len(DIRECTION)):
        temp_x = int(current_location[0]) + DIRECTION[direction_idx][0]
        temp_y = int(current_location[1]) + DIRECTION[direction_idx][1]
 
        if (-1 < temp_x < N) and (-1 < temp_y < N):
            search(possible_string, [temp_x, temp_y], depth+1)
 
    return memoi_string + str(MAP[current_location[0]][current_location[1]])
 
 
T = int(input())
 
for t_iter in range(1, T+1):
    for n_iter in range(N):
        MAP[n_iter] = list(map(int, input().split()))
 
    MEMOIZATION = {}
    result = set()
 
    for x in range(N):
        for y in range(N):
            search("", [x, y], 0)
            # search("", [x, y], {}, 0)
 
    print(f"#{t_iter} {len(result)}")