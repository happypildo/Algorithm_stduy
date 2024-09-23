class Dish:
    def __init__(self):
        self.name_set = set()
        self.amount_of_sushi = {}

    def make_sushi(self, name):
        global remain_sushi

        remain_sushi += 1
        if name in self.name_set:
            self.amount_of_sushi[name] += 1
        else:
            self.name_set.add(name)
            self.amount_of_sushi[name] = 1

    def eat_sushi(self, name, amount):
        global remain_sushi

        if name in self.name_set:
            if self.amount_of_sushi[name] >= amount:
                self.amount_of_sushi[name] -= amount
                remain_sushi -= amount
                amount = 0
            else:
                amount = amount - self.amount_of_sushi[name]
                remain_sushi -= self.amount_of_sushi[name]
                self.amount_of_sushi[name] = 0

            if self.amount_of_sushi[name] == 0:
                self.name_set.discard(name)
                del self.amount_of_sushi[name]

                if amount == 0:
                    return True, amount
                else:
                    return False, amount
        return False, amount


class Customer:
    def __init__(self, name, target_sushi):
        self.name = name
        self.target_sushi = target_sushi


def convert_fix2rotate(rail_len, idx, sim_t):
    ret = idx - sim_t + 1
    if ret < 0:
        if (ret * -1) % rail_len == 0:
            ret = 0
        else:
            ret += ((ret * -1) // rail_len + 1) * rail_len
    return ret


def all_customer_eat(sim_t, rail_len, customers, dishes):
    to_be_removed_customers = []
    for key in customers.keys():
        # key는 고정된 자리 위치와 동일하다.
        customer = customers[key]
        c_name, c_target_sushi = customer.name, customer.target_sushi

        dish_key = convert_fix2rotate(rail_len, key, sim_t)
        if dishes.get(dish_key, None) is not None:
            if len(dishes[dish_key].amount_of_sushi) == 0:
                del dishes[dish_key]
                continue

            is_done, remains = dishes[dish_key].eat_sushi(c_name, c_target_sushi)

            if is_done:
                to_be_removed_customers.append(key)
            else:
                customer.target_sushi = remains

    for rm_customer in to_be_removed_customers:
        del customers[rm_customer]


# 입력 받기
L, Q = list(map(int, input().split()))
queries = []

# key: location
# value: 앉은 사람
chair_dict = {}

# key: original location
# value: 접시 클래스
dish_dict = {}

remain_sushi = 0
remain_customer = 0

for _ in range(Q):
    queries.append(input().split())

simulation_time = 1
for query in queries:
    order = int(query[0])
    target_time = int(query[1])

    # 못 갈 것이란 걸 미리 아는 방법은 없을까?
    minimum_jump = float('inf')
    for chair in chair_dict.keys():
        for dish in dish_dict.keys():
            if chair_dict[chair].name in dish_dict[dish].name_set:
                # 언젠가 가게 될 곳
                # 가장 작은 수 만큼 가면 되지 않을까?
                rot_t = convert_fix2rotate(L, dish, simulation_time)
                time_to_wait = chair - rot_t - 1
                if time_to_wait < 0:
                    time_to_wait = L - time_to_wait
                if minimum_jump > time_to_wait:
                    minimum_jump = time_to_wait

    if minimum_jump + simulation_time <= target_time:
        # 그 만큼 점프해도 됨
        simulation_time += minimum_jump
        all_customer_eat(simulation_time, L, chair_dict, dish_dict)
    else:
        # 점프하긴 빡셈
        simulation_time = target_time
        all_customer_eat(simulation_time, L, chair_dict, dish_dict)

    # cnt = 0
    # while simulation_time < target_time:
    #     if cnt > L:
    #         simulation_time = target_time
    #     if len(dish_dict) == 0 or len(chair_dict) == 0:
    #         simulation_time = target_time
    #     else:
    #         all_customer_eat(simulation_time, L, chair_dict, dish_dict)
    #         simulation_time += 1
    #     cnt += 1

    if order == 100:
        # 초밥 만들기
        x, in_name = query[2:]
        x = int(x)

        rot_t = convert_fix2rotate(L, x, simulation_time)
        if dish_dict.get(rot_t, None) is None:
            dish_dict[rot_t] = Dish()
        dish_dict[rot_t].make_sushi(in_name)
    elif order == 200:
        x, in_name, amount_sushi = query[2:]
        x = int(x)
        amount_sushi = int(amount_sushi)

        chair_dict[x] = Customer(in_name, amount_sushi)
    elif order == 300:
        all_customer_eat(simulation_time, L, chair_dict, dish_dict)
        print(len(chair_dict), remain_sushi)



