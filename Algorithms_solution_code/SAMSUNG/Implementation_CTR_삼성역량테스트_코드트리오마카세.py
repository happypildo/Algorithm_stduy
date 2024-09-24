import sys
sys.stdin= open("fucking_shit.txt")

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


def get_minimum_jump(customers, dishes, sim_t):
    # 못 갈 것이란 걸 미리 아는 방법은 없을까?
    # minimum_jump 까지는 점프해야 누군가 먹는 액션이 발생한다.
    minimum_jump = float('inf')
    for chair in customers.keys():
        for dish in dishes.keys():
            if customers[chair].name in dishes[dish].name_set:
                # 언젠가 가게 될 곳
                # 가장 작은 수 만큼 가면 되지 않을까?
                fix_t = (dish + sim_t - 1) % L
                time_to_wait = chair - fix_t
                if time_to_wait < 0:
                    time_to_wait = L + time_to_wait
                if minimum_jump > time_to_wait:
                    minimum_jump = time_to_wait
    return minimum_jump


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

answer = []
simulation_time = 1
for idx, query in enumerate(queries):
    order = int(query[0])
    target_time = int(query[1])

    while simulation_time < target_time:
        min_jump = get_minimum_jump(chair_dict, dish_dict, simulation_time)

        if min_jump == 0:
            all_customer_eat(simulation_time, L, chair_dict, dish_dict)
            simulation_time += 1
        elif min_jump + simulation_time <= target_time:
            all_customer_eat(simulation_time, L, chair_dict, dish_dict)
            simulation_time += min_jump
        else:
            simulation_time = target_time

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
        # print(idx, len(chair_dict), remain_sushi)
        answer.append(f"{len(chair_dict)} {remain_sushi}")
    # print(idx, query, len(chair_dict), remain_sushi)
print("\n".join(answer))


