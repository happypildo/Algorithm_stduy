# from collections import deque
minimum_count = float('inf')


def recursively_find(target, received_arr, popped_arr, count):
    global minimum_count

    if len(popped_arr) == len(target):
        if popped_arr == target:
            print(popped_arr, count)
            if minimum_count > count:
                minimum_count = count
            return
        else:
            return
    
    if minimum_count <= count or len(popped_arr) > len(target):
        return
    
    if received_arr[0] in target:
        item = received_arr[0]
        popped_arr.append(item)
        recursively_find(target, received_arr[1:], popped_arr[:], count)
        return
    
    # Second operation
    recursively_find(target, received_arr[1:] + [received_arr[0]], popped_arr[:], count + 1)

    # Third operation
    recursively_find(target, [received_arr[-1]] + received_arr[:-1], popped_arr[:], count + 1)



N, M = list(map(int, input().split()))
target_numbers = list(map(int, input().split()))
arr = [x for x in range(1, N + 1)]

recursively_find(target_numbers, arr, [], 0)
print(minimum_count)