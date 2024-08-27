def rotate_magnetic(magnetic, direction):
    # 하나의 자석을 오른쪽 또는 왼쪽으로 돌려 해당 자석을 반환하는 함수
    temp_magnetic = None
    if direction == 1:
        # 왼쪽으로 돌리기
        temp_magnetic = [magnetic[-1]] + magnetic[:-1]
    elif direction == -1:
        temp_magnetic = magnetic[1:] + [magnetic[0]]
    return temp_magnetic


def recursive_rotate(magnetics, is_left, target_magnetic, original_magentic, original_direction):
    # 인자 설명
    # 자석 배열, 왼쪽으로 가는 재귀함수인지 여부, 현재 (영향을 받아) 돌아가야 하는 자석 인덱스, 원래 방향 (반대로 돌게 되기 때문)
    if is_left and target_magnetic == 0:
        return
    if not is_left and target_magnetic == 5:
        return

    # 돌려지는 자석 / 돌아간 자석의 톱니 번호
    first, second = 2, 6
    offset = -1
    if not is_left: 
        first, second = second, first
        offset *= -1

    # 동일하게 돌리기 전 톱니가 같은지 여부를 확인 / 왼쪽과 오른쪽일 경우의 케이스를 나눈다.
    have_to = False
    if is_left and target_magnetic - 1 > 0: 
        if magnetics[target_magnetic - 2][first] != magnetics[target_magnetic - 1][second]:
            have_to = True
    elif not is_left and target_magnetic + 1 < 5: 
        if magnetics[target_magnetic][first] != magnetics[target_magnetic - 1][second]:
            have_to = True
    
    # 돌려버리기
    magnetics[target_magnetic - 1] = rotate_magnetic(magnetics[target_magnetic - 1], original_direction * -1)
    
    # 다른 애들이 영향을 받으면, 아래 함수를 또한 실행한다. 재귀적으로 왼쪽 또는 오른쪽으로 퍼져나간다.
    if have_to:
        recursive_rotate(magnetics, is_left, target_magnetic+offset, target_magnetic, original_direction * -1)


def solve(magnetics, rotate_order):
    # 돌리는 순서에 따라 자석을 하나 씩 돌리게 됨
    for idx, direction in rotate_order:
        # 각각의 변수는 왼쪽이 재귀적으로 돌아야 하는가? 오른쪽이 재귀로 돌아야 하는가?
        have_to_left = False
        have_to_right = False
        if idx - 1 > 0:
            # 극이 다르다면, 돌아가야 한다 (왼쪽 케이스)
            if magnetics[idx - 2][2] != magnetics[idx - 1][6]:
                have_to_left = True
        if idx + 1 < 5:
            if magnetics[idx][6] != magnetics[idx - 1][2]:
                have_to_right = True
        
        # 일단 현재 자석을 돌려 버린다.
        magnetics[idx - 1] = rotate_magnetic(magnetic=magnetics[idx - 1], direction=direction)
        if have_to_left: recursive_rotate(magnetics, True, idx - 1, idx, direction)
        if have_to_right: recursive_rotate(magnetics, False, idx + 1, idx, direction)


T = int(input())
for t_iter in range(1, T+1):
    K = int(input())

    magnetics = [list(map(int, input().split())) for _ in range(4)]
    magnetics = magnetics
    rotate_order = [list(map(int, input().split())) for _ in range(K)]

    solve(magnetics, rotate_order)

    total_score = 0
    for idx in range(4):
        if magnetics[idx][0] == 1:
            total_score = total_score + 2 ** idx

    print(f"#{t_iter} {total_score}")
