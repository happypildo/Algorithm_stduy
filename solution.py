N = int(input())

DP = [1, 2]
for i in range(2, N):
    DP.append(DP[i - 1] % 10007 + DP[i - 2] % 10007)
print(DP[N-1] % 10007)