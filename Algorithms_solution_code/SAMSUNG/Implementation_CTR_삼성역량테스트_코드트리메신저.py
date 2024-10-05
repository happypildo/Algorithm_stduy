class ChatRoom:
    def __init__(self, parent_id, authority):
        self.parent_id = parent_id
        self.authority = authority
        self.is_on = True
        self.left_child = None
        self.right_child = None


class Samsung:
    def __init__(self, num_of_chats):
        # 맨 처음 채팅방은 최상위 채팅방
        self.num_of_chats = num_of_chats
        self.chat_rooms = [ChatRoom(-1, -1) for _ in range(num_of_chats + 1)]
        self.alarm_dict = {}

    def initialize(self, p_ids, powers):
        for c_id, p_id, power in zip(range(1, self.num_of_chats + 1), p_ids, powers):
            self.chat_rooms[c_id].parent_id = p_id
            self.chat_rooms[c_id].authority = power
            if self.chat_rooms[p_id].left_child is None:
                self.chat_rooms[p_id].left_child = c_id
            else:
                self.chat_rooms[p_id].right_child = c_id

    def reset_upper_dict(self, c_id):
        while c_id != -1:
            for depth in range(1, 22):
                if self.alarm_dict.get((c_id, depth), None) is not None:
                    del self.alarm_dict[(c_id, depth)]
                else:
                    continue
            c_id = self.chat_rooms[c_id].parent_id
        print("", end="")

    def toggle(self, c_id):
        self.chat_rooms[c_id].is_on = False if self.chat_rooms[c_id].is_on else True

        # self.reset_upper_dict(self.chat_rooms[c_id].parent_id)
        self.reset_upper_dict(c_id)

    def change_authority(self, c_id, power):
        self.chat_rooms[c_id].authority = power

        # self.alarm_dict = {}
        self.reset_upper_dict(c_id)

    def change_parents(self, c1, c2):
        # 해당 노드의 부모의 자식 키 바꾸기
        p_c1 = self.chat_rooms[c1].parent_id
        p_c2 = self.chat_rooms[c2].parent_id

        if self.chat_rooms[p_c1].left_child == c1:
            self.chat_rooms[p_c1].left_child = c2
        else:
            self.chat_rooms[p_c1].right_child = c2

        if self.chat_rooms[p_c2].left_child == c2:
            self.chat_rooms[p_c2].left_child = c1
        else:
            self.chat_rooms[p_c2].right_child = c1

        # 해당 노드의 부모 바꾸기
        temp_parent_id = self.chat_rooms[c1].parent_id
        self.chat_rooms[c1].parent_id = self.chat_rooms[c2].parent_id
        self.chat_rooms[c2].parent_id = temp_parent_id

        self.reset_upper_dict(c1)
        self.reset_upper_dict(c2)

    def check_alarms(self, c_id):
        if self.alarm_dict.get((c_id, 1), None) is None:
            ret = (self.recursively_check_alarm(self.chat_rooms[c_id].left_child, 1)
                   + self.recursively_check_alarm(self.chat_rooms[c_id].right_child, 1))
            self.alarm_dict[(c_id, 1)] = ret

        return self.alarm_dict[(c_id, 1)]

    def recursively_check_alarm(self, curr_id, depth):
        if curr_id is None:
            return 0

        ret = 0
        if self.alarm_dict.get((curr_id, depth + 1), None) is None:
            if self.chat_rooms[curr_id].is_on:

                if self.chat_rooms[curr_id].authority >= depth:
                    ret += 1

                alarm_count = (self.recursively_check_alarm(self.chat_rooms[curr_id].left_child, depth + 1)
                               + self.recursively_check_alarm(self.chat_rooms[curr_id].right_child, depth + 1))

                ret += alarm_count
                self.alarm_dict[(curr_id, depth + 1)] = alarm_count
        else:
            if self.chat_rooms[curr_id].authority >= depth and self.chat_rooms[curr_id].is_on:
                ret += 1
            ret += self.alarm_dict[(curr_id, depth + 1)]
            # print("Good")

        return ret


N, Q = list(map(int, input().split()))
input_queries = [list(map(int, input().split())) for _ in range(Q)]

samsung = Samsung(N)
samsung.initialize(input_queries[0][1:N + 1], input_queries[0][N + 1:])

answer = []
for query in input_queries[1:]:
    order = query[0]

    if order == 200:
        # 알림 설정 토글
        samsung.toggle(query[1])
    elif order == 300:
        # 파워 세기 변경
        samsung.change_authority(*query[1:])
    elif order == 400:
        # 부모 채팅방 교체
        samsung.change_parents(*query[1:])
    elif order == 500:
        # 알림을 받을 수 있는 채팅방 수 조회
        answer.append(str(samsung.check_alarms(query[1])))

print("\n".join(answer))

