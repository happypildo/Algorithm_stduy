from itertools import product


def merge(N, line):
    idx = 0
    new_line = []
    for val in line:
        if val == 0:
            continue
        else:
            new_line.append(val)
    line = new_line[:]
    new_line = []

    while idx < len(line):
        if idx + 1 < len(line):
            if line[idx] == line[idx + 1]:
                new_line.append(line[idx] * 2)
                idx += 2
            else:
                new_line.append(line[idx])
                idx += 1
        else:
            new_line.append(line[idx])
            idx += 1

    while len(new_line) != N:
        new_line.append(0)

    return new_line


def search_all(N, game_board):
    highest_score = 0
    for prod in product(range(5), range(5), range(5), range(5), range(5)):
        # if prod == (0, 2, 0, 0, 0):
        #     print()
        new_map = [game_board[i][:] for i in range(len(game_board))]
        for direction in prod:
            if direction == 0:
                # 상
                for j in range(len(new_map)):
                    line = []
                    for i in range(len(new_map)):
                        line.append(new_map[i][j])
                    new_line = merge(N, line)
                    for i in range(len(new_map)):
                        new_map[i][j] = new_line[i]
            elif direction == 1:
                # 하
                for j in range(len(new_map)):
                    line = []
                    for i in range(len(new_map) - 1, -1, -1):
                        line.append(new_map[i][j])
                    new_line = merge(N, line)
                    for i in range(len(new_map)):
                        new_map[i][j] = new_line[len(new_map) - i - 1]
            elif direction == 2:
                # 좌
                for i in range(len(new_map)):
                    new_map[i] = merge(N, new_map[i][:])
            elif direction == 3:
                # 우
                for i in range(len(new_map)):
                    new_line = merge(N, new_map[i][::-1])
                    for j in range(len(new_map)):
                        new_map[i][j] = new_line[len(new_map) - j - 1]
            else:
                # 아무 것도 안 함
                pass
        for line in new_map:
            for val in line:
                if highest_score < val:
                    highest_score = val
    return highest_score


N = int(input())
board = [list(map(int, input().split())) for _ in range(N)]
print(search_all(N, board))