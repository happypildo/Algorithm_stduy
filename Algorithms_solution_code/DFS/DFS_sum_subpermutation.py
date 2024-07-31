def make_target_number(remains, current_sum, target_num):
    ret = 0
    if current_sum == target_num:
        return 1
    if current_sum > target_num:
        return 0

    for idx in range(len(remains)):
        ret = ret + make_target_number(remains[idx+1:], current_sum + remains[idx], target_num)

    return ret


T = int(input())
for t_iter in range(1, T+1):
    N, K = list(map(int, input().split()))
    input_numbers = list(map(int, input().split()))

    print(f"#{t_iter} {make_target_number(input_numbers, 0, K)}")