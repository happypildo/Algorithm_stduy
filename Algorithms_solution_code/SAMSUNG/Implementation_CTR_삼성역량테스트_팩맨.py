from itertools import product
import heapq

MAP_SIZE = 4
MONSTER_DIRECTION = [
    [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]
] # 반시계 순
PACK_DIRECTION = [
    [-1, 0], [0, -1], [1, 0], [0, 1]
] # 우선순위 수


class Monster:
    def __init__(self, x, y, d):
        self.x = x - 1
        self.y = y - 1
        self.d = d - 1

        # 2는 살아 있음, 1과 0은 시체인 동안, -1일 경우 맵 상에 존재하지 않음
        self.is_dead = 2


class Packman:
    class PathPriority:
        def __init__(self, directions, monsters):
            self.directions = directions
            self.monsters = monsters

        def __lt__(self, other):
            if self.monsters > other.monsters:
                return True
            elif self.monsters < other.monsters:
                return False
            for d1, d2 in zip(self.directions, other.directions):
                if d1 < d2:
                    return True
                elif d1 > d2:
                    return False
            return False

    def __init__(self, x, y):
        self.x = x - 1
        self.y = y - 1

    def move(self, game_map):
        max_values = (-1, 5, 5, 5)    # 몬스터 수, 방향 각도
        for prod in product([0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]):
            is_possible = True

            temp_x, temp_y = self.x, self.y
            caught_monsters = set()
            for direction in prod:
                dx, dy = PACK_DIRECTION[direction]
                temp_x, temp_y = temp_x + dx, temp_y + dy

                if (-1 < temp_x < MAP_SIZE) and (-1 < temp_y < MAP_SIZE):
                    caught_monsters = caught_monsters | set(game_map[temp_x][temp_y][0])
                else:
                    is_possible = False
                    break

            if is_possible:
                if len(caught_monsters) > max_values[0]:
                    max_values = (len(caught_monsters), prod[0], prod[1], prod[2])
                    continue
                elif len(caught_monsters) < max_values[0]:
                    continue
                for d1, d2 in zip(prod, max_values[1:]):
                    if d1 < d2:
                        max_values = (len(caught_monsters), prod[0], prod[1], prod[2])
                        break
                    elif d1 > d2:
                        break

        caught_monsters = set()
        moving_history = []
        for direction in max_values[1:]:
            dx, dy = PACK_DIRECTION[direction]

            self.x, self.y = self.x + dx, self.y + dy
            moving_history.append((self.x, self.y))
            caught_monsters = caught_monsters | set(game_map[self.x][self.y][0])

        return moving_history, caught_monsters


class Game:
    def __init__(self, num_of_turns, pack, mon):
        self.num_of_turns = num_of_turns
        self.packman = Packman(*pack)
        self.monsters = [Monster(*m) for m in mon]

        # 0번째는 살아 있는, 첫번째는 시체
        self.game_map = [
            [
                [[], 0] for _ in range(MAP_SIZE)
            ] for _ in range(MAP_SIZE)
        ]
        for m in self.monsters:
            self.game_map[m.x][m.y][0].append(m)

    def play(self):
        for tik in range(self.num_of_turns):
            # 몬스터 복제 시도 & 몬스터 이동
            new_game_map = [[[] for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
            newly_born = []
            for i in range(MAP_SIZE):
                for j in range(MAP_SIZE):
                    for monster in self.game_map[i][j][0]:
                        # 복제 기릿
                        newly_born.append(Monster(monster.x + 1, monster.y + 1, monster.d + 1))

                        # 이동 기릿
                        cnt = 0
                        while True:
                            temp_x = monster.x + MONSTER_DIRECTION[monster.d][0]
                            temp_y = monster.y + MONSTER_DIRECTION[monster.d][1]

                            if (-1 < temp_x < MAP_SIZE) and (-1 < temp_y < MAP_SIZE):
                                if self.game_map[temp_x][temp_y][1] == 0 and ((temp_x, temp_y) != (self.packman.x, self.packman.y)):
                                    # 이동 가능
                                    monster.x, monster.y = temp_x, temp_y
                                    new_game_map[temp_x][temp_y].append(monster)
                                    break
                            monster.d += 1
                            if monster.d == 8:
                                monster.d = 0

                            cnt += 1
                            if cnt == 8:
                                new_game_map[monster.x][monster.y].append(monster)
                                break

            for i in range(MAP_SIZE):
                for j in range(MAP_SIZE):
                    self.game_map[i][j][0] = new_game_map[i][j]

            # 팩맨 이동
            moving_loc, to_be_body_monsters = self.packman.move(self.game_map)

            # 몬스터 시체 생성 및 소멸
            for i, j in moving_loc:
                if len(self.game_map[i][j][0]) != 0:
                    self.game_map[i][j][1] = 3
                self.game_map[i][j][0] = []

            for i in range(MAP_SIZE):
                for j in range(MAP_SIZE):
                    if self.game_map[i][j][1] > 0:
                        self.game_map[i][j][1] -= 1

            # 복제 완성
            for mon in newly_born:
                i, j = mon.x, mon.y
                self.game_map[i][j][0].append(mon)


m, t = list(map(int, input().split()))
p = list(map(int, input().split()))
ms = [list(map(int, input().split())) for _ in range(m)]

game = Game(t, p, ms)
game.play()

answer = 0
for i in range(MAP_SIZE):
    for j in range(MAP_SIZE):
        answer += len(game.game_map[i][j][0])
print(answer)