T = int(input())

for t_iter in range(1, T+1):
    N = int(input())
    
    happy_days = [int(input()) - 1 for _ in range(N)]
    multipliers = [happy_days[1]]
    
    for happy in happy_days[2:]:
        is_there = False
        for mul in multipliers:
            if happy % mul == 0:
                is_there = True
                break
        if not is_there: multipliers.append(happy)
    
    print(f"#{t_iter} {len(multipliers)}")
    