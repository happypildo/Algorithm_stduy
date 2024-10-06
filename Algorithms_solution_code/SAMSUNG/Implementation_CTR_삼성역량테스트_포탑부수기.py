import heapq
from collections import deque

DIRECTION = [
    [0, 1], [1, 0], [0, -1], [-1, 0]
]


class PriorityNode:
    def __init__(self, power, attack_date, rc_sum, c, turret):
        self.power = power
        self.attack_date = attack_date
        self.rc_sum = rc_sum
        self.c = c
        self.turret = turret

    def __lt__(self, other):
        if self.power < other.power:
            return True
        elif self.power > other.power:
            return False
        if self.attack_date < other.attack_date:
            return True
        elif self.attack_date > other.attack_date:
            return False
        if self.rc_sum > other.rc_sum:
            return True
        elif self.rc_sum < other.rc_sum:
            return False
        if self.c > other.c:
            return True
        else:
            return False


class Turret:
    def __init__(self, power, r, c):
        self.power = power
        self.r = r
        self.c = c

        self.attack_date = 0


class War:
    min_depth_count = float('inf')
    min_path = None

    def __init__(self, N, M, turret_map):
        self.N = N
        self.M = M
        self.turret_map = turret_map
        self.bomb_area = [(i, j) for j in range(-1, 2) for i in range(-1, 2)]
        self.active_turrets = set()
        self.all_turret_loc = set()

        for i in range(self.N):
            for j in range(self.M):
                self.turret_map[i][j] = Turret(self.turret_map[i][j], i, j)
                self.all_turret_loc.add((i, j))

    def __str__(self):
        for i in range(self.N):
            for j in range(self.M):
                print(self.turret_map[i][j].power, end=" ")
            print("")
        return ""

    def select_attacker_and_victim(self, for_answer=False):
        self.active_turrets = set()

        min_heap_attacker = []
        min_heap_victim = []

        for i in range(self.N):
            for j in range(self.M):
                turret = self.turret_map[i][j]
                if turret.power == 0:
                    continue
                min_heap_attacker.append(PriorityNode(turret.power, turret.attack_date, i + j, j, turret))
                min_heap_victim.append(PriorityNode(-1 * turret.power, -1 * turret.attack_date, -1 * (i + j), -1 * j, turret))

                turret.attack_date += 1

        heapq.heapify(min_heap_attacker)
        heapq.heapify(min_heap_victim)

        attacker = min_heap_attacker[0].turret
        victim = min_heap_victim[0].turret

        self.active_turrets.add((attacker.r, attacker.c))
        self.active_turrets.add((victim.r, victim.c))

        if not for_answer:
            attacker.attack_date = 0
            attacker.power += self.N + self.M

        return attacker, victim

    def bfs_shortest_path(self, start, goal):
        queue = deque([start])
        prev_nodes = {start: None}

        while queue:
            point = queue.popleft()

            if point == goal:
                break

            for dr, dc in DIRECTION:
                temp_r, temp_c = point[0] + dr, point[1] + dc
                if temp_r == -1:
                    temp_r = self.N - 1
                elif temp_r == self.N:
                    temp_r = 0
                if temp_c == -1:
                    temp_c = self.M - 1
                elif temp_c == self.M:
                    temp_c = 0

                if self.turret_map[temp_r][temp_c].power == 0 or (temp_r, temp_c) in prev_nodes:
                    continue

                queue.append((temp_r, temp_c))
                prev_nodes[(temp_r, temp_c)] = point

        if goal not in prev_nodes:
            return None

        path = [goal]
        curr = prev_nodes[goal]
        while curr is not None:
            path.append(curr)
            curr = prev_nodes[curr]
        path.pop()
        return path

    def DFS(self, point, target, is_visited):
        if point == target:
            if len(is_visited) < War.min_depth_count:
                War.min_depth_count = len(is_visited)
                War.min_path = is_visited
            return

        if War.min_depth_count < len(is_visited):
            return

        for dr, dc in DIRECTION:
            temp_r, temp_c = point[0] + dr, point[1] + dc
            if temp_r == -1:
                temp_r = self.N - 1
            elif temp_r == self.N:
                temp_r = 0
            if temp_c == -1:
                temp_c = self.M - 1
            elif temp_c == self.M:
                temp_c = 0

            if (temp_r, temp_c) not in is_visited and self.turret_map[temp_r][temp_c].power != 0:
                temp_is_visited = is_visited | {(temp_r, temp_c)}
                self.DFS((temp_r, temp_c), target, temp_is_visited)

    def take_attack(self):
        # 클래스 변수 초기화
        War.min_depth_count = float('inf')
        War.min_path = None

        attacker, victim = self.select_attacker_and_victim()

        # self.DFS((attacker.r, attacker.c), (victim.r, victim.c), {(attacker.r, attacker.c)})
        War.min_path = self.bfs_shortest_path((attacker.r, attacker.c), (victim.r, victim.c))

        if War.min_path is not None:
            # 레이져 공격!
            for path in War.min_path:
                if path == (attacker.r, attacker.c):
                    continue
                power = attacker.power
                if path != (victim.r, victim.c):
                    power //= 2

                self.turret_map[path[0]][path[1]].power -= power
                if self.turret_map[path[0]][path[1]].power <= 0:
                    self.turret_map[path[0]][path[1]].power = 0

                self.active_turrets.add(path)
        else:
            for i, j in self.bomb_area:
                v_r, v_c = victim.r, victim.c
                power = attacker.power
                if i != 0 or j != 0:
                    power //= 2

                temp_r, temp_c = v_r + i, v_c + j
                if temp_r == -1:
                    temp_r = self.N - 1
                elif temp_r == self.N:
                    temp_r = 0
                if temp_c == -1:
                    temp_c = self.M - 1
                elif temp_c == self.M:
                    temp_c = 0

                if attacker.r == temp_r and attacker.c == temp_c:
                    continue

                self.turret_map[temp_r][temp_c].power -= power
                if self.turret_map[temp_r][temp_c].power <= 0:
                    self.turret_map[temp_r][temp_c].power = 0

                self.active_turrets.add((temp_r, temp_c))

    def fix_turrets(self):
        to_be_fixed = self.all_turret_loc - self.active_turrets

        cnt = 0
        for r, c in self.all_turret_loc:
            if self.turret_map[r][c].power > 0:
                cnt += 1
                if (r, c) in to_be_fixed:
                    self.turret_map[r][c].power += 1
        if cnt > 1:
            return True
        else:
            return False


N, M, K = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(N)]

game = War(N, M, input_map)

for k_iter in range(K):
    game.take_attack()
    can_keep_going = game.fix_turrets()
    if not can_keep_going:
        break

_, victim = game.select_attacker_and_victim(for_answer=True)
print(victim.power)