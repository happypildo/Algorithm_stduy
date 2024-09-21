MAX_LANE = 1000000000


class Customer:
    def __init__(self, loc, name, target_sushi):
        self.loc = loc
        self.name = name
        self.target_sushi = target_sushi


class Dish:
    def __init__(self):
        # Key: customer name
        # Value: Is customer alive..
        self.customer_set = set()
        self.customer_sushi_count = {}

    def delete(self, name):
        self.customer_set.discard(name)
        del self.customer_sushi_count[name]

class Restaurant:
    def __init__(self, max_lane):
        # 회전한 위치: 원래 있던 위치
        self.max_lane = max_lane
        self.dishes = [Dish() for _ in range(max_lane)]
        self.customers = []

        self.remain_customers = 0
        self.remain_sushi = 0

    def customer_sit(self, loc, name, target_sushi):
        self.customers.append(Customer(loc, name, target_sushi))
        self.remain_customers += 1

    def customer_eat(self, sim_tik):
        if len(self.customers) == 0:
            return

        alive_customers = []
        for c in self.customers:
            if c.target_sushi == 0:
                continue

            c_idx = c.loc
            d_idx = c_idx - sim_tik + 1
            while d_idx < 0:
                d_idx += self.max_lane

            if c.name in self.dishes[d_idx].customer_set:
                c.target_sushi -= self.dishes[d_idx].customer_sushi_count[c.name]
                self.remain_sushi -= self.dishes[d_idx].customer_sushi_count[c.name]

                self.dishes[d_idx].delete(c.name)

                if c.target_sushi == 0:
                    self.remain_customers -= 1
                else:
                    alive_customers.append(c)
            else:
                alive_customers.append(c)

        self.customers = alive_customers

    def locate_dish(self, sim_tik, loc, for_who):
        d_idx = loc - sim_tik + 1
        while d_idx < 0:
            d_idx += self.max_lane
        self.dishes[d_idx].customer_set.add(for_who)
        if self.dishes[d_idx].customer_sushi_count.get(for_who, None) is None:
            self.dishes[d_idx].customer_sushi_count[for_who] = 1
        else:
            self.dishes[d_idx].customer_sushi_count[for_who] += 1
        self.remain_sushi += 1


# 입력 받기
L, Q = list(map(int, input().split()))
qs = []

simulation_tik = 1
q_idx = 0

restaurant = Restaurant(L)

for _ in range(Q):
    # qs.append(input().split())

    query = input().split()

    order_type, target_tik = query[0:2]
    target_tik = int(target_tik)
    while simulation_tik < target_tik:
        simulation_tik += 1
        restaurant.customer_eat(simulation_tik)

    if query[0] == "100":
        # 초밥 만들어서 위치에 놓기
        at_loc, name = query[2:]
        restaurant.locate_dish(simulation_tik, int(at_loc), name)
        restaurant.customer_eat(simulation_tik)
    elif query[0] == "200":
        # 사람 도착
        at_loc, name, target = query[2:]
        restaurant.customer_sit(int(at_loc), name, int(target))
        restaurant.customer_eat(simulation_tik)
    elif query[0] == "300":
        # 사진 찍기
        print(restaurant.remain_customers, restaurant.remain_sushi)
