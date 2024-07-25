DIRECTION = {
    0: [-1, 0],
    1: [1, 0],
    2: [0, -1],
    3: [0, 1]
}
T = 10
N = 16
 
is_visited = set()
 
 
def DFS(maze, node_location):
    global is_visited
 
    if maze[node_location[0]][node_location[1]] == '3':
        return False
 
    ret = True
 
    for dx, dy in DIRECTION.values():
        temp_x = node_location[0] + dx
        temp_y = node_location[1] + dy
 
        if (-1 < temp_x < N) and (-1 < temp_y < N):
            if (temp_x * N + temp_y) not in is_visited and maze[temp_x][temp_y] != '1':
                is_visited.add(temp_x * N + temp_y)
                ret = ret & DFS(maze, [temp_x, temp_y])
 
    return ret
 
 
for t_iter in range(1, T+1):
    _ = int(input())
 
    maze = []
    start_point = []
    end_point = []
 
    is_visited = set()
 
    for n_iter in range(N):
        input_line = input()
        if '2' in input_line:
            start_point = [n_iter, input_line.index('2')]
        elif '3' in input_line:
            end_point = [n_iter, input_line.index('3')]
 
        maze.append(input_line)
 
    is_visited.add(start_point[0] * N + start_point[1])
    if DFS(maze, start_point):
        print(f"#{t_iter} 0")
    else:
        print(f"#{t_iter} 1")