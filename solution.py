N, K = list(map(int, input().split()))

weights = []
values = []
for n_iter in range(N):
    w, v = list(map(int, input().split()))
    weights.append(w)
    values.append(v)

sorted_w = sorted(weights)
sorted_w_idx = sorted(range(len(weights)), key=lambda x: weights[x])
sorted_v = [values[x] for x in sorted_w_idx]

# print(sorted_w, sorted_v)
# print("----------------")

DP = {x: [0, 0] for x in range(K + 1)} # 무게, 가치
idx = 0
for k in range(1, K + 1):
    # 가방을 비우고 현재 무게로 채우자.
    first_term = sorted_v[idx] if idx < len(sorted_v) and K >= sorted_w[idx] else -1

    # 새로운 짐을 하나 추가해보자.
    second_term = DP[k - 1][1] + sorted_v[idx] if idx < len(sorted_v) and DP[k - 1][0] + sorted_w[idx] <= K else -1

    # 그냥 가자
    original_term = DP[k - 1][1]

    if max([first_term, second_term, original_term]) == first_term:
        DP[k] = [sorted_w[idx], first_term]
        idx += 1
    elif max([first_term, second_term, original_term]) == second_term:
        DP[k] = [DP[k - 1][0] + sorted_w[idx], second_term]
        idx += 1
    elif max([first_term, second_term, original_term]) == original_term:
        DP[k] = DP[k - 1]
    # print(DP[k])

print(DP[K][1])
