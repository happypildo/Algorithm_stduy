from itertools import product

N = int(input())
to_product = [[0, 1] for _ in range(N)]
info = [list(map(int, input().split())) for _ in range(N)]

answer = -1
for prod in product(*to_product):
    meetings = []
    for idx, jud in enumerate(prod):
        if jud == 1:
            meeting = [idx + 1, idx + 1 + info[idx][0] - 0.5, info[idx][1]]
            meetings.append(meeting)

    if len(meetings) == 0:
        continue

    cannot = False
    s, e, values = meetings[0]
    if e > N + 1:
        continue
    for meeting in meetings[1:]:
        # 시작 시간이 이전 회의의 끝 시간보다 커야 하고,
        # 끝나는 시간이 총 시간보다 작아야 한다.
        if e > meeting[0] or meeting[1] > N + 1:
            cannot = True
            break

        values += meeting[2]
        s, e = meeting[:2]

    if not cannot and answer < values:
        answer = values

answer = 0 if answer == -1 else answer
print(answer)

