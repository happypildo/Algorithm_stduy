N, K = list(map(int, input().split()))      # 짐 개수, 가방 한계치

baggages = [
    list(map(int, input().split())) for _ in range(N)
]       
baggages = sorted(baggages, key=lambda x:x[0])

# (i, k)는 넣고자 하는 짐이 [0 ~ i]까지 있고 가방 한계치가 k일 때, 짐의 최대 가치
DP = [[0 for k in range(K + 1)] for n in range(N + 1)]

for i in range(1, N + 1):
    for w in range(K + 1):
        if w < baggages[i - 1][0]:
            # 지금 보려는 짐의 무게가 가방 한계치보다 높다!
            # 따라서, 넣지 못하고 이전까지 정보를 활용한다.
            DP[i][w] = DP[i - 1][w]
        else:
            # 지금 보려는 짐을 넣을 수 있다!
            DP[i][w] = max(
                DP[i - 1][w],                   # 넣지 않는 것이 이득이 될 수 있다.
                baggages[i - 1][1] + DP[i - 1][w - baggages[i - 1][0]] # 넣고, 남은 무게를 채우는 것이 이득이 될 수 있다.
            )

print(DP[N][K])

"""
4 8
2 1
3 2
4 5
5 6
"""