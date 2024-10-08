maximum_profit = -1
maximum_honey_list = []


def get_maximum_honey_combination(selected, remains, honeys, current_C, C):
    global maximum_profit
    global maximum_honey_list

    if current_C > C:
        return

    for idx in range(len(remains)):
        new_selected = selected + [remains[idx]]
        new_remains = remains[idx+1:]
        new_honey = current_C + honeys[remains[idx]]

        if new_honey <= C:
            profit = sum([honeys[i] ** 2 for i in new_selected])
            if maximum_profit < profit:
                maximum_profit = profit
                maximum_honey_list = [honeys[i] for i in new_selected]

        get_maximum_honey_combination(new_selected, new_remains, honeys, new_honey, C)


def shrink_honey_for_user(input_map, N, M, C):
    ret_map = []

    for i in range(N):
        temp_ret = []

        for j in range(N):
            if j + M > N:
                break
            else:
                honeys = input_map[i][j:j+M]
                if sum(honeys) > C:
                    global maximum_profit
                    global maximum_honey_list

                    maximum_profit = -1
                    maximum_honey_list = []

                    # C보다 높은 경우에는, 
                    # 채취할 수 있는 꿀의 양이 정해져 있기에 최대 이득을 낼 수 있는 조합을 찾아야 한다.
                    get_maximum_honey_combination([], [x for x in range(len(honeys))], honeys, 0, C)
                    # Maximum_honey_list에는 최대 수익을 낼 수 있는 꿀 조합을 나타낸다.
                    honeys = [h ** 2 for h in maximum_honey_list]
                    temp_ret.append(sum(honeys))
                else:
                    honeys = [h ** 2 for h in honeys]
                    temp_ret.append(sum(honeys))
        # 각 라인별로 얻을 수 있는 최대 이득들을 저장한다.
        ret_map.append(temp_ret)

    return ret_map


T = int(input())
for t_iter in range(1, T+1):
    N, M, C = list(map(int, input().split()))

    honey_house = []
    for n_iter in range(N):
        honey_house.append(list(map(int, input().split())))

    honey_house = shrink_honey_for_user(honey_house, N, M, C)
    print(honey_house)

    honey_house_1d = []
    for i in range(N):
        for j in range(len(honey_house[0])):
            honey_house_1d.append(honey_house[i][j])
    # 최대 이득을 내림차순으로 정렬한 index를 반환
    honey_house_1d_idx = sorted(range(len(honey_house_1d)), reverse=True, key=lambda k: honey_house_1d[k])

    # 가장 큰 이득을 내는 것을 첫 사람이 취해야 한다.
    first_max_idx = honey_house_1d_idx[0]
    second_max_idx = -1
    idx = 1
    while True:
        if first_max_idx // (N - M + 1) != honey_house_1d_idx[idx] // (N - M + 1):
            # 겹치지 않는 부분일 경우를 의미
            second_max_idx = honey_house_1d_idx[idx]
            break
        if first_max_idx // (N - M + 1) == honey_house_1d_idx[idx] // (N - M + 1):
            # 1차원으로 변환했기 때문에 겹칠 수도 있다.
            if honey_house_1d_idx[idx] > first_max_idx + M - 1:
                # 겹치지 않음이 확정된다.
                second_max_idx = honey_house_1d_idx[idx]
                break
        idx = idx + 1

    max_profit = honey_house_1d[first_max_idx] + honey_house_1d[second_max_idx]
    print(f"#{t_iter} {max_profit}")
