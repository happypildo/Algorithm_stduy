"""
N x M 크기의 얼음 틀이 있다. 구멍이 뚫려있는 부분은 0, 칸막이가 있는 부분은 1이다. 
구멍이 뚫려있는 부분끼리 상, 하, 좌, 우 붙어 있는 경우 서로 연결되어 있는 것으로 간주한다.
이 때, 얼음 틀이 주어졌을 때 생성되는 아이스크림의 총 개수를 구하시오.

예)
00110
11111
00000
에서는 총 3개의 아이스크림이 생성된다.
"""
from collections import deque

DIRECTION = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def BFS(N, M, start_point, is_visited, ice_grid):
    if start_point in is_visited:
        return 0, is_visited
    
    x = start_point // M
    y = start_point % M
    if ice_grid[x][y] == '1':
        return 0, is_visited

    queue = deque([start_point])
    is_visited.add(start_point)

    while queue:
        current_point = queue.popleft()
        x = current_point // M
        y = current_point % M

        for direction in DIRECTION:
            dx, dy = direction

            temp_x = x + dx
            temp_y = y + dy
            temp_point = temp_x * M + temp_y

            if (-1 < temp_x < N) and (-1 < temp_y < M):
                if ice_grid[temp_x][temp_y] == '0' and temp_point not in is_visited:
                    is_visited.add(temp_point)
                    queue.append(temp_point)

    return 1, is_visited
    

def solution(N, M):
    answer = 0

    ice_grid = []
    for n_iter in range(N):
        ice_grid.append(input())

    is_visited = set()
    for i in range(N):
        for j in range(M):
            start_point = i * M + j
            is_icecream, is_visited = BFS(N, M, start_point, is_visited, ice_grid)
            answer += is_icecream

    return answer


N, M = list(map(int, input().split()))
print(solution(N, M))