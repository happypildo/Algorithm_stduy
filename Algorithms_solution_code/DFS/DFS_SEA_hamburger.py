maximum_score = -1


def make_hamburger(remains, selected, ingredient_info, cumulative_calorie, cumulative_score, calorie_limit):
    global maximum_score

    if cumulative_calorie > calorie_limit:
        return

    for idx in range(len(remains)):
        new_remains = remains[idx+1:]
        new_selected = selected + [remains[idx]]

        new_score = cumulative_score + ingredient_info[remains[idx]][0]
        new_calorie = cumulative_calorie + ingredient_info[remains[idx]][1]

        if new_calorie <= calorie_limit:
            if maximum_score < new_score:
                maximum_score = new_score
        make_hamburger(new_remains, new_selected, ingredient_info, new_calorie, new_score, calorie_limit)


T = int(input())
for t_iter in range(1, T+1):
    N, L = list(map(int, input().split()))

    info = []
    for _ in range(N):
        info.append(list(map(int, input().split())))

    maximum_score = 0
    make_hamburger([x for x in range(N)], [], info, 0, 0, L)
    print(f"#{t_iter} {maximum_score}")