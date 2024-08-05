CARDS = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]


def selection_sort():
    for i in range(len(CARDS)):
        min_idx = i
        min_value = CARDS[i]
        for j in range(i+1, len(CARDS)):
            if CARDS[j] < min_value:
                min_value = CARDS[j]
                min_idx = j
        
        CARDS[i], CARDS[min_idx] = CARDS[min_idx], CARDS[i]


selection_sort()
print(CARDS)
CARDS = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]


def insertion_sort():
    for i in range(1, len(CARDS)):
        for j in range(i, 0, -1):
            if CARDS[j] < CARDS[j - 1]:
                CARDS[j], CARDS[j - 1] = CARDS[j - 1], CARDS[j]
            else:
                break


insertion_sort()
print(CARDS)
CARDS = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]

def quick_sort(arr):
    if len(arr) == 0 or len(arr) == 1:
        return arr
        
    pivot = 0

    left = 1
    right = len(arr) - 1
    while left < right:
        while left < len(arr) and arr[left] < arr[pivot]:
            left = left + 1
        while right > 0 and arr[right] > arr[pivot]:
            right = right - 1
        
        if left > right:
            arr[pivot], arr[right] = arr[right], arr[pivot]
        else:
            arr[left], arr[right] = arr[right], arr[left]
    
    sorted_arr = quick_sort(arr[:right]) + [arr[right]] + quick_sort(arr[right+1:])

    return sorted_arr

print(quick_sort(CARDS))