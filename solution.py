from collections import deque

DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def BFS(N, M, maze):
    queue = deque()
    queue.append((0, 0)) 

    queue_for_integ = deque()

    
    price_map = [[float('inf') for m in range(M)] for n in range(N)]                # 벽을 부수지 않고 간 배열
    price_map_with_broken = [[float('inf') for m in range(M)] for n in range(N)]    # 벽을 단 한 번 부수고 간 배열
    has_broken = False          # 벽을 한 번이라도 부쉈는지?
    price_map[0][0] = 0

    while queue:
        x, y = queue.popleft()

        for dx, dy in DIRECTION:
            temp_x, temp_y = x + dx, y + dy
            
            if (-1 < temp_x < N) and (-1 < temp_y < M):
                if maze[temp_x][temp_y] == '0':
                    prev_price = price_map[temp_x][temp_y]
                    incoming_price = price_map[x][y] + 1

                    if prev_price > incoming_price:         # 벽을 부수지 않고 간 배열에 대한 BFS
                        price_map[temp_x][temp_y] = incoming_price
                        queue.append((temp_x, temp_y))
                else:
                    prev_price = price_map_with_broken[temp_x][temp_y]
                    incoming_price = price_map[x][y] + 1

                    if prev_price > incoming_price:     # 벽을 연속으로 부술 수 없기 떄문에, queue.append를 하지 않음
                        price_map_with_broken[temp_x][temp_y] = incoming_price
                        queue_for_integ.append((temp_x, temp_y))    # 이후, 벽을 부순 것과 부수지 않은 것을 통합하기 위해 queue_for_integ 큐에 삽입
                        has_broken = True
    if has_broken:
        while queue_for_integ:
            x, y = queue_for_integ.popleft()
            
            for dx, dy in DIRECTION:
                temp_x, temp_y = x + dx, y + dy

                if (-1 < temp_x < N) and (-1 < temp_y < M):
                    if maze[temp_x][temp_y] == '0':
                        # 부순 적이 있기 때문에, 0으로만 간다.
                        prev_price = price_map_with_broken[temp_x][temp_y]
                        incoming_price = price_map_with_broken[x][y] + 1
                        if prev_price == float('inf'):
                            price_map_with_broken[temp_x][temp_y] = incoming_price
                            queue_for_integ.append((temp_x, temp_y))
                        elif prev_price > incoming_price:
                            price_map_with_broken[temp_x][temp_y] = incoming_price
                            queue_for_integ.append((temp_x, temp_y))
        return price_map_with_broken[N - 1][M - 1] + 1
    else:
        return price_map[N - 1][M - 1] + 1

N, M = list(map(int, input().split()))

maze = [input() for n_iter in range(N)]
answer = BFS(N, M, maze)
answer = -1 if answer == float('inf') else answer
print(answer)