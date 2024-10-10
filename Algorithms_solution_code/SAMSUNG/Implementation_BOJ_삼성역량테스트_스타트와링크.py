from itertools import combinations

N = int(input())

teams = set([x for x in range(N)])
synergy_arr = [list(map(int, input().split())) for _ in range(N)]

min_gap = float('inf')
for comb in combinations([x for x in range(N)], N // 2):
    first_team = comb
    second_team = tuple(teams - set(comb))

    first_team_power = 0
    second_team_power = 0
    for i1, i2 in zip(first_team, second_team):
        for j1, j2 in zip(first_team, second_team):
            first_team_power += synergy_arr[i1][j1]
            second_team_power += synergy_arr[i2][j2]

    gap = abs(first_team_power - second_team_power)

    if min_gap > gap:
        min_gap = gap

print(min_gap)