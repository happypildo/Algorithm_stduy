import heapq

DIRECTION = [
    [-1, 0, 1], [1, 0, 1], [0, -1, 2], [0, 1, 2]
]   # 마지막 인덱스는 우선순위 부여 위함
ROTATION = [
    [-1, -1], [-1, 0], [0, -1], [0, 0]
]

class MovePriorityNode:
    def __init__(self, direction, distance, priority):
        self.direction = direction
        self.distance = distance
        self.priority = priority

    def __lt__(self, other):
        if self.distance < other.distance:
            return True
        elif self.distance > other.distance:
            return False
        if self.priority < other.priority:
            return True
        else:
            return False


class RotatePriorityNode:
    def __init__(self, size, ul_r, ul_c):
        self.ul_r = ul_r
        self.ul_c = ul_c
        self.size = size

    def __lt__(self, other):
        if self.size > other.size:
            return True
        elif self.size < other.size:
            return False
        if self.ul_r < other.ul_r:
            return True
        elif self.ul_r > other.ul_r:
            return False
        if self.ul_c < other.ul_c:
            return True
        else:
            return False


class Person:
    def __init__(self, r, c):
        self.r = r
        self.c = c

        self.is_exited = False
        self.travel_dist = 0

    def get_best_effort(self):
        pass


class Game:
    def __init__(self, game_size, num_of_people, game_map, people_loc, exit_loc):
        self.game_size = game_size
        self.num_of_people = num_of_people

        self.game_map = game_map
        self.people = [Person(r - 1, c - 1) for r, c in people_loc]
        self.exit_location = (exit_loc[0] - 1, exit_loc[1] - 1)

    def __str__(self):
        print("---------------------")
        for line in self.game_map:
            print(line)
        for person in self.people:
            print("P: ", person.r, person.c)
        print("E: ", self.exit_location)
        print()
        return "\n"

    def get_distance_p2e(self, r, c):
        if (-1 < r < self.game_size) and (-1 < c < self.game_size):
            if self.game_map[r][c] == 0:
                return abs(self.exit_location[0] - r) + abs(self.exit_location[1] - c)
            else:
                return float('inf')
        return float('inf')

    def move_people(self):
        for person in self.people:
            if person.is_exited:
                continue

            prev_dist = self.get_distance_p2e(person.r, person.c)
            min_heap = []
            for idx, (dr, dc, prio) in enumerate(DIRECTION):
                temp_r, temp_c = person.r + dr, person.c + dc

                dist = self.get_distance_p2e(temp_r, temp_c)
                dist = dist if dist < prev_dist else float('inf')

                min_heap.append(MovePriorityNode(idx, dist, prio))
            heapq.heapify(min_heap)

            direction, distance = min_heap[0].direction, min_heap[0].distance
            if distance == float('inf'):
                # 움직이지 않는다.
                continue
            else:
                dr, dc, _ = DIRECTION[direction]
                temp_r, temp_c = person.r + dr, person.c + dc

                person.travel_dist += 1
                person.r = temp_r
                person.c = temp_c

                if (temp_r, temp_c) == self.exit_location:
                    person.is_exited = True

    def find_square(self):
        for size in range(1, self.game_size + 1):
            for i in range(self.game_size):
                for j in range(self.game_size):
                    upper_left_r, upper_left_c = i, j

                    if (-1 < upper_left_r + size < self.game_size) and (-1 < upper_left_c + size < self.game_size):
                        if (upper_left_r <= self.exit_location[0] <= upper_left_r + size) and (
                                    upper_left_c <= self.exit_location[1] <= upper_left_c + size):
                            included_people = []
                            for person in self.people:
                                if person.is_exited:
                                    continue
                                if (upper_left_r <= person.r <= upper_left_r + size) and (
                                        upper_left_c <= person.c <= upper_left_c + size):
                                    included_people.append(person)
                            if len(included_people) > 0:
                                return upper_left_r, upper_left_c, size, included_people

    def rotate_map(self):
        ul_r, ul_c, size, included_people = self.find_square()

        temp_game_map = [self.game_map[i][:] for i in range(self.game_size)]

        # mapping
        mapping_dict = {}
        for person in included_people:
            key = (person.r, person.c)
            if mapping_dict.get(key, None) is None:
                mapping_dict[key] = [person]
            else:
                mapping_dict[key].append(person)
        for r, c in mapping_dict.keys():
            temp_game_map[r][c] = mapping_dict[(r, c)]
        temp_game_map[self.exit_location[0]][self.exit_location[1]] = -1

        # Rotate
        partial_map = [temp_game_map[i][ul_c:ul_c+size + 1] for i in range(ul_r, ul_r + size + 1)]
        partial_map = list(map(list, zip(*partial_map[::-1])))

        # interest point
        for i in range(size + 1):
            for j in range(size + 1):
                if partial_map[i][j] == -1:
                    # New exit
                    self.exit_location = (i + ul_r, j + ul_c)
                    partial_map[i][j] = 0
                elif isinstance(partial_map[i][j], list):
                    for person in partial_map[i][j]:
                        person.r = i + ul_r
                        person.c = j + ul_c
                    partial_map[i][j] = 0
                elif partial_map[i][j] > 0:
                    partial_map[i][j] -= 1

                self.game_map[i + ul_r][j + ul_c] = partial_map[i][j]

    def can_keep_going(self):
        for person in self.people:
            if not person.is_exited:
                return True
        return False


N, M, K = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(N)]
input_people_loc = [list(map(int, input().split())) for _ in range(M)]
input_exit_loc = list(map(int, input().split()))

game = Game(N, M, input_map, input_people_loc, input_exit_loc)

for k_iter in range(K):
    game.move_people()
    if not game.can_keep_going():
        break
    game.rotate_map()

answer = 0
for p in game.people:
    answer += p.travel_dist
print(answer)
print(game.exit_location[0] + 1, game.exit_location[1] + 1)