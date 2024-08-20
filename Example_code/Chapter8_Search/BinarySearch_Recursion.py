def binary_search(arr, target):
    if len(arr) == 0:
        return 0
    
    middle_idx = len(arr) // 2

    if arr[middle_idx] == target:
        return middle_idx
    elif arr[middle_idx] > target:
        # 데이터는 왼쪽 반에 위치한다.
        return binary_search(arr[:middle_idx], target)
    elif arr[middle_idx] < target:
        # 데이터는 오른쪽 반에 위치한다.
        return middle_idx + 1 + binary_search(arr[middle_idx+1:], target)

data = [1, 2, 3, 4, 5, 6]
print(binary_search(data, 4))