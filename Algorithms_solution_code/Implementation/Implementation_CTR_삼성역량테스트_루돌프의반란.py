import heapq

DIRECTION = [[1, -1, 0], [2, 0, 1], [3, 1, 0], [4, 0, -1]]


class DistanceNodeSanta:
    def __init__(self, distance, direction, curr_distance):
        """
        산타가 이동할 때, 우선 순위 계산을 위한 클래스
        Args:
            distance: 루돌프까지의 거리
            direction: 해당 거리 계산 시 사용된 방향 (우선 순위를 위해 상우하좌를 각각 1~4로 인덱싱 함)
            curr_distance: 움직이지 않을 떄의 거리 (조건 중 거리가 멀어지는 방향으로 가지 않아야 함이 있음)
        """
        self.distance = distance
        self.direction = direction
        self.curr_distance = curr_distance

    def __lt__(self, other):
        # 거리가 짧을 수록 이득
        if self.distance < other.distance:
            return True
        elif self.distance > other.distance:
            return False

        # 거리가 같다면, 방향 우선순위
        if self.direction < other.direction:
            return True
        else:
            return False


class DistanceNodeRudolph:
    def __init__(self, dist, r, c, santa_idx):
        """
        루돌프가 방향을 정할 때, 우선순위를 위해 사용하는 클래스
        Args:
            dist: 루돌프에서 산타까지의 거리
            r: 산타의 열 번호
            c: 산타의 행 번호
            santa_idx: 산타 번호
        """
        self.dist = dist
        self.r = r
        self.c = c
        self.santa_idx = santa_idx

    def __lt__(self, other):
        # 가장 거리가 가까운 산타를 선택한다.
        if self.dist < other.dist:
            return True
        elif self.dist > other.dist:
            return False

        # 거리가 동일할 경우, 열 번호가 가장 큰 산타를 선택
        if self.r > other.r:
            return True
        elif self.r < other.r:
            return False

        # 열 번호가 같다면, 행 번호가 가장 큰 산타를 선택
        if self.c > other.c:
            return True
        else:
            return False


class Game:
    def __init__(self, map_size, info_of_rudolph, info_of_santa):
        """
        루돌프의 반란 게임을 푸는 클래스
        Args:
            map_size: 맵 크기
            info_of_rudolph: 루돌프의 정보
            info_of_santa: 산타의 정보
        """
        class Rudolph:
            def __init__(self, r, c, power):
                """
                루돌프 클래스
                Args:
                    r: 루돌프 열 위치
                    c: 루돌프 행 위치
                    power: 루돌프 파워
                """
                self.r = r
                self.c = c
                self.power = power

        class Santa:
            def __init__(self, idx, r, c, power):
                """

                Args:
                    idx: 산타 번호
                    r: 산타 열 위치
                    c: 산타 행 위치
                    power: 산타 파워
                """
                self.idx = idx
                self.r = r
                self.c = c
                self.power = power

                """
                reward: 해당 산타가 게임동안 얻게 되는 점수
                is_die: 산타가 죽었는지 살았는지에 대한 변수 (True면 죽음)
                is_stun: 산타가 기절했는지 아닌지에 대한 변수 (양수면 기절)
                """
                self.reward = 0
                self.is_die = False
                self.is_stun = 0

        self.map_size = map_size
        self.rudolph = Rudolph(*info_of_rudolph)
        self.santas = [Santa(idx, *info) for idx, info in enumerate(info_of_santa)]

    def solve(self, num_of_turns):
        """
        문제 풀기 함수
        Args:
            num_of_turns: 게임 턴 수

        """
        for turn in range(num_of_turns):
            # 루돌프를 먼저 움직인다.
            self.move(False)
            # 그 다음 산타를 움직인다.
            self.move(True)

            # 게임이 끝났는지 여부를 판단하는 변수
            is_done = True
            for santa in self.santas:
                is_done = False
                # 생존 점수 추가
                santa.reward += 0 if santa.is_die else 1
            if is_done:
                break

    def interaction(self, target_santa, dx, dy, power):
        """
        산타 튕기기 상호작용 함수, 재귀적으로 동작한다.
        Args:
            target_santa: 날라간 산타
            dx: 산타의 날라가는 방향 (열 방향)
            dy: 산타의 날라가는 방향 (행 방향)
            power: 어떤 파워로 날라가는지

        """

        # 날라 갔을 때의 위치 좌표, power만큼 곱해져 날라간다.
        pushed_r, pushed_c = target_santa.r + power * dx, target_santa.c + power * dy

        # 만약 맵 범위를 넘는다면, 산타를 죽인다.
        if (pushed_r < 0 or pushed_r > self.map_size - 1) or (pushed_c < 0 or pushed_c > self.map_size - 1):
            target_santa.is_die = True
            return

        # 산타가 날라간 위치에 산타가 있는지(is_there)와 있다면 그 녀석의 인덱스(interacted_santa_idx)를 가져온다.
        is_there, interacted_santa_idx = self.is_there_santa(target_santa.idx, pushed_r, pushed_c)
        if not is_there:
            # 갈 곳에 아무도 없어요
            target_santa.r = pushed_r
            target_santa.c = pushed_c
            return

        interacted_santa = self.santas[interacted_santa_idx]

        # 일단 그 곳으로 날라온 산타를 이동시키고
        target_santa.r = pushed_r
        target_santa.c = pushed_c

        # 원래 있던 산타 옮기기 -> 파워는 1이 된다.
        self.interaction(interacted_santa, dx, dy, 1)

    def is_there_santa(self, own_idx, r, c):
        """
        (r, c)에 산타가 존재하는지 여부를 확인한다.
        Args:
            own_idx: 제외할 산타의 인덱스
            r: 열
            c: 행

        Returns:
            (True or False) / 산타의 인덱스
        """
        for santa in self.santas:
            if santa.idx == own_idx:
                continue
            else:
                if r == santa.r and c == santa.c and not santa.is_die:
                    # 살아있는 산타가 있을 경우 리턴
                    return True, santa.idx
        return False, None

    def move(self, is_santa):
        """
        산타 또는 루돌프를 옮기는 함수
        Args:
            is_santa: 산타를 옮긴다면 True, 루돌프라면 False
        """
        if is_santa:
            # 산타 움직이게 하기
            for santa in self.santas:
                # 죽은 산타는 움직이지 안는다.
                if santa.is_die:
                    continue
                # is_stun 값이 0이 아니라면, 기절해 있는 산타다.
                if santa.is_stun > 0:
                    santa.is_stun -= 1
                    continue

                # 산타 좌표와, 루돌프 좌표
                s_r, s_c = santa.r, santa.c
                r_r, r_c = self.rudolph.r, self.rudolph.c

                # 어떤 방향으로 나아갈 지 결정하기 위해, 우선순위 큐를 사용한다.
                min_heap = []
                for dir, dx, dy in DIRECTION:
                    # 움직이지 않을 경우의 위치
                    curr_distance = (s_r - r_r) ** 2 + (s_c - r_c) ** 2
                    # dir 방향으로 움직였을 경우의 위치
                    distance = (s_r + dx - r_r) ** 2 + (s_c + dy - r_c) ** 2
                    # 나아간 곳에 산타가 있는지 여부 판단
                    is_there, _ = self.is_there_santa(santa.idx, s_r + dx, s_c + dy)
                    # 산타가 있거나, 맵 밖으로 나가게 된다면, 거리를 무한대로 취급한다.
                    if is_there or ((0 > s_r + dx or self.map_size - 1 < s_r + dx) or (0 > s_c + dy or self.map_size - 1 < s_c + dy)):
                        distance = float('inf')

                    min_heap.append(DistanceNodeSanta(distance, dir, curr_distance))
                heapq.heapify(min_heap)

                # 우선 순위에 따라 방향을 결정한다.
                target_dir = min_heap[0].direction
                temp_r, temp_c = santa.r + DIRECTION[target_dir - 1][1], santa.c + DIRECTION[target_dir - 1][2]

                if min_heap[0].distance > min_heap[0].curr_distance:
                    # 만약, 해당 방향으로 가는 것이 더 먼 길이라면 가지 않는다.
                    pass
                elif self.rudolph.r == temp_r and self.rudolph.c == temp_c:
                    # 해당 위치에 루돌프가 있다면, 기절시키고 날린다.
                    santa.is_stun = 1

                    santa.r, santa.c = temp_r, temp_c

                    # 방향 전환
                    reverse_dir = target_dir + 2 if target_dir + 2 < 5 else target_dir - 2
                    santa.reward += santa.power

                    # 상호작용 시작
                    self.interaction(santa, DIRECTION[reverse_dir - 1][1], DIRECTION[reverse_dir - 1][2], santa.power)
                else:
                    # 날라간 곳에 아무 것도 없으면, 날라간다.
                    santa.r, santa.c = temp_r, temp_c
        else:
            # 루돌프 움직이기
            min_heap = []

            # 목표로 하는 산타 찾기
            r, c = self.rudolph.r, self.rudolph.c
            for santa in self.santas:
                distance = float('inf') if santa.is_die else (r - santa.r) ** 2 + (c - santa.c) ** 2
                min_heap.append(DistanceNodeRudolph(distance, santa.r, santa.c, santa.idx))

            # 우선순위에 따라 산타를 결정한다.
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

            # 루돌프를 그 곳으로 옮긴다.
            self.rudolph.r, self.rudolph.c = self.rudolph.r + dx, self.rudolph.c + dy
            is_there, _ = self.is_there_santa(-1, self.rudolph.r, self.rudolph.c)
            if is_there:
                # 산타와 충돌이 발생한다. 기절시키고 상호작용한다.
                target_santa.is_stun = 2
                target_santa.reward += self.rudolph.power
                self.interaction(target_santa, dx, dy, self.rudolph.power)


"""
N: 맵 크기
M: 게임 턴 수
P: 산타 수
C: 루돌프의 힘
D: 산타의 힘
"""
N, M, P, C, D = list(map(int, input().split()))
R_r, R_c = list(map(int, input().split()))
santa_information = [None for _ in range(P)]
for _ in range(P):
    S_n, S_r, S_c = list(map(int, input().split()))
    santa_information[S_n - 1] = [S_r - 1, S_c - 1, D]

game = Game(map_size=N, info_of_rudolph=[R_r - 1, R_c - 1, C], info_of_santa=santa_information)
game.solve(M)

for s in game.santas:
    print(s.reward, end=" ")
