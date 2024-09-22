import heapq

DIRECTION = [[1, -1, 0], [2, 0, 1], [3, 1, 0], [4, 0, -1]]

class DistanceNodeSanta:
    def __init__(self, distance, direction):
        self.distance = distance
        self.direction = direction

    def __lt__(self, other):
        if self.distance < other.distance:
            return True
        elif self.distance > other.distance:
            return False

        if self.direction < other.distance:
            return True
        else:
            return False


class DistanceNodeRudolph:
    def __init__(self, dist, r, c, santa_idx):
        self.dist = dist
        self.r = r
        self.c = c
        self.santa_idx = santa_idx

    def __lt__(self, other):
        if self.dist < other.dist:
            return True
        elif self.dist > other.dist:
            return False

        if self.r > other.r:
            return True
        elif self.r < other.r:
            return False

        if self.c > other.c:
            return True
        else:
            return False


class Game:
    def __init__(self, map_size, info_of_rudolph, info_of_santa):
        class Rudolph:
            def __init__(self, r, c, power):
                self.r = r
                self.c = c
                self.power = power

        class Santa:
            def __init__(self, idx, r, c, power):
                self.idx = idx
                self.r = r
                self.c = c
                self.power = power
                self.reward = 0
                self.is_die = False
                self.is_stun = 0

        self.map_size = map_size
        self.rudolph = Rudolph(*info_of_rudolph)
        self.santas = [Santa(idx, *info) for idx, info in enumerate(info_of_santa)]

        self.loc_of_santas = set()
        self.loc_dict_of_santas = {}
        for santa in self.santas:
            self.loc_of_santas.add((santa.r, santa.c))
            self.loc_dict_of_santas[(santa.r, santa.c)] = santa.idx

    def solve(self, num_of_turns):
        answer = []
        for turn in range(num_of_turns):
            ret = 0
            ret += self.move(False)
            ret += self.move(True)
            answer.append(ret)

        return answer

    def interaction(self, target_santa, dx, dy, power):
        pushed_r, pushed_c = target_santa.r + power * dx, target_santa.c + power * dy

        if (pushed_r < 0 or pushed_r > self.map_size - 1) or (pushed_c < 0 or pushed_c > self.map_size - 1):
            # 얘 죽음
            target_santa.is_die = True
            del self.loc_dict_of_santas[(target_santa.r, target_santa.c)]
            self.loc_of_santas.discard((target_santa.r, target_santa.c))
            return

        if (pushed_r, pushed_c) not in self.loc_of_santas:
            # 정보 최신화
            # 날라온 산타가 원래 있던 위치 없애기
            del self.loc_dict_of_santas[(target_santa.r, target_santa.c)]
            self.loc_of_santas.discard((target_santa.r, target_santa.c))
            # 날라온 산타로 정보 대체
            self.loc_dict_of_santas[(pushed_r, pushed_c)] = target_santa.idx
            self.loc_of_santas.add((pushed_r, pushed_c))

            # 갈 곳에 아무도 없어요
            target_santa.r = pushed_r
            target_santa.c = pushed_c

            return

        pushed_loc = (pushed_r, pushed_c)
        interacted_santa = self.santas[self.loc_dict_of_santas[pushed_loc]]

        # 정보 최신화
        # 날라온 산타가 원래 있던 위치 없애기
        del self.loc_dict_of_santas[(target_santa.r, target_santa.c)]
        self.loc_of_santas.discard((target_santa.r, target_santa.c))
        # 날라온 산타로 정보 대체
        self.loc_dict_of_santas[(interacted_santa.r, interacted_santa.c)] = target_santa.idx
        self.loc_of_santas.add((interacted_santa.r, interacted_santa.c))

        # 일단 그 곳으로 날라온 산타를 이동시키고
        target_santa.r = pushed_r
        target_santa.c = pushed_c

        # 원래 있던 산타 옮기기
        self.interaction(interacted_santa, dx, dy, 1)

    def move(self, is_santa):
        if is_santa:
            reward = 0
            # 산타 움직이게 하기
            for santa in self.santas:
                if santa.is_die:
                    continue
                if santa.is_stun > 0:
                    santa.is_stun -= 1

                s_r, s_c = santa.r, santa.c
                r_r, r_c = self.rudolph.r, self.rudolph.c
                min_heap = []
                for dir, dx, dy in DIRECTION:
                    distance = (s_r + dx - r_r) ** 2 + (s_c + dy - r_c) ** 2
                    min_heap.append(DistanceNodeSanta(distance, dir))
                heapq.heapify(min_heap)

                target_dir = min_heap[0].direction

                if 0 <= min_heap[0].distance <= 2:
                    reverse_dir = target_dir + 2 if target_dir + 2 < 5 else target_dir -2
                    santa.reward += santa.power
                    self.interaction(santa, DIRECTION[reverse_dir][1], DIRECTION[reverse_dir][2], santa.power)

                    reward += santa.power
                else:
                    santa.reward += 1
                    reward += 1
            return reward
        else:
            # 루돌프 움직이기
            reward = 0
            min_heap = []

            # 목표로 하는 산타 찾기
            r, c = self.rudolph.r, self.rudolph.c
            santa_loc = set()
            santa_loc_dict = {}
            for santa in self.santas:
                santa_loc.add((santa.r, santa.c))
                santa_loc_dict[(santa.r, santa.c)] = santa.idx
                distance = (r - santa.r) ** 2 + (c - santa.c) ** 2
                min_heap.append(DistanceNodeRudolph(distance, santa.r, santa.c, santa.idx))
            self.loc_of_santas = santa_loc
            self.loc_dict_of_santas = santa_loc_dict

            heapq.heapify(min_heap)
            distance = min_heap[0].dist
            target_santa = self.santas[min_heap[0].santa_idx]

            # 해당 산타로 가기 위한 위치 정하기
            dx, dy = 0, 0
            if r > target_santa.r:
                if c == target_santa.c:
                    # 위로
                    dx, dy = -1, 0
                elif c < target_santa.c:
                    # 우측 상단 대각선
                    dx, dy = -1, +1
                elif c > target_santa.c:
                    # 좌측 상단 대각선
                    dx, dy = -1, -1
            elif r < target_santa.r:
                if c == target_santa.c:
                    # 아래로
                    dx, dy = +1, 0
                elif c < target_santa.c:
                    # 우측 하단 대각선
                    dx, dy = 1, 1
                elif c > target_santa.c:
                    # 좌측 하단 대각선
                    dx, dy = 1, -1
            else:
                if c == target_santa.c:
                    # 있을 수 없는 일
                    pass
                elif c < target_santa.c:
                    # 오른쪽
                    dx, dy = 0, 1
                elif c > target_santa.c:
                    # 왼쪽
                    dx, dy = 0, -1
                    pass

            self.rudolph.r, self.rudolph.c = self.rudolph.r + dx, self.rudolph.c + dy

            if 0 <= distance <= 2:
                # 산타와 충돌이 발생했다!
                target_santa.is_stun = 2
                target_santa.reward += 2
                self.interaction(target_santa, dx, dy, self.rudolph.power)
                reward += self.rudolph.power

            return reward
"""
N: 맵 크기
M: 게임 턴 수
P: 산타 수
C: 루돌프의 힘
D: 산타의 힘
"""
N, M, P, C, D = list(map(int, input().split()))
R_r, R_c = list(map(int, input().split()))
santa_information = []
for _ in range(P):
    S_n, S_r, S_c = list(map(int, input().split()))
    santa_information.append([S_r, S_c, D])

game = Game(map_size=N, info_of_rudolph=[R_r, R_c, C], info_of_santa=santa_information)
game.solve(M)

for s in game.santas:
    print(s.reward)
