from collections import deque
import heapq

RELIC_SIZE = 5
DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]


class RelicValue:
    # 첫 번째 단계에서, 최고 우선 순위의 유물을 찾기 위한 클래스
    def __init__(self, value, degree, x, y, points, rot_idx):
        """
        Args:
            value: 유물 개수
            degree: 돌린 각도
            x: 중점 행 좌표
            y: 중점 열 좌표
            points: 유물들 좌표
            rot_idx: 미리 만들어 놓은 회전 배열의 좌표
        """
        self.value = value
        self.degree = degree
        self.x = x
        self.y = y
        self.points = points
        self.rot_idx = rot_idx

    def __lt__(self, other):
        # 가치가 높을수록 우선 순위
        if self.value > other.value:
            return True
        elif self.value < other.value:
            return False

        # 가치가 같다면, 각도가 작을수록 우선 순위
        if self.degree < other.degree:
            return True
        elif self.degree > other.degree:
            return False

        # 각도가 같다면, 열이 작을수록 우선 순위
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False

        # 열이 같아면, 행이 작을수록 우선 순위
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False


class Location:
    # 유물을 발굴하고, 남은 공간에 집어 넣기 위한 우선순위 계산
    def __init__(self, x, y):
        """
        Args:
            x: 빈 곳의 행
            y: 빈 곳의 열
        """
        self.x = x
        self.y = y

    def __lt__(self, other):
        # 열이 작을수록 우선 순위
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False

        # 열이 같다면, 행이 클수록 우선 순위
        if self.x > other.x:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.x} - {self.y}"


def bfs_without_replace(loc, relic_map):
    """
    BFS를 수행할 때, 기존 유물 지도를 돌리는 것이 아닌, 이미 돌아간 좌표 정보를 활용하여 BFS 수행
    Args:
        loc: 이미 돌아간 좌표 정보 (5x5)
        relic_map: 기존 맵

    Returns:
        탐색을 통해 얻어낸 유물 개수
        유물들의 좌표
    """
    num_of_relics = 0

    is_visited = set()
    queue = deque()
    searched_points = []

    for i in range(RELIC_SIZE):
        for j in range(RELIC_SIZE):
            if (i, j) in is_visited:
                continue

            rot_x, rot_y = loc[i][j]

            is_visited.add((i, j))
            queue.append((i, j))
            temp_searched_points = [(i, j)]

            # 좌표만 돌아간 것을 참고한다.
            target_color = relic_map[rot_x][rot_y]
            cnt = 1

            while queue:
                x, y = queue.popleft()

                for dx, dy in DIRECTION:
                    temp_x, temp_y = x + dx, y + dy

                    if (-1 < temp_x < RELIC_SIZE) and (-1 < temp_y < RELIC_SIZE):
                        if (temp_x, temp_y) in is_visited:
                            continue

                        rot_x, rot_y = loc[temp_x][temp_y]

                        # 좌표만 돌아간 것을 참고한다.
                        if target_color == relic_map[rot_x][rot_y]:
                            is_visited.add((temp_x, temp_y))
                            queue.append((temp_x, temp_y))
                            temp_searched_points.append((temp_x, temp_y))
                            cnt += 1

            if cnt > 2:
                num_of_relics += cnt
                searched_points.extend(temp_searched_points)

    return num_of_relics, searched_points


def search_relic(rotated_locations, rot_info, relic_map):
    """
    모든 회전 경우의 수를 돌아보면서, 가장 큰 유물 조각을 가질 수 있을 때를 확인한다.
    Args:
        rotated_locations: 미리 회전 시킨 배열 정보
        rot_info: RelicValue 인스턴스를 만들기 위한 정보를 사전에 정의한 배열
        relic_map: 유물 정보

    Returns:
        우선 순위에 따라 구해진 가장 많은 유물 수, 바뀐 유물 정보, 발견한 유물 위치 정보
    """
    # 우선순위를 위해 heapq 사용
    min_heap = []
    for idx, loc in enumerate(rotated_locations):
        # 매 회전마다 BFS를 수행하여 얻어 낸 유물 개수 등의 정보
        num_of_relics, searched_points = bfs_without_replace(loc, relic_map)
        # 정보를 heap에 담기
        heapq.heappush(min_heap, RelicValue(num_of_relics, *rot_info[idx], searched_points, idx))

    # 최종적으로 맨 위에 그 정보가 담기게 됨
    result = heapq.heappop(min_heap)
    largest_search = result.points
    largest_nums = result.value
    largest_idx = result.rot_idx

    # 해당 회전 경우의 수로 일부분 회전
    temp_relic_map = [relic_map[i][:] for i in range(RELIC_SIZE)]
    for i in range(RELIC_SIZE):
        for j in range(RELIC_SIZE):
            rot_x, rot_y = rotated_locations[largest_idx][i][j]
            relic_map[i][j] = temp_relic_map[rot_x][rot_y]

    return largest_nums, relic_map, largest_search


def repeatedly_search(numbers_on_wall, cnt, relic_map, search_result):
    """
    문제에서 2-3단계 반복을 하는 부분으로,
        1. 이전에 찾은 유물을 벽에 적힌 번호로 대체하고
        2. 다시 BFS를 돌려 유물을 찾는다. (이 때 회전은 없다.)
    Args:
        numbers_on_wall: 벽에 적힌 번호 리스트
        cnt: 벽 번호 순서
        relic_map: 유물 정보
        search_result: 이전에 얻어 낸 유물 좌표들

    Returns:
        더 이상 유물을 찾을 수 없는 경우에 반환
            연쇄 과정을 통해 구해진 유물의 개수 총 합
            유물 정보
            벽 순서
    """
    ret = 0
    loc = [[(x, y) for y in range(RELIC_SIZE)] for x in range(RELIC_SIZE)]
    while True:
        # 우선, 유물 발굴로 인해 남은 공간을 채운다. -> 우선 순위를 따져 진행한다.
        min_heap = []
        for x, y in search_result:
            heapq.heappush(min_heap, Location(x, y))

        # 채우는 과정...
        while min_heap:
            item = heapq.heappop(min_heap)
            x, y = item.x, item.y
            relic_map[x][y] = numbers_on_wall[cnt]
            cnt += 1  # 벽에 적힌 순서를 따라가도록 하나 씩 증가

        # 회전이 없음
        num_of_relics, search_result = bfs_without_replace(loc, relic_map)

        # 유물을 발견할 수 없다! break
        if num_of_relics == 0:
            break

        ret += num_of_relics

    return ret, relic_map, cnt


# 미리 배열을 회전한 정보를 저장해 놓자.
original_loc = [[(x, y) for y in range(RELIC_SIZE)] for x in range(RELIC_SIZE)]
rotated_loc = []
rotation_info = []
for y in range(RELIC_SIZE - 2, 0, -1):
    for x in range(RELIC_SIZE - 2, 0, -1):
        new_loc = [original_loc[i][:] for i in range(RELIC_SIZE)]
        # 일부분을 가져와 돌린다.
        partial = [row[y - 1:y + 2] for row in new_loc[x - 1:x + 2]]

        for rot in range(1, 5):
            # 4번 돌리면 원위치가 되기 때문에, 4번 회전한다.
            partial = list(map(list, zip(*partial)))[::-1]

            for _x in range(x - 1, x + 2):
                for _y in range(y - 1, y + 2):
                    new_loc[_x][_y] = partial[_x - (x - 1)][_y - (y - 1)]

            if rot < 4:
                rotated_loc.append([new_loc[i][:] for i in range(RELIC_SIZE)])
                # 우선 순위를 표현하기 위해 각도는 -1을 곱한다.
                rotation_info.append((rot * -1, x, y))

K, M = list(map(int, input().split()))
input_relic = [list(map(int, input().split())) for _ in range(RELIC_SIZE)]
input_numbers = list(map(int, input().split()))

wall_count = 0
answer_list = []
for k_iter in range(K):
    answer = 0

    # 1. 탐사 진행) 중심점을 잡고 회전시키면서 유물을 탐색한다.
    ret1, input_relic, searched_loc = search_relic(rotated_loc, rotation_info, input_relic)
    answer += ret1

    # 2. 반복하면서, 유물을 찾자!
    ret2, input_relic, wall_count = repeatedly_search(input_numbers, wall_count, input_relic, searched_loc)
    answer += ret2

    if answer == 0:
        break
    answer_list.append(answer)

for item in answer_list:
    print(item, end=" ")
print()
