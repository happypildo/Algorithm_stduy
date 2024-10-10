DIRECTION = [[-1, 0], [0, 1], [1, 0], [0, -1]]

class Snake:
    def __init__(self, N, apple_loc, move_orders):
        self.N = N
        self.direction = 1

        self.body = [[0, 0]]

        self.apple_loc = apple_loc
        self.move_orders = move_orders

        self.game_map = [[0 for _ in range(N)] for _ in range(N)]
        for x_a, y_a in apple_loc:
            self.game_map[x_a - 1][y_a - 1] = 1

    def move(self):
        x_h, y_h = self.body[0]

        x_h, y_h = x_h + DIRECTION[self.direction][0], y_h + DIRECTION[self.direction][1]

        if (-1 < x_h < self.N) and (-1 < y_h < self.N):
            head = [x_h, y_h]

            if head in self.body:
                return False

            if self.game_map[x_h][y_h] == 1:
                # 사과가 있다!
                self.game_map[x_h][y_h] = 0

                remain = self.body[:]
                self.body = [[x_h, y_h]] + remain
            else:
                remain = self.body[:-1]
                self.body = [[x_h, y_h]] + remain

            return True
        else:
            return False

    def debug(self):
        for i in range(self.N):
            for j in range(self.N):
                if [i, j] in self.body:
                    print("X", end=" ")
                else:
                    print(self.game_map[i][j], end = " ")
            print()

map_size = int(input())
num_of_apples = int(input())
apples = [list(map(int, input().split())) for _ in range(num_of_apples)]
num_of_orders = int(input())
orders = [list(input().split()) for _ in range(num_of_orders)]

snake = Snake(map_size, apples, orders)

tik = 1
order_idx = 0
while True:
    ret = snake.move()

    if (order_idx < len(orders)) and (int(orders[order_idx][0]) == tik):
        if orders[order_idx][1] == 'L':
            snake.direction -= 1
            if snake.direction == -1:
                snake.direction = 3
        else:
            snake.direction += 1
            if snake.direction == 4:
                snake.direction = 0
        order_idx += 1

    # print()
    # print(tik, snake.direction)
    # # print(orders[order_idx], " - > ", snake.direction)
    # snake.debug()

    tik += 1

    if not ret:
        break

print(tik - 1)
