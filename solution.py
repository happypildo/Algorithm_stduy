from collections import deque

DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def BFS(N, M, maze):
    queue = deque()
    queue.append((0, 0)) 
    # False-False 일 때와 False-True일 때만 값이 갱신될 수 있다.
    price_map = [[float('inf') for m in range(M)] for n in range(N)]
    price_map_with_broken = [[float('inf') for m in range(M)] for n in range(N)]
    price_map[0][0] = 0
    has_broken_map = [[False for m in range(M)] for n in range(N)]

    while queue:
        x, y = queue.popleft()
        
        for direction in DIRECTION:
            dx, dy = direction
            temp_x, temp_y = x + dx, y + dy

            if (-1 < temp_x < N) and (-1 < temp_y < M):
                if maze[temp_x][temp_y] == '0':
                    prev_price = price_map[temp_x][temp_y]
                    incoming_price = price_map[x][y] + 1

                    prev_price_with_broken = price_map_with_broken[temp_x][temp_y]

                    if prev_price > prev_price_with_broken > incoming_price:
                        price_map[temp_x][temp_y] = incoming_price
                        price_map_with_broken[temp_x][temp_y] = incoming_price
                        queue.append((temp_x, temp_y))
                    elif prev_price_with_broken > prev_price > incoming_price:
                        price_map[temp_x][temp_y] = incoming_price
                        price_map_with_broken[temp_x][temp_y] = incoming_price
                        queue.append((temp_x, temp_y))

                elif maze[temp_x][temp_y] == '1' and price_map_with_broken[temp_x][temp_y] == float('inf'):
                    prev_price = price_map_with_broken[temp_x][temp_y]
                    incoming_price = price_map[x][y] + 1

                    if prev_price > incoming_price:
                        price_map_with_broken[temp_x][temp_y] = incoming_price
                        # queue.append((temp_x, temp_y))
                elif maze[temp_x][temp_y] == '1' and price_map_with_broken[temp_x][temp_y] != float('inf'):
                    prev_price = price_map_with_broken[temp_x][temp_y]
                    incoming_price = price_map[x][y] + 1

                    if prev_price_with_broken > incoming_price:
                        price_map_with_broken[temp_x][temp_y] = incoming_price
                        queue.append((temp_x, temp_y))


    print(price_map_with_broken)
    print(price_map)
    return min(price_map[N-1][M-1] + 1, price_map_with_broken[N-1][M-1] + 1)
                         

N, M = list(map(int, input().split()))

maze = [input() for n_iter in range(N)]

answer = BFS(N, M, maze)
answer = -1 if answer == float('inf') else answer
print(answer)