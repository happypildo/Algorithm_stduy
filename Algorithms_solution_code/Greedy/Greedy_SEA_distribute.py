T = int(input())

for t_iter in range(1, T+1):
    N, K = list(map(int, input().split()))
    candy_bags = list(map(int, input().split()))
    candy_bags = sorted(candy_bags, reverse=True)

    min_gap = float('inf')
    for idx in range(N):
        if idx + K - 1 > N - 1:
            continue
        else:
            temp_gap = candy_bags[idx] - candy_bags[idx + K - 1]
            if min_gap > temp_gap:
                min_gap = temp_gap

    print(f"#{t_iter} {min_gap}")