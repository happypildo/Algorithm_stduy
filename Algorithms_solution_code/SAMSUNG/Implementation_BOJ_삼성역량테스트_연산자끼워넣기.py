from itertools import permutations

N = int(input())

values = list(map(int, input().split()))
num_of_operators = list(map(int, input().split()))
operator = ['+', '-', '*', '/']
operators = []
for idx, num in enumerate(num_of_operators):
    for _ in range(num):
        operators.append(operator[idx])

already_calculated = set()
max_result = -1000000001
min_result = float('inf')

for comb in permutations(operators, N - 1):
    if comb in already_calculated:
        continue

    already_calculated.add(comb)

    left_hand = values[0]
    value_idx = 1
    while value_idx < len(values):
        right_hand = values[value_idx]
        operator = comb[value_idx - 1]

        if operator == '+':
            left_hand += right_hand
        elif operator == '-':
            left_hand -= right_hand
        elif operator == '*':
            left_hand *= right_hand
        else:
            if left_hand < 0:
                temp_lh = left_hand * -1
                temp_lh //= right_hand
                left_hand = temp_lh * -1
            else:
                left_hand //= right_hand

        value_idx += 1

    if max_result < left_hand:
        max_result = left_hand
    if min_result > left_hand:
        min_result = left_hand

print(max_result)
print(min_result)