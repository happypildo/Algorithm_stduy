max_cores = -1
min_lines = float('inf')

def solution(loc_of_cores, made_circuit, curr_core_idx, num_of_linked_lines, num_of_linked_cores):
    # 코어 정보, 현재 만들고 있는 서킷 맵, 현재 보려는 코어 인덱스, 지금까지 연결된 전선 수, 지금까지 연결된 코어 수
    global max_cores
    global min_lines
    if loc_of_cores.get(curr_core_idx, -1) == -1:
        if max_cores < num_of_linked_cores:
            max_cores = num_of_linked_cores
            min_lines = num_of_linked_lines
        elif max_cores == num_of_linked_cores:
            if min_lines > num_of_linked_lines:
                min_lines = num_of_linked_lines
                
        return

    loc_of_core = loc_of_cores[curr_core_idx]
    
    # 위쪽으로 선 연결
    jud = 0
    for i in range(0, loc_of_core[0]):
        jud += made_circuit[i][loc_of_core[1]]
    if jud == 0:
        # 위쪽 연결 가능
        new_circuit = []
        for i in range(len(made_circuit)):
            temp = []
            for j in range(len(made_circuit)):
                if j == loc_of_core[1] and (-1 < i < loc_of_core[0]): temp.append(2)
                else: temp.append(made_circuit[i][j])
            new_circuit.append(temp)
        
        add_lines = loc_of_core[0]
        solution(loc_of_cores, new_circuit, curr_core_idx + 1, num_of_linked_lines + add_lines, num_of_linked_cores + 1)
    
    # 아래쪽으로 선 연결
    jud = 0
    for i in range(loc_of_core[0]+1, len(made_circuit)):
        jud += made_circuit[i][loc_of_core[1]]
    if jud == 0:
        # 아래쪽 연결 가능
        new_circuit = []
        for i in range(len(made_circuit)):
            temp = []
            for j in range(len(made_circuit)):
                if j == loc_of_core[1] and (loc_of_core[0] < i < len(made_circuit)): temp.append(2)
                else: temp.append(made_circuit[i][j])
            new_circuit.append(temp)
        
        add_lines = len(new_circuit) - loc_of_core[0] - 1
        solution(loc_of_cores, new_circuit, curr_core_idx + 1, 
                 num_of_linked_lines + add_lines, num_of_linked_cores + 1)
    
    # 왼쪽으로 연결
    jud = sum(made_circuit[loc_of_core[0]][:loc_of_core[1]])
    if jud == 0:
        # 왼쪽 연결 가능
        new_circuit = []
        for i in range(len(made_circuit)):
            temp = []
            for j in range(len(made_circuit)):
                if i == loc_of_core[0] and (-1 < j < loc_of_core[1]): temp.append(2)
                else: temp.append(made_circuit[i][j])
            new_circuit.append(temp)

        add_lines = loc_of_core[1]
        solution(loc_of_cores, new_circuit, curr_core_idx + 1, num_of_linked_lines + add_lines, num_of_linked_cores+1)
    
    # 오른쪽으로 연결
    jud = sum(made_circuit[loc_of_core[0]][loc_of_core[1]+1:])
    if jud == 0:
        # 오른쪽 연결 가능
        new_circuit = []
        for i in range(len(made_circuit)):
            temp = []
            for j in range(len(made_circuit)):
                if i == loc_of_core[0] and (loc_of_core[1] < j < len(made_circuit)): temp.append(2)
                else: temp.append(made_circuit[i][j])
            new_circuit.append(temp)

        add_lines = len(new_circuit) - loc_of_core[1] - 1
        solution(loc_of_cores, new_circuit, curr_core_idx + 1, 
                 num_of_linked_lines + add_lines, num_of_linked_cores + 1)

    # 그냥 넘어가기
    solution(loc_of_cores, made_circuit, curr_core_idx + 1, num_of_linked_lines, num_of_linked_cores)



T = int(input())

for t_iter in range(1, T+1):
    max_cores = -1
    min_lines = float('inf')

    N = int(input())

    loc_of_cores = {}   # key: core index, value: core location (tuple)
    core_idx = 0
    circuit = []

    for n_iter in range(N):
        line = list(map(int, input().split())) 
        for idx, val in enumerate(line):
            if val == 1:
                if n_iter == 0 or n_iter == N - 1:  # 가장자리에 있을 경우에는 전선을 따로 연결하지 않아도 됨.
                    line[idx] = 2
                elif idx == 0 or idx == N - 1:      # 가장자리에 있을 경우에는 전선을 따로 연결하지 않아도 됨.
                    line[idx] = 2
                else:                               # 가장자리가 아닌 어딘가에 있는 코어는 전선을 달아줘야 함.
                    loc_of_cores[core_idx] = (n_iter, idx, )
                    core_idx += 1
        circuit.append(line)
    
    solution(loc_of_cores, circuit, 0, 0, 0)

    print(f"#{t_iter} {min_lines}")