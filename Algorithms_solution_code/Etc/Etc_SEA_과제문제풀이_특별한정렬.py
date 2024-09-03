def quick_sort(arr):
    n = len(arr)
    if n == 0 or n == 1: return arr
    
    pivot = 0
    left = 1
    right = n - 1

    while True:
        while left < n - 1 and arr[left] < arr[pivot]:
            left += 1
        while right > 0 and arr[right] >= arr[pivot]:
            right -= 1
        if left < right:
            arr[left], arr[right] = arr[right], arr[left]
        else: break
    
    arr[pivot], arr[right] = arr[right], arr[pivot]
    
    left_arr = quick_sort(arr[:right])
    right_arr = quick_sort(arr[right+1:])
    
    return left_arr + [arr[right]] + right_arr


T = int(input())
for t_iter in range(1, T+1):
    N = int(input())
    
    data = list(map(int, input().split()))
    data = quick_sort(data)
    data = [-1] + data
    
    answer = []
    for i in range(1, 6):
        answer.append(data[-1 * i])
        answer.append(data[i])
    print(f"#{t_iter}", end=" ")
    for c in answer:
        print(c, end=" ")
    print()