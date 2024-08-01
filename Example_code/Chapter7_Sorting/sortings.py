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