# Merge Sort
def merge_sort(arr):
    n = len(arr)
    
    if n == 1:
        return arr
    
    half = n // 2
    left_half, right_half = arr[:half], arr[half:]
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    
    return merge(left_half, right_half)

def merge(left, right):
    merged = []
    
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged

arr = [5, 9, 8, 2, 3, 1, 7, 6, 8]
print(merge_sort(arr))

# Quick sort
def quick_sort(arr):
    n = len(arr)
    if n == 1 or n == 0: return arr
    
    pivot = 0
    left = 1
    right = n - 1
    
    while True:
        while left <= n - 1 and arr[left] < arr[pivot]:
            left += 1
        while right > pivot and arr[right] >= arr[pivot]:
            right -= 1
        
        if left < right:
            arr[left], arr[right] = arr[right], arr[left]
        else:
            break
    
    arr[pivot], arr[right] = arr[right], arr[pivot]
    
    left_arr = quick_sort(arr[:right])
    right_arr = quick_sort(arr[right+1:])
    
    return left_arr + [arr[right]] + right_arr
    
print(quick_sort(arr))

    