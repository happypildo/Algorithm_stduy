N = int(input())

stack = []
is_visited = set()
popped_number = set()
current_head = 0
operations = ""

can_make = True
for n_iter in range(N):
    target_number = int(input())
    if target_number in popped_number:
        can_make = False
        break

    if current_head < target_number:
        for i in range(current_head + 1, target_number + 1):
            if i not in is_visited:
                stack.append(i)
                operations += "+\n"
                is_visited.add(i)
    
    while True:
        if len(stack) == 0:
            can_make = False
            break
        
        item = stack.pop()
        popped_number.add(item)
        operations += "-\n"

        if item == target_number:
            break
    
    if not can_make:
        break
    if len(stack) != 0:
        current_head = stack[-1]
    else:
        current_head = 0

if can_make:
    print(operations)
else:
    print("NO")