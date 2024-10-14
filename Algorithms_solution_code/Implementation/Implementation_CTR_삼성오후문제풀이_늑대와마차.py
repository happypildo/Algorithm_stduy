from collections import deque

DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]

class HorseCar:
    def __init__(self, r, c, target_r, target_c):
        self.r = r
        self.c = c
        self.target_r = target_r
        self.target_c = target_c

    def move_horse_car(self, game_map):
        queue = deque([(self.r, self.c)])
        prev_nodes = {(self.r, self.c): None}

        while queue:
            r, c = queue.popleft()

            if (r, c) == (self.target_r, self.target_c):
                break

            for dr, dc in DIRECTION:
                temp_r, temp_c = r + dr, c + dc

                if (-1 < temp_r < len(game_map)) and (-1 < temp_c < len(game_map)):
                    if (temp_r, temp_c) in prev_nodes:
                        continue
                    if game_map[temp_r][temp_c] == 1:
                        continue
                    queue.append((temp_r, temp_c))
                    prev_nodes[(temp_r, temp_c)] = (r, c)

        cur_node = (self.target_r, self.target_c)
        path = []
        if prev_nodes.get(cur_node, None) is None:
            return False
        while cur_node is not None:
            path.append(cur_node)
            cur_node = prev_nodes[cur_node]

        self.r, self.c = path[-2]
        return True
    # def move_horse_car(self, game_map):
    #     r, c = self.r, self.c
    #     minimum_dist = float('inf')
    #     minimum_direction = -1
    #     for d_idx, (dr, dc) in enumerate(DIRECTION):
    #         temp_r, temp_c = r + dr, c + dc
    #
    #         dist = float('inf')
    #         if (-1 < temp_r < len(game_map)) and (-1 < temp_c < len(game_map)):
    #             if game_map[temp_r][temp_c] == 1:
    #                 continue
    #             dist = abs(temp_r - self.target_r) + abs(temp_c - self.target_c)
    #
    #             if minimum_dist > dist:
    #                 minimum_dist = dist
    #                 minimum_direction = d_idx
    #         else:
    #             continue
    #
    #     self.r, self.c = self.r + DIRECTION[minimum_direction][0], self.c + DIRECTION[minimum_direction][1]

    def light_up(self, game_map, wolves):
        maximum_lighted_wolves = []
        maximum_lighted_area = set()
        for idx, (dr, dc) in enumerate(DIRECTION):
            lighted_area = set()

            if dc == 0:
                temp_val = [self.r, self.c]
            else:
                temp_val = [self.c, self.r]

            light_direction = dr if dc == 0 else dc
            offset = 0
            while -1 < temp_val[0] < len(game_map):
                for width in range(temp_val[1] - offset, temp_val[1] + offset + 1):
                    if -1 < width < len(game_map):
                        if dc == 0:
                            lighted_area.add((temp_val[0], width))
                        else:
                            lighted_area.add((width, temp_val[0]))

                offset += 1
                temp_val[0] += light_direction

            # 늑대를 한 마리 씩 돌면서 shadow_area 만들기
            shadow_area = set()
            for wolf in wolves:
                own_shadow = set()

                if not wolf.is_alive:
                    continue
                if (wolf.r, wolf.c) not in lighted_area:
                    continue

                if dc == 0:
                    temp_val = [wolf.r, wolf.c]
                    criterion = self.c - wolf.c
                else:
                    temp_val = [wolf.c, wolf.r]
                    criterion = self.r - wolf.r

                light_direction = dr if dc == 0 else dc

                if criterion < 0:
                    # 증가하는 방향으로 offset
                    where = 0
                elif criterion > 0:
                    # 감소하는 방향으로 offset
                    where = 1
                else:
                    where = 2

                offset = 0
                while -1 < temp_val[0] < len(game_map):
                    if where == 0:
                        for width in range(temp_val[1], temp_val[1] + offset + 1):
                            if -1 < width < len(game_map):
                                if dc == 0:
                                    own_shadow.add((temp_val[0], width))
                                else:
                                    own_shadow.add((width, temp_val[0]))
                    elif where == 1:
                        for width in range(temp_val[1] - offset, temp_val[1] + 1):
                            if -1 < width < len(game_map):
                                if dc == 0:
                                    own_shadow.add((temp_val[0], width))
                                else:
                                    own_shadow.add((width, temp_val[0]))
                    else:
                        if dc == 0:
                            own_shadow.add((temp_val[0], temp_val[1]))
                        else:
                            own_shadow.add((temp_val[1], temp_val[0]))

                    offset += 1
                    temp_val[0] += light_direction

                own_shadow = own_shadow - {(wolf.r, wolf.c)}
                shadow_area = shadow_area | own_shadow

            # 최종 영역 구하기
            lighted_area = lighted_area - shadow_area
            lighted_area = lighted_area - {(self.r, self.c)}

            lighted_wolves = []
            num_of_lighted_wolves = 0
            for wolf in wolves:
                if not wolf.is_alive:
                    continue
                if (wolf.r, wolf.c) in lighted_area:
                    lighted_wolves.append(wolf)
                    num_of_lighted_wolves += 1

            if len(maximum_lighted_wolves) < len(lighted_wolves):
                maximum_lighted_wolves = lighted_wolves
                maximum_lighted_area = lighted_area

        return maximum_lighted_wolves, maximum_lighted_area


class Wolf:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.is_alive = True

    def move(self, game_map, hc, lighted_area):
        md = [
            [[-1, 0], [1, 0], [0, -1], [0, 1]],
            [[0, -1], [0, 1], [-1, 0], [1, 0]]
        ]

        moved_dist = 0
        for direction in md:
            prev_dist = abs(self.r - hc.r) + abs(self.c - hc.c)
            minimum_dist = float('inf')
            min_d_idx = -1
            for d_idx, (dr, dc) in enumerate(direction):
                temp_r, temp_c = self.r + dr, self.c + dc

                dist = float('inf')
                if (-1 < temp_r < len(game_map)) and (-1 < temp_c < len(game_map)):
                    if (temp_r, temp_c) in lighted_area:
                        continue

                    dist = abs(temp_r - hc.r) + abs(temp_c - hc.c)

                    if dist >= prev_dist:
                        dist = float('inf')

                if minimum_dist > dist:
                    minimum_dist = dist
                    min_d_idx = d_idx

            if minimum_dist == float('inf'):
                return moved_dist
            else:
                self.r, self.c = self.r + direction[min_d_idx][0], self.c + direction[min_d_idx][1]
                moved_dist += 1

        return moved_dist


class Game:
    def __init__(self, game_map, map_size, num_of_wolves, r, c, t_r, t_c, wolves_info):
        self.game_map = game_map
        self.map_size = map_size
        self.num_of_wolves = num_of_wolves

        self.horse_car = HorseCar(r, c, t_r, t_c)
        self.wolves = [Wolf(*info) for info in wolves_info]

    def play(self):
        while True:
            can_go = self.horse_car.move_horse_car(self.game_map)
            if not can_go:
                print(-1)
                return

            if (self.horse_car.r, self.horse_car.c) == (self.horse_car.target_r, self.horse_car.target_c):
                print(0)
                break

            for wolf in self.wolves:
                if wolf.is_alive:
                    if (wolf.r, wolf.c) == (self.horse_car.r, self.horse_car.c):
                        wolf.is_alive = False

            lighted_wolves, lighted_area = self.horse_car.light_up(self.game_map, self.wolves)

            died_wolves = 0
            total_move = 0
            for wolf in self.wolves:
                if wolf.is_alive and (wolf.r, wolf.c) not in lighted_area:
                    total_move += wolf.move(self.game_map, self.horse_car, lighted_area)

                    if (wolf.r, wolf.c) == (self.horse_car.r, self.horse_car.c):
                        died_wolves += 1
                        wolf.is_alive = False

            print(total_move, len(lighted_wolves), died_wolves)


N, M = list(map(int, input().split()))
hc_r, hc_c, hc_t_r, hc_t_c = list(map(int, input().split()))
input_info = list(map(int, input().split()))
w_info = []
for i in range(M):
    w_info.append([input_info[2 * i], input_info[2 * i + 1]])
input_map = [list(map(int, input().split())) for _ in range(N)]

game = Game(input_map, N, M, hc_r, hc_c, hc_t_r, hc_t_c, w_info)
game.play()