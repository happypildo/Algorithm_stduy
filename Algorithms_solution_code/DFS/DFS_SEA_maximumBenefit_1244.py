switch_results = set()
MEMOIZATION = {}
 
 
def make_possible_combinations(N):
    results = []
 
    for i in range(N):
        temp_arr = [i]
        for j in range(i+1, N):
            results.append(temp_arr + [j])
 
    return results
 
 
def switch_numbers(given_string, possible_combinations, switch_count):
    global switch_results
    global MEMOIZATION
 
    memoi_value = MEMOIZATION.get(f"{given_string}_{switch_count}", None)
    if memoi_value is not None:
        switch_results.add(int(memoi_value))
        return int(memoi_value)
    if switch_count == 0:
        switch_results.add(int(given_string))
        return int(given_string)
 
    dict_ret = MEMOIZATION.get(given_string, None)
    if dict_ret is None:
        temp_strings = set()
        for comb in possible_combinations:
            first_idx = comb[0]
            second_idx = comb[1]
 
            temp_string = ""
            for idx, c in enumerate(given_string):
                if idx == first_idx:
                    temp_string = temp_string + given_string[second_idx]
                elif idx == second_idx:
                    temp_string = temp_string + given_string[first_idx]
                else:
                    temp_string = temp_string + c
            temp_strings.add(temp_string)
 
        MEMOIZATION[given_string] = temp_strings
        returns = []
        for temp_string in temp_strings:
            returns.append(switch_numbers(temp_string, possible_combinations, switch_count - 1))
        MEMOIZATION[f"{given_string}_{switch_count}"] = max(returns)
 
        return MEMOIZATION[f"{given_string}_{switch_count}"]
    else:
        returns = []
        for temp_string in MEMOIZATION[given_string]:
            returns.append(switch_numbers(temp_string, possible_combinations, switch_count - 1))
        MEMOIZATION[f"{given_string}_{switch_count}"] = max(returns)
 
        return MEMOIZATION[f"{given_string}_{switch_count}"]
 
 
T = int(input())
 
for t_iter in range(1, T+1):
    numbers, count = input().split()
 
    switch_results = set()
    possible_combinations = make_possible_combinations(len(numbers))
 
    switch_numbers(numbers, possible_combinations, int(count))
 
    print(f"#{t_iter} {max(switch_results)}")