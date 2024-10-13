KNIGHT_OFFSET = 3
DIRECTION = [[-1, 0], [0, 1], [1, 0], [0, -1]]

class Knight:
    def __init__(self, idx, r, c, h, w, k, game_map):
        self.idx = idx
        self.r = r - 1
        self.c = c - 1
        self.h = h
        self.w = w
        self.k = k          # 체력
        self.received_damage = 0

        self.loc = set()
        for i in range(self.r, self.r + self.h):
            for j in range(self.c, self.c + self.w):
                game_map[i][j] = self.idx + KNIGHT_OFFSET
                self.loc.add((i, j))


class Game:
    def __init__(self, game_map, map_size, num_of_knights, num_of_orders, knight_info, orders):
        self.original_game_map = game_map
        self.game_map = [self.original_game_map[i][:] for i in range(map_size)]
        self.map_size = map_size
        self.num_of_knights = num_of_knights
        self.num_of_orders = num_of_orders
        self.knight_info = knight_info
        self.orders = orders

        self.knights = [Knight(idx, *info, self.game_map) for idx, info in enumerate(knight_info)]
        self.loc_of_traps = set()
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.original_game_map[i][j] == 1:
                    self.loc_of_traps.add((i, j))

    def can_move(self, idx, direction, to_be_moved):
        if self.knights[idx].k <= 0:
            return True

        new_loc = set()
        dx, dy = DIRECTION[direction]

        # 같이 밀려나야 할 애들이 있는가?
        ret = True
        for x, y in self.knights[idx].loc:
            temp_x, temp_y = x + dx, y + dy

            if (-1 < temp_x < self.map_size) and (-1 < temp_y < self.map_size):
                if self.game_map[temp_x][temp_y] == 2:
                    continue
                new_loc.add((temp_x, temp_y))
                if self.game_map[temp_x][temp_y] >= KNIGHT_OFFSET and self.game_map[temp_x][temp_y] != idx + KNIGHT_OFFSET:
                    # 밀려나야 할 애가 있다.
                    to_be_moved.append(self.game_map[temp_x][temp_y] - KNIGHT_OFFSET)
                    ret = ret & self.can_move(self.game_map[temp_x][temp_y] - KNIGHT_OFFSET, direction, to_be_moved)

        if ret and len(new_loc) == len(self.knights[idx].loc):
            return True
        else:
            return False

    def move_knight(self, to_be_moved, direction):
        dx, dy = DIRECTION[direction]
        for idx in to_be_moved:
            new_loc = set()
            for x, y in self.knights[idx].loc:
                temp_x, temp_y = x + dx, y + dy
                new_loc.add((temp_x, temp_y))
            self.knights[idx].loc = new_loc

    def play(self):
        for order in self.orders:
            idx, direction = order
            idx -= 1

            to_be = [idx]
            ret = self.can_move(idx, direction, to_be)
            # print()
            # print(ret, to_be)
            to_be = set(to_be)
            if ret:
                self.move_knight(to_be, direction)

            # 맵 재정비
            self.game_map = [self.original_game_map[i][:] for i in range(self.map_size)]

            # 죽이기
            if ret:
                for k_idx in to_be:
                    if k_idx == idx:
                        continue
                    knight = self.knights[k_idx]
                    for loc in knight.loc:
                        if loc in self.loc_of_traps:
                            knight.k -= 1
                            knight.received_damage += 1
                    # print("After health")
                    # print(f"{knight.idx}: {knight.k} ")

            for knight in self.knights:
                if knight.k > 0:
                    for x, y in knight.loc:
                        self.game_map[x][y] = knight.idx + KNIGHT_OFFSET
            #
            # for line in self.game_map:
            #     print(line)

        answer = 0
        for knight in self.knights:
            if knight.k > 0:
                answer += knight.received_damage

        return answer


L, N, Q = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(L)]
input_knights = [list(map(int, input().split())) for _ in range(N)]
input_orders = [list(map(int, input().split())) for _ in range(Q)]

game = Game(input_map, L, N, Q, input_knights, input_orders)
ret = game.play()
print(ret)
