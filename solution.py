def make_child_dict(graph, node, layer, child_dict):
    if layer in child_dict:
        child_dict[layer].append(len(graph[node]))
    else:
        child_dict[layer] = [len(graph[node])]

    for child in graph[node]:
        make_child_dict(graph, child, layer+1, child_dict)


T = int(input())

for t_iter in range(T):
    first_line = list(input().split())
    second_line = list(input().split())

    # Temporal
    trees = []
    for line in [first_line, second_line]:
        idx = 0
        parent = line[idx]
        temp_tree = {}
        parent_dict = {}

        while idx < len(line) - 1:
            child = line[idx + 1]

            parent_dict[child] = parent

            if parent in temp_tree:
                temp_tree[parent].append(child)
            else:
                temp_tree[parent] = [child]

            if child == '#':
                temp_tree[parent] = temp_tree[parent][:-1]
                if parent == line[0]:
                    break
                parent = parent_dict[parent]
            else:
                parent = child

            idx += 1
        trees.append(temp_tree)

    child_count1 = {}
    make_child_dict(trees[0], first_line[0], 0, child_count1)
    child_count2 = {}
    make_child_dict(trees[1], second_line[0], 0, child_count2)

    jud = True
    for key in child_count1:
        if key not in child_count2:
            jud = False
            break

        if sorted(child_count1[key]) != sorted(child_count2[key]):
            jud = False
            break

    if jud:
        print("The two trees are isomorphic.")
    else:
        print("The two trees are not isomorphic.")
