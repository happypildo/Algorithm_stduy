import sys
sys.stdin = open("")
perm = []

def product(arr, k, selected):
    if len(selected) == k:
        perm.append(selected)
        return

    for idx, item in enumerate(arr):
        temp_selected = selected + [item]
        product(arr, k, temp_selected)


def permutation(arr, k, selected):
    if len(selected) == k:
        perm.append(selected)
        return

    for idx, item in enumerate(arr):
        temp_selected = selected + [item]
        permutation(arr[:idx] + arr[idx + 1:], k, temp_selected)

def combination(arr, k, selected):
    if len(selected) == k:
        perm.append(selected)
        return

    for idx, item in enumerate(arr):
        temp_selected = selected + [item]
        combination(arr[idx + 1:], k, temp_selected)


perm = []
product([1, 2, 3, 4], 4, [])
print(perm)
print(len(perm))

perm = []
permutation([1, 2, 3, 4], 4, [])
print(perm)
print(len(perm))

perm = []
combination([1, 2, 3, 4], 2, [])
print(perm)
print(len(perm))