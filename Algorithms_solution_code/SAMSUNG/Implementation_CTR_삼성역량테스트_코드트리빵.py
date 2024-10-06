from collections import deque
import heapq

DIRECTION = [
    [-1, 0], [0, -1], [0, 1], [1, 0]
]


class Priority:
    def __init__(self, dist, x, y, bc):
        self.dist = dist
        self.x = x
        self.y = y
        self.bc = bc

    def __lt__(self, other):
        if self.dist < other.dist:
            return True
        elif self.dist > other.dist:
            return False
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        if self.y < other.y:
            return True
        else:
            return False


class Person:
    def __init__(self, target_conv, curr_point=None):
        self.curr_point = curr_point
        self.target_conv = target_conv
        self.is_activated = False
        self.is_arrived = False


class BaseCamp:
    def __init__(self, loc):
        self.loc = loc
        self.is_occupied = False


class BreadShop:
    def __init__(self, N, num_of_people, conv_map, target_convs):
        self.N = N
        self.num_of_people = num_of_people
        self.people = [Person((conv[0] - 1, conv[1] - 1)) for conv in target_convs]
        self.conv_map = conv_map

        self.all_loc = []
        self.base_camps = []
        for i in range(self.N):
            for j in range(self.N):
                if self.conv_map[i][j] == 1:
                    self.base_camps.append(BaseCamp((i, j)))

    def bfs_for_shortest(self, p_idx=None, temp_person=None):
        if temp_person is None:
            person = self.people[p_idx]
        else:
            person = temp_person
        point = person.curr_point

        queue = deque([point])
        prev_nodes = {point: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == person.target_conv:
                break

            for dx, dy in DIRECTION:
                temp_x, temp_y = x + dx, y + dy

                if (-1 < temp_x < self.N) and (-1 < temp_y < self.N):
                    if self.conv_map[temp_x][temp_y] == -1 or (temp_x, temp_y) in prev_nodes:
                        continue

                    queue.append((temp_x, temp_y))
                    prev_nodes[(temp_x, temp_y)] = (x, y)

        path = []
        shortest_node = None
        curr_node = person.target_conv
        if curr_node not in prev_nodes:
            return None, None

        while curr_node is not None:
            if prev_nodes[curr_node] == person.curr_point:
                shortest_node = curr_node
            path.append(curr_node)
            curr_node = prev_nodes[curr_node]

        return shortest_node, path

    def move(self, p_idx):
        person = self.people[p_idx]
        target_conv = person.target_conv

        shortest_node, _ = self.bfs_for_shortest(p_idx)
        person.curr_point = shortest_node

        if person.curr_point == target_conv:
            # 그 사람을 움직이지 못하게 한다.
            person.is_arrived = True
            # 편의점을 못 지나가게 하는 것은 모든 사람의 move가 끝난 이후
            return True
        return False

    def select_basecamp(self, p_idx):
        min_heap = []
        for bc in self.base_camps:
            if bc.is_occupied:
                continue
            target_conv = self.people[p_idx].target_conv
            _, path = self.bfs_for_shortest(temp_person=Person(target_conv=target_conv, curr_point=tuple(bc.loc)))
            if path is None:
                continue

            min_heap.append(Priority(len(path), *bc.loc, bc))
        heapq.heapify(min_heap)

        bc = min_heap[0].bc
        bc.is_occupied = True
        self.people[p_idx].curr_point = tuple(bc.loc)
        self.conv_map[bc.loc[0]][bc.loc[1]] = -1

    def start(self):
        tik = 1
        while True:
            if tik - 1 < self.num_of_people:
                self.people[tik - 1].is_activated = True

            p_range = min(self.num_of_people, tik - 1)
            move_result = []
            for p_idx in range(p_range):
                if self.people[p_idx].is_arrived:
                    move_result.append(False)
                    continue
                move_result.append(self.move(p_idx))

            result = []
            for person in self.people:
                result.append(person.is_arrived)
            if sum(result) == self.num_of_people:
                break

            for idx, result in enumerate(move_result):
                if result:
                    c_x, c_y = self.people[idx].target_conv
                    self.conv_map[c_x][c_y] = -1

            if tik - 1 < self.num_of_people:
                self.select_basecamp(tik - 1)

            tik += 1

        return tik


n, m = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(n)]
convs = [list(map(int, input().split())) for _ in range(m)]

bs = BreadShop(n, len(convs), input_map, convs)
print(bs.start())