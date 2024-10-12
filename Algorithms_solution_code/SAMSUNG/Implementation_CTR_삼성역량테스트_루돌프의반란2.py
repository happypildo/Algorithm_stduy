import heapq


class Santa:
    def __init__(self, r, c, power, idx):
        self.r = r - 1
        self.c = c - 1
        self.power = power
        self.idx = idx

        self.is_stunned = 0
        self.is_dead = False
        self.score = 0

        self.direction = [
            [-1, 0], [0, 1], [1, 0], [0, -1]
        ]


class Rudolph:
    def __init__(self, r, c, power):
        self.r = r - 1
        self.c = c - 1
        self.power = power

        self.direction = [
            [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]
        ]


class RudolphPriority:
    def __init__(self, d, s_r, s_c, s_idx):
        self.d = d
        self.s_r = s_r
        self.s_c = s_c
        self.s_idx = s_idx
        self.direction = []

    def __lt__(self, other):
        if self.d < other.d:
            return True
        elif self.d > other.d:
            return False
        if self.s_r > other.s_r:
            return True
        elif self.s_r < other.s_r:
            return False
        if self.s_c > other.s_c:
            return True
        else:
            return False


class SantaPriority:
    def __init__(self, d, direction, temp_r, temp_c):
        self.d = d
        self.direction = direction
        self.temp_r = temp_r
        self.temp_c = temp_c

    def __lt__(self, other):
        if self.d < other.d:
            return True
        elif self.d > other.d:
            return False
        if self.direction < other.direction:
            return True
        else:
            return False


class Game:
    SANTA_OFFSET = 2
    RUDOLPH = 1

    def __init__(self, map_size, num_of_turns, r, c, santa_info, r_power, s_power):
        self.map_size = map_size
        self.num_of_turns = num_of_turns
        self.rudolph = Rudolph(r, c, r_power)
        self.santas = [Santa(*info[1:], s_power, idx) for idx, info in enumerate(santa_info)]

        self.game_map = [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.game_map[self.rudolph.r][self.rudolph.c] = Game.RUDOLPH
        for santa in self.santas:
            self.game_map[santa.r][santa.c] = santa.idx + Game.SANTA_OFFSET

    def move_rudolph(self):
        # 어떤 산타로 향할 것인지
        min_heap = []
        # for dr, dc in self.rudolph.direction:
        #     temp_r, temp_c = self.rudolph.r + dr, self.rudolph.c + dc
        #
        #     if (-1 < temp_r < self.map_size) and (-1 < temp_c < self.map_size):
        #         for s in self.santas:
        #             if s.is_dead:
        #                 continue
        #             dist = (temp_r - s.r) ** 2 + (temp_c - s.c) ** 2
        #             min_heap.append(RudolphPriority(dist, s.r, s.c, s.idx, temp_r, temp_c, (dr, dc)))
        for s in self.santas:
            if s.is_dead:
                continue
            dist = (self.rudolph.r - s.r) ** 2 + (self.rudolph.c - s.c) ** 2
            min_heap.append(RudolphPriority(dist, s.r, s.c, s.idx))

        heapq.heapify(min_heap)
        target_santa_info = min_heap[0]

        # dr, dc = target_santa_info.s_r - self.rudolph.r, target_santa_info.s_c - self.rudolph.c

        dr, dc = 0, 0
        min_dist = float('inf')
        for dr1, dc1 in self.rudolph.direction:
            temp_r, temp_c = self.rudolph.r + dr1, self.rudolph.c + dc1

            if (-1 < temp_r < self.map_size) and (-1 < temp_c < self.map_size):
                dist = (temp_r - target_santa_info.s_r) ** 2 + (temp_c - target_santa_info.s_c) ** 2
                if min_dist > dist:
                    min_dist = dist
                    dr, dc = dr1, dc1

        target_santa_info.direction = (dr, dc)
        self.game_map[self.rudolph.r][self.rudolph.c] = 0
        self.rudolph.r, self.rudolph.c = self.rudolph.r + dr, self.rudolph.c + dc
        self.game_map[self.rudolph.r][self.rudolph.c] = Game.RUDOLPH

        if self.rudolph.r == target_santa_info.s_r and self.rudolph.c == target_santa_info.s_c:
            return True, target_santa_info
        else:
            return False, target_santa_info

    def interaction(self, santa_idx, direction, power):
        target_santa = self.santas[santa_idx]
        pushed_r, pushed_c = target_santa.r + direction[0] * power, target_santa.c + direction[1] * power

        if (-1 < pushed_r < self.map_size) and (-1 < pushed_c < self.map_size):
            # 밀려날 수 있다.
            if self.game_map[pushed_r][pushed_c] == 0:
                # 산타가 없는 곳이다.
                self.santas[santa_idx].r = pushed_r
                self.santas[santa_idx].c = pushed_c
                self.game_map[pushed_r][pushed_c] = santa_idx + Game.SANTA_OFFSET
            else:
                # 산타가 있는 곳이다.
                other_santa_idx = self.game_map[pushed_r][pushed_c] - Game.SANTA_OFFSET
                self.game_map[pushed_r][pushed_c] = santa_idx + Game.SANTA_OFFSET
                self.santas[santa_idx].r = pushed_r
                self.santas[santa_idx].c = pushed_c
                self.interaction(other_santa_idx, direction, 1)
        else:
            target_santa.is_dead = True

    def move_santa(self, santa):
        min_heap = []
        prev_dist = (self.rudolph.r - santa.r) ** 2 + (self.rudolph.c - santa.c) ** 2
        for idx, (dr, dc) in enumerate(santa.direction):
            temp_r, temp_c = santa.r + dr, santa.c + dc

            dist = float('inf')
            if (-1 < temp_r < self.map_size) and (-1 < temp_c < self.map_size):
                dist = (self.rudolph.r - temp_r) ** 2 + (self.rudolph.c - temp_c) ** 2
                if dist >= prev_dist or self.game_map[temp_r][temp_c] > 1:
                    dist = float('inf')

            min_heap.append(SantaPriority(dist, idx, temp_r, temp_c))

        heapq.heapify(min_heap)

        selected_path = min_heap[0]

        if selected_path.d == float('inf'):
            return

        self.game_map[santa.r][santa.c] = 0
        if self.rudolph.r == selected_path.temp_r and self.rudolph.c == selected_path.temp_c:
            santa.is_stunned = 2
            santa.score += santa.power
            santa.r, santa.c = selected_path.temp_r, selected_path.temp_c
            reverse_d = santa.direction[selected_path.direction]
            reverse_d = (reverse_d[0] * -1, reverse_d[1] * -1)
            self.interaction(santa.idx, reverse_d, santa.power)
        else:
            santa.r, santa.c = selected_path.temp_r, selected_path.temp_c
            self.game_map[santa.r][santa.c] = santa.idx + Game.SANTA_OFFSET

    def play(self):
        for t in range(self.num_of_turns):
            # 루돌프 이동
            is_crushed, santa_info = self.move_rudolph()

            if is_crushed:
                # 점수 올리고, 상호작용 레츠고
                santa_idx = santa_info.s_idx
                self.santas[santa_idx].is_stunned = 2
                self.santas[santa_idx].score += self.rudolph.power
                self.interaction(santa_idx, santa_info.direction, self.rudolph.power)

            # 산타 이동
            for santa in self.santas:
                if santa.is_dead or santa.is_stunned > 0:
                    continue

                self.move_santa(santa)

            # 게임 종료 여부 판단
            is_over = []
            for santa in self.santas:
                is_over.append(santa.is_dead)
                if santa.is_stunned > 0:
                    santa.is_stunned -= 1

                if not santa.is_dead:
                    santa.score += 1

            if sum(is_over) == len(self.santas):
                ret = []
                for santa in self.santas:
                    ret.append(santa.score)
                return ret

        ret = []
        for santa in self.santas:
            ret.append(santa.score)
        return ret

    def display(self):
        for line in self.game_map:
            print(line)


N, M, P, C, D = list(map(int, input().split()))
r_r, r_c = list(map(int, input().split()))
temp_s_info = [list(map(int, input().split())) for _ in range(P)]
s_info = [[] for _ in range(P)]
for s_i in temp_s_info:
    s_info[s_i[0] - 1] = s_i

game = Game(N, M, r_r, r_c, s_info, C, D)
answer = game.play()
for a in answer:
    print(a, end=" ")