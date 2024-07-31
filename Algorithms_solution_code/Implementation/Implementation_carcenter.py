from collections import deque


class Person:
    def __init__(self, k, tk):
        self.idx = k
        self.arrival_time = tk
        self.processing_time_a = float('INF')
        self.processing_time_b = float('INF')
        self.number_a = float('INF')
        self.number_b = float('INF')


class CounterA:
    def __init__(self, i, ai):
        self.idx = i
        self.processing_time = ai
        self.waiting_queue = 0
        self.waiting_person_idx = -1


class CounterB:
    def __init__(self, j, bj):
        self.idx = j
        self.processing_time = bj
        self.waiting_queue = 0
        self.waiting_person_idx = -1


class CarCenter:
    def __init__(self, N, M, K, A, B, processing_times_A, processing_times_B, tk):
        self.num_of_counter_A = N
        self.num_of_counter_B = M
        self.num_of_people = K
        self.lost_person_A = A
        self.lost_person_B = B

        self.counterA = []
        self.counterB = []
        self.people = []
        self.waiting_in_first = {}
        self.waiting_in_second = {}

        self.simulation_tik = 0

        for i in range(self.num_of_counter_A):
            self.counterA.append(CounterA(i, processing_times_A[i]))
        for j in range(self.num_of_counter_B):
            self.counterB.append(CounterB(j, processing_times_B[j]))
        for k in range(self.num_of_people):
            self.people.append(Person(k, tk[k]))

            key = tk[k]
            value = self.waiting_in_first.get(key, None)
            if value is not None:
                self.waiting_in_first[key].append(k)
            else:
                self.waiting_in_first[key] = [k]

    def tik(self):
        # 기다리는 사람들 중 갈 수 있는 사람 모으기
        if self.simulation_tik == 7:
            print()
        can_go_people = []
        for key in sorted(self.waiting_in_first.keys()):
            if key <= self.simulation_tik:
                for k_idx in self.waiting_in_first[key]:
                    if self.people[k_idx].number_a == float('inf'):
                        can_go_people.append(k_idx)           # 빨리 도착한 사람이 앞에 있음.

        # A 창구에서 끝난 사람들 정리
        for c_a in self.counterA:
            if c_a.waiting_queue == 0 and c_a.waiting_person_idx != -1:
                key = self.simulation_tik
                value = self.waiting_in_second.get(key, None)
                if value is None:
                    self.waiting_in_second[key] = [c_a.waiting_person_idx]
                else:
                    self.waiting_in_second[key].append(c_a.waiting_person_idx)

        # 모은 사람들 중 창구로 보낼 수 있으면 보내기
        for p_idx in can_go_people:             # 우선순위 1. 먼저 온 사람
            for c_a in self.counterA:           # 우선순위 2. 카운터 인덱스가 빠른 것
                if c_a.waiting_queue == 0:
                    c_a.waiting_queue = c_a.processing_time
                    c_a.waiting_person_idx = p_idx
                    self.people[p_idx].number_a = c_a.idx
                    self.people[p_idx].processing_time_a = c_a.processing_time

        # A 창구에서 끝난 사람들 모으기
        can_go_people = []
        for key in sorted(self.waiting_in_second.keys()):         # 일찍 도착한 사람부터...
            for k_idx in self.waiting_in_second[key]:             # a 카운터 인덱스가 빠른 순서 (정리하면서 순서대로 들어감)
                if self.people[k_idx].number_b == float('inf'):
                    can_go_people.append(k_idx)

        # 모은 사람들 중 창구로 보낼 수 있으면 보내기
        for p_idx in can_go_people:
            for c_b in self.counterB:
                if c_b.waiting_queue == 0:
                    c_b.waiting_queue = c_b.processing_time
                    c_b.waiting_person_idx = p_idx
                    self.people[p_idx].number_b = c_b.idx
                    self.people[p_idx].processing_time_b = c_b.processing_time

    def simulation_start(self):
        while True:
            self.tik()

            # 대기 시간 지우기
            for c_a in self.counterA:
                if c_a.waiting_person_idx != -1:
                    c_a.waiting_queue = c_a.waiting_queue - 1
                    p_idx = c_a.waiting_person_idx
                    self.people[p_idx].processing_time_a = c_a.waiting_queue
            for c_b in self.counterB:
                if c_b.waiting_person_idx != -1:
                    c_b.waiting_queue = c_b.waiting_queue - 1
                    p_idx = c_b.waiting_person_idx
                    self.people[p_idx].processing_time_b = c_b.waiting_queue

            self.simulation_tik += 1
            # 딕셔너리 관리
            temp_dict_a = {}
            for key in sorted(self.waiting_in_first.keys()):
                people_idxs = []
                for k_idx in self.waiting_in_first[key]:
                    if self.people[k_idx].number_a == float('inf') and self.people[k_idx].number_b == float('inf'):
                        people_idxs.append(k_idx)
                if len(people_idxs) > 0:
                    temp_dict_a[key] = people_idxs[:]
            self.waiting_in_first = temp_dict_a

            temp_dict_b = {}
            for key in sorted(self.waiting_in_second.keys()):
                people_idxs = []
                for k_idx in self.waiting_in_second[key]:
                    if self.people[k_idx].number_a != float('inf') and self.people[k_idx].number_b == float('inf'):
                        people_idxs.append(k_idx)
                if len(people_idxs) > 0:
                    temp_dict_b[key] = people_idxs[:]
            self.waiting_in_second = temp_dict_b

            if self.waiting_in_first == {} and self.waiting_in_second == {}:
                return

    def check_lost_person(self):
        dup_cnt = 0
        for person in self.people:
            print(person.number_a, person.number_b)
            if person.number_a == self.lost_person_A - 1 and person.number_b == self.lost_person_B - 1:
                dup_cnt += person.idx + 1

        return dup_cnt


T = int(input())
for t_iter in range(1, T+1):
    N, M, K, A, B = list(map(int, input().split()))
    As = list(map(int, input().split()))
    Bs = list(map(int, input().split()))
    ts = list(map(int, input().split()))

    center = CarCenter(N, M, K, A, B, As, Bs, ts)
    center.simulation_start()
    print(center.check_lost_person())