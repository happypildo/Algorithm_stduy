def get_profit(N, M, input_map, center_point, service_are_size):
    x, y = center_point

    offsets = [k for k in range(service_are_size)]
    offsets.extend([k for k in range(service_are_size-2, -1, -1)])
    x_axis = [x + k for k in range(-service_are_size + 1, service_are_size)]

    operational_price = service_are_size ** 2 + (service_are_size - 1) ** 2

    house_count = 0
    for idx, temp_x in enumerate(x_axis):
        for temp_y in range(y - offsets[idx], y + offsets[idx] + 1):
            if (-1 < temp_x < N) and (-1 < temp_y < N):
                house_count = house_count + input_map[temp_x][temp_y]
    profit = house_count * M - operational_price

    return profit, house_count


def move_filter(N, M, input_map):
    x_from, y_from = N // 2, N // 2
    x_to, y_to = N // 2, N // 2
    cnt = 1                         # service area size (K) = N - cnt + 1
    while N - cnt + 1 > 0:
        house_counts = []
        for i in range(x_from, x_to + 1):
            for j in range(y_from, y_to + 1):
                if i < 0 or i > N - 1 or j < 0 or j > N - 1:
                    continue
                else:
                    profit, house_count = get_profit(N, M, input_map, [i, j], N - cnt + 1)
                    if profit >= 0:
                        house_counts.append(house_count)
        if len(house_counts) > 0:
            return max(house_counts)

        x_from, y_from = N // 2 - cnt, N // 2 - cnt
        x_to, y_to = N // 2 + cnt, N // 2 + cnt
        cnt = cnt + 1

    return 0


T = int(input())
for t_iter in range(1, T+1):
    N, M = list(map(int, input().split()))

    input_map = []
    for _ in range(N):
        input_map.append(list(map(int, input().split())))

    max_k = 0
    if N % 2 == 0:
        # N을 홀수로... 규칙이 있기 때문
        for n_iter in range(N):
            input_map[n_iter].append(0)
        input_map.append([0 for _ in range(N+1)])
        N = N + 1
    answer = move_filter(N, M, input_map)

    print(f"#{t_iter} {answer}")



