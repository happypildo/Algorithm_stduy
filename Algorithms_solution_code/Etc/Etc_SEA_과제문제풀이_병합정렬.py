def merge_sort(N, arr):
    if len(arr) == 0 or len(arr) == 1: return arr
    
    half = N // 2
    left_half = arr[:half]
    right_half = arr[half:]
    
    left_half = merge_sort(len(left_half), left_half)
    right_half = merge_sort(len(right_half), right_half)
    
    return merge(left_half, right_half)

count = 0
def merge(left_half, right_half):
    global count
    merge_result = []
    
    if left_half[-1] > right_half[-1]: count += 1
    
    i, j = 0, 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]: 
            merge_result.append(left_half[i])
            i += 1
        else: 
            merge_result.append(right_half[j])
            j += 1
    
    merge_result.extend(left_half[i:])
    merge_result.extend(right_half[j:])
    
    return merge_result

T = int(input())

for t_iter in range(1, T+1):
    count = 0
    
    N = int(input())
    
    arr = list(map(int, input().split()))
    arr = merge_sort(N, arr)
    
    print(f"#{t_iter} {arr[N//2]} {count}")
