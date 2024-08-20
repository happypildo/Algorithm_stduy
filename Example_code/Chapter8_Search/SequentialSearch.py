def sequential_sort(arr, target):
    ret = []
    for idx, elem in enumerate(arr):
        if elem == target:
            ret.append(idx)
    return ret

data = ["Hi", "My", "Name", "Is", "Pildo"]
print(sequential_sort(data, "My"))