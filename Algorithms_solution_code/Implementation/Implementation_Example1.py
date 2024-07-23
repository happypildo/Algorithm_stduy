DIRECTION = {
    'U': [-1, 0],
    'D': [1, 0],
    'L': [0, -1],
    'R': [0, 1]
}

N = int(input())
moving_directions = input().split()
current_location = [0, 0]

for direction in moving_directions:
    dx, dy = DIRECTION[direction]

    temp_x = current_location[0] + dx
    temp_y = current_location[1] + dy

    if temp_x < 0 or temp_x > N - 1:
        continue
    elif temp_y < 0 or temp_y > N - 1:
        continue
    else:
        current_location[0] = temp_x
        current_location[1] = temp_y

print(current_location[0] + 1, current_location[1] + 1)