class ChatRoom:
    def __init__(self, parent_idx, power):
        self.parent_idx = parent_idx
        self.power = power

        self.child_idx = set()
        self.is_on = True

class Samsung:
    def __init__(self, num_of_chatroom, chat_room_info):
        self.chat_dict = {
            0: ChatRoom(0, 0)
        }

        parent_info = chat_room_info[:num_of_chatroom]
        power_info = chat_room_info[num_of_chatroom:]

        cnt = 1
        for parent, power in zip(parent_info, power_info):
            self.chat_dict[cnt] = ChatRoom(parent_idx=parent, power=power)
            self.chat_dict[parent].child_idx.add(cnt)
            cnt += 1

    def toggle_onoff(self, num):
        self.chat_dict[num].is_on = False if self.chat_dict[num].is_on else True

    def change_power(self, num, power):
        self.chat_dict[num].power = power

    def change_parent(self, num1, num2):
