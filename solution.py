def calculate_line(first_loc, sec_loc):
    x1, y1 = first_loc
    x2, y2 = sec_loc

    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    return (a, b)

def find_the_poor(locations, target_x):
    # LEFT
    left_visibile_building = -1
    temp_x = target_x
    while True:
        temp_x -= 1
        if 0 > temp_x:
            break
        a, b = calculate_line(locations[target_x], locations[temp_x])
        temp_visible_building = 1
        for btw_x in range(target_x - 1, temp_x, -1):
            btw_y = a * btw_x + b
            real_y = locations[btw_x][1]

            if btw_y > real_y:
                temp_visible_building += 1
            else:
                temp_visible_building -= 1
                break
        
        if left_visibile_building < temp_visible_building:
            left_visibile_building = temp_visible_building
    # RIGHT
    right_visibile_building = -1
    temp_x = target_x
    while True:
        temp_x += 1
        if len(locations) - 1 < temp_x:
            break
        a, b = calculate_line(locations[target_x], locations[temp_x])
        temp_visible_building = 1
        for btw_x in range(target_x + 1, temp_x):
            btw_y = a * btw_x + b
            real_y = locations[btw_x][1]

            if btw_y > real_y:
                temp_visible_building += 1
            else:
                print("OSS")
                temp_visible_building -= 1
                break
        
        if right_visibile_building < temp_visible_building:
            right_visibile_building = temp_visible_building
    
    return left_visibile_building + right_visibile_building

X = int(input())
locations = []
Y = list(map(int, input().split()))
for x in range(X):
    locations.append((x, Y[x]))

results = []
for x in range(X):
    results.append(find_the_poor(locations, x))
    print(results)
print(max(results))