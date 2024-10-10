DIRECTION = [[], [0, 1], [0, -1], [-1, 0], [1, 0]]
class Dice:
    def __init__(self, init_x, init_y):
        self.value_dict = {idx: 0 for idx in range(1, 7)}
        self.mapping_dict = {
            1: {
                1: 6,
                2: 2,
                3: 5,
                4: 4,
                5: 1,
                6: 3
            },
            2: {
                1: 5,
                2: 2,
                3: 6,
                4: 4,
                5: 3,
                6: 1
            },
            3: {
                1: 4,
                2: 1,
                3: 2,
                4: 3,
                5: 5,
                6: 6
            },
            4: {
                1: 2,
                2: 3,
                3: 4,
                4: 1,
                5: 5,
                6: 6
            }
        }
        self.x = init_x
        self.y = init_y

    def roll(self, N, M, game_map, direction):
        dx, dy = DIRECTION[direction]

        temp_x, temp_y = self.x + dx, self.y + dy

        if (-1 < temp_x < N) and (-1 < temp_y < M):
            # Dice mapping
            self.x, self.y = temp_x, temp_y

            mapping_d = self.mapping_dict[direction]

            new_value_dict = {}
            for key in self.value_dict:
                new_key = mapping_d[key]
                new_value_dict[new_key] = self.value_dict[key]
            self.value_dict = new_value_dict

            if game_map[temp_x][temp_y] == 0:
                game_map[temp_x][temp_y] = self.value_dict[1]
                return self.value_dict[3]
            else:
                self.value_dict[1] = game_map[temp_x][temp_y]
                game_map[temp_x][temp_y] = 0
                return self.value_dict[3]
        else:
            return -1


N, M, x, y, K = list(map(int, input().split()))

world_map = [list(map(int, input().split())) for _ in range(N)]

orders = list(map(int, input().split()))

dice = Dice(x, y)
for i, order in enumerate(orders):
    ret = dice.roll(N, M, world_map, order)
    if ret == -1:
        continue
    else:
        print(ret)
