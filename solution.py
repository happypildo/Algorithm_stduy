from collections import deque


class Node:
    def __init__(self, node_id, parent_id, auth):
        self.node_id = node_id
        self.parent_id = parent_id
        self.authority = auth

        self.is_on = True
        self.child_set = set()
        self.alarm_set = set()


class ChatRoom:
    def __init__(self, num_of_nodes, parent_ids, auths):
        self.chats = {}
        to_be_added = []
        for i in range(1, num_of_nodes + 1):
            self.chats[i] = Node(i, parent_ids[i - 1], auths[i - 1])
            if self.chats.get(parent_ids[i - 1], None) is not None:
                self.chats[parent_ids[i - 1]].child_set.add(i)
            else:
                to_be_added.append((parent_ids[i - 1], i))

        for p_id, c_id in to_be_added:
            self.chats[p_id].child_set.add(c_id)

    def find_alarm_set(self, target_node_id):
        # 타겟 노드에서 아래로 내려가면서 알람 셋을 설정한다.

        return

    def toggle(self, node_id):
        self.chats[node_id].is_on = False if self.chats[node_id].is_on else True

    def change_authority(self, node_id, power):
        self.chats[node_id].authority = power
