from collections import deque

ROW_OFFSET = 3
DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]


class Golem:
    def __init__(self, y, exit_direction):
        self.x = 1
        self.y = y - 1

        self.exit_direction = exit_direction
        if exit_direction == 0:
            self.exit_location = (self.x - 1, self.y)
        elif exit_direction == 1:
            self.exit_location = (self.x, self.y + 1)
        elif exit_direction == 2:
            self.exit_location = (self.x + 1, self.y)
        else:
            self.exit_location = (self.x, self.y - 1)

        self.is_in = True

        self.area = {
            1: [(1, -1), (1, 1), (2, 0)],
            2: [(-1, -1), (0, -2), (1, -2), (1, -1), (2, -1)],
            3: [(-1, 1), (0, 2), (1, 2), (1, 1), (2, 1)]
        }
        self.exit_rotation = {
            0: (-1, 0),
            1: (0, 1),
            2: (1, 0),
            3: (0, -1)
        }
        self.center_rotation = {
            1: (1, 0),
            2: (1, -1),
            3: (1, 1)
        }

    def search_area(self, idx, game_map, move_idx):
        interest_area = self.area[move_idx]

        search_result = []
        for dx, dy in interest_area:
            temp_x, temp_y = self.x + dx, self.y + dy

            if (-1 < temp_x < len(game_map)) and (-1 < temp_y < len(game_map[0])):
                if game_map[temp_x][temp_y] == 0:
                    search_result.append(True)
                else:
                    search_result.append(False)
            else:
                search_result.append(False)

        if sum(search_result) == len(search_result):
            # Body check!
            if move_idx == 1:
                pass
            elif move_idx == 2:
                self.exit_direction = self.exit_direction - 1
                if self.exit_direction == -1:
                    self.exit_direction = 3
            elif move_idx == 3:
                self.exit_direction = self.exit_direction + 1
                if self.exit_direction == 4:
                    self.exit_direction = 0

            self.x, self.y = self.x + self.center_rotation[move_idx][0], self.y + self.center_rotation[move_idx][1]
            self.exit_location = (
                self.x + self.exit_rotation[self.exit_direction][0],
                self.y + self.exit_rotation[self.exit_direction][1]
            )

            return True
        else:
            return False


class Game:
    def __init__(self, row, col, num_of_golems, golems):
        self.row = row
        self.col = col
        self.num_of_golems = num_of_golems

        self.game_map = [[0 for _ in range(col)] for _ in range(row + ROW_OFFSET)]

        self.golems = [Golem(*info) for info in golems]

        self.score = 0

    def play(self):
        for idx, golem in enumerate(self.golems):
            self.recursively_move(idx)

            reset = False
            for dx, dy in DIRECTION + [[0, 0]]:
                if -1 < golem.x + dx < 3:
                    reset = True
                self.game_map[golem.x + dx][golem.y + dy] = idx + ROW_OFFSET

            if reset:
                self.game_map = [[0 for _ in range(self.col)] for _ in range(self.row + ROW_OFFSET)]
            else:
                # self.game_map[golem.exit_location[0]][golem.exit_location[1]] = 1

                visited_loc = [golem.x + 1]
                visited_idx = [idx]
                self.dfs(idx, golem, visited_loc, visited_idx)
                self.score += max(visited_loc) - ROW_OFFSET + 1

    def recursively_move(self, idx):
        while True:
            jud = self.golems[idx].search_area(idx, self.game_map, 1)
            if not jud:
                break

        jud = self.golems[idx].search_area(idx, self.game_map, 2)
        if jud:
            jud = self.recursively_move(idx)
        else:
            jud = self.golems[idx].search_area(idx, self.game_map, 3)

            if jud:
                jud = self.recursively_move(idx)
            else:
                return jud
        return jud

    def dfs(self, idx, golem, visited_loc, visited_idx):
        x, y = golem.exit_location

        for dx, dy in DIRECTION:
            temp_x, temp_y = x + dx, y + dy

            if (-1 < temp_x < len(self.game_map)) and (-1 < temp_y < len(self.game_map[0])):
                if self.game_map[temp_x][temp_y] != 0 and self.game_map[temp_x][temp_y] != idx + ROW_OFFSET:
                    target_idx = self.game_map[temp_x][temp_y] - ROW_OFFSET
                    if target_idx in visited_idx:
                        continue

                    visited_loc.append(self.golems[target_idx].x + 1)
                    visited_idx.append(target_idx)

                    self.dfs(target_idx, self.golems[target_idx], visited_loc, visited_idx)


R, C, K = list(map(int, input().split()))
infos = [list(map(int, input().split())) for _ in range(K)]

game = Game(R, C, K, infos)
game.play()

print(game.score)