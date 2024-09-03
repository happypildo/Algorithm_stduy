def quick_sort(arr):
    if len(arr) == 0 or len(arr) == 1: return arr
    if len(arr) == 2:
        if arr[0] > arr[1]: arr[0], arr[1] = arr[1], arr[0]
        return arr
    pivot = 0
    left = 1
    right = len(arr) - 1
    
    while True:
        while left <= len(arr) - 1 and arr[left] < arr[pivot]: left += 1
        while right > 1 and arr[right] >= arr[pivot]: right -= 1
        if left < right: arr[left], arr[right] = arr[right], arr[left]
        else: break
    
    arr[pivot], arr[right] = arr[right], arr[pivot]
    
    left_arr = quick_sort(arr[:right])
    right_arr = quick_sort(arr[right+1:])
    
    return left_arr + [arr[right]] + right_arr
    

T = int(input())

for t_iter in range(1, T+1):
    N = int(input())
    
    arr = list(map(int, input().split()))
    arr = quick_sort(arr)
    
    print(f"#{t_iter} {arr[N // 2]}")