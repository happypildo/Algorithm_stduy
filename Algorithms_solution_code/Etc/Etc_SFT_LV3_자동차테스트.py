def binary_search(arr, val):
    s = 0
    e = len(arr)
    while s < e:
        half = (s + e) // 2
        
        if arr[half] == val: return half
        elif arr[half] < val:
            s = half
        else:
            e = half
    
    
n, q = list(map(int, input().split()))

efficiency = list(map(int, input().split()))
eff_set = set(efficiency)
sorted_eff_list = sorted(efficiency)

answer = []
for _ in range(q):
    exp = int(input())
    # print("-"*10)
    if exp not in eff_set: answer.append("0")
    else:
        idx = binary_search(sorted_eff_list, exp)
        left = idx
        right = n - idx - 1
        answer.append(f"{left * right}")
print("\n".join(answer))