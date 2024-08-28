N = int(input())

arr = list(map(int, input().split()))
DP = [1 for _ in range(N)]

latest_largest_idx = 1
for i in range(N):
    if i == 0: continue

    found = False
    candi_DP = -1
    candi_lli = -1
    for j in range(latest_largest_idx, -1, -1):
        if arr[i] > arr[j]:
            if DP[j] + 1 >= DP[i - 1]:
                if candi_DP < DP[j] + 1:
                    candi_DP = DP[j] + 1
                    candi_lli = i
                found = True
    if found:
        DP[i] = candi_DP
        latest_largest_idx = i
    else:
        DP[i] = DP[i - 1]
        # latest_largest_idx = i
print(DP)
print(DP[-1])