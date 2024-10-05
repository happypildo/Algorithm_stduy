DIRECTION = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}
OFFSET = 3


class Knight:
    def __init__(self, r, c, h, w, k):
        self.knight_num = 0
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.k = k
        self.is_alive = True

        self.area = self.make_area(self.r, self.c)
        self.damage = 0

    def make_area(self, row, col):
        # 기사를 움직이게 한 이후에 영역을 전개한다.
        new_area = set()
        for i in range(self.h):
            for j in range(self.w):
                new_area.add((row + i, col + j))
        return new_area


class Chess:
    def __init__(self, game_map, num_of_knight):
        self.knight_move_map = [[0 for _ in range(len(game_map))] for _ in range(len(game_map))]
        self.obstacle_map = [game_map[i][:] for i in range(len(game_map))]

        self.size = len(self.obstacle_map)
        self.num_of_knight = num_of_knight
        self.knights = [Knight(-1, -1, -1, -1, -1) for _ in range(self.num_of_knight)]

        self.is_moved = [False for _ in range(self.num_of_knight)]

    def __str__(self):
        from pprint import pprint
        print("---- Knight move map")
        for line in self.knight_move_map:
            pprint(line)
        print("---- Obstacle map")
        for line in self.obstacle_map:
            pprint(line)

        return ""

    def initialize(self, idx, r, c, h, w, k):
        # index는 3부터
        self.knights[idx] = Knight(r - 1, c - 1, h, w, k)
        self.knights[idx].knight_num = idx + OFFSET

        for i, j in self.knights[idx].area:
            self.knight_move_map[i][j] = self.knights[idx].knight_num

    def move_knight(self, idx, direction):
        temp_r, temp_c = self.knights[idx].r + DIRECTION[direction][0], self.knights[idx].c + DIRECTION[direction][1]

        # 여러 명의 나이트를 옮겨야 할 때, 어찌할 것인가....
        if (-1 < temp_r < self.size) and (-1 < temp_c < self.size):
            jud = set(self.is_there_something(idx, temp_r, temp_c))

            if len(jud) == 0:
                self.is_moved[idx] = True
                return True
            elif 2 in jud:
                return False
            else:
                ret = True
                for other_knight in jud:
                    ret = ret & self.move_knight(other_knight - OFFSET, direction)

                if ret:
                    self.is_moved[idx] = True
                    return True
                else:
                    return False

        return False

    def is_there_something(self, idx, new_r, new_c):
        new_area = self.knights[idx].make_area(new_r, new_c)

        for i, j in new_area:
            if (0 > i or i > self.size - 1) or (0 > j or j > self.size - 1):
                # 외부로 빠져 나가면 안 돼요 -> 벽으로 치자.
                return [2]
        ret = []
        for i, j in new_area:
            if self.obstacle_map[i][j] == 2:
                # 벽이 있어요
                return [2]
            elif (self.knight_move_map[i][j] > 2) and (self.knight_move_map[i][j] != self.knights[idx].knight_num):
                # 나 아닌 다른 사람이 있어요.
                ret.append(self.knight_move_map[i][j])

        return ret

    def locate_knight(self, knight_direction):
        for idx, can_go in enumerate(self.is_moved):
            if can_go:
                self.knights[idx].r = self.knights[idx].r + DIRECTION[knight_direction][0]
                self.knights[idx].c = self.knights[idx].c + DIRECTION[knight_direction][1]
                self.knights[idx].area = self.knights[idx].make_area(
                    self.knights[idx].r, self.knights[idx].c
                )

        new_map = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for knight in self.knights:
            if knight.is_alive:
                for i, j in knight.area:
                    new_map[i][j] = knight.knight_num
        self.knight_move_map = new_map

    def activate_trap(self, except_idx):
        for i in range(self.size):
            for j in range(self.size):
                if self.knight_move_map[i][j] > 2 and self.obstacle_map[i][j] == 1:
                    idx = self.knight_move_map[i][j] - OFFSET
                    if idx == except_idx:
                        continue
                    if not self.is_moved[idx]:
                        continue

                    self.knights[idx].k -= 1
                    self.knights[idx].damage += 1

                    if self.knights[idx].k == 0:
                        self.knights[idx].is_alive = False

                        for k_i, k_j in self.knights[idx].area:
                            self.knight_move_map[k_i][k_j] = 0


L, N, Q = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(L)]

chess = Chess(input_map, N)

for n_iter in range(N):
    knight_info = list(map(int, input().split()))
    chess.initialize(n_iter, *knight_info)

for q_iter in range(Q):
    knight_idx, knight_dir = list(map(int, input().split()))
    knight_idx -= 1

    chess.is_moved = [False for _ in range(N)]
    if chess.knights[knight_idx].is_alive:
        ret = chess.move_knight(knight_idx, knight_dir)
        if ret:
            chess.locate_knight(knight_dir)
            chess.activate_trap(knight_idx)

answer = 0
for n_iter in range(N):
    answer += chess.knights[n_iter].damage if chess.knights[n_iter].is_alive else 0
print(answer)