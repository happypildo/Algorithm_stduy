from collections import deque

DIRECTION = [[-1, 0], [0, 1], [1, 0], [0, -1]]

class Dice:
    def __init__(self, r, c):
        self.r = r
        self.c = c

        self.dice_map = [2, 1, 5, 6, 4, 3]
        self.under_idx = 3

        self.rolling_map = {
            0: {
                3: 0,
                0: 1,
                1: 2,
                2: 3,
                4: 4,
                5: 5
            },
            2: {
                1: 0,
                2: 1,
                3: 2,
                0: 3,
                4: 4,
                5: 5
            },
            3: {
                0: 0,
                5: 1,
                2: 2,
                4: 3,
                1: 4,
                3: 5
            },
            1: {
                0: 0,
                4: 1,
                2: 2,
                5: 3,
                3: 4,
                1: 5
            }
        }


class Game:
    def __init__(self, map_size, num_of_rolls, game_map):
        self.map_size = map_size
        self.num_of_rolls = num_of_rolls
        self.game_map = game_map

        self.dice = Dice(0, 0)

    def get_score(self, start_node, target_number):
        queue = deque([start_node])
        is_visited = {start_node}

        cnt = 1
        while queue:
            x, y = queue.popleft()

            for dx, dy in DIRECTION:
                temp_x, temp_y = x + dx, y + dy

                if (-1 < temp_x < self.map_size) and (-1 < temp_y < self.map_size):
                    if (temp_x, temp_y) in is_visited:
                        continue
                    if self.game_map[temp_x][temp_y] != target_number:
                        continue

                    queue.append((temp_x, temp_y))
                    is_visited.add((temp_x, temp_y))

                    cnt += 1

        return cnt * target_number

    def play(self):
        score = 0
        direction = 3
        for turn in range(self.num_of_rolls):
            # 주사위 이동
            r, c = self.dice.r, self.dice.c

            temp_r, temp_c = r + DIRECTION[direction][0], c + DIRECTION[direction][1]
            if (-1 < temp_r < self.map_size) and (-1 < temp_c < self.map_size):
                self.dice.r, self.dice.c = temp_r, temp_c
            else:
                # 벗어난 곳이기 때문에 반대로 가야 한다.
                direction = (direction + 2) % 4

                temp_r, temp_c = r + DIRECTION[direction][0], c + DIRECTION[direction][1]
                self.dice.r, self.dice.c = temp_r, temp_c

            # 주사위 변형
            mapping_dict = self.dice.rolling_map[direction]

            temp_dice_map = self.dice.dice_map[:]
            for from_idx, to_idx in mapping_dict.items():
                temp_dice_map[to_idx] = self.dice.dice_map[from_idx]
            self.dice.dice_map = temp_dice_map[:]

            under = self.dice.dice_map[self.dice.under_idx]
            on_board = self.game_map[self.dice.r][self.dice.c]

            # Get score
            score += self.get_score((self.dice.r, self.dice.c), on_board)

            if under > on_board:
                # 시계방향 90도 회전
                direction = direction + 1
                if direction == len(DIRECTION):
                    direction = 0
            elif under < on_board:
                # 반시계 90도
                direction = direction - 1
                if direction == -1:
                    direction = len(DIRECTION) - 1

        return score


n, m = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(n)]

game = Game(n, m, input_map)
ret = game.play()
print(ret)

